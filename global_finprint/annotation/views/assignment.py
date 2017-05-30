from datetime import date, timedelta
import numpy as np
import json
import re as re
from django.views.generic import View
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.db.models import Count
from django.http.response import JsonResponse, HttpResponse
from django.template import RequestContext

from ...core.mixins import UserAllowedMixin
from ...trip.models import Trip
from ...bruv.models import Set
from ...habitat.models import Location, Site
from ...core.models import Affiliation, FinprintUser
from ..models.video import Assignment, Video, AnnotationState
from ..models.project import Project
from ..models.custommodels import MultiVideoAssignmentData


class VideoAutoAssignView(UserAllowedMixin, View):
    """
    View to handle auto-assignment functionality found at /assignment/
    """
    def assign_video(self, annotators, video, num, project):
        """
        Assign a video to a number of annotators
        :param annotators: list of annotator objects
        :param video: video object
        :param num: integer denoting how many annotators should have this video assigned
        :param project: project object
        :return:
        """
        avail = list(a for a in annotators if a not in video.annotators_assigned(project))
        assigned_by = FinprintUser.objects.get(user=self.request.user)
        assign_count = 0
        while len(video.annotators_assigned(project)) < num and len(annotators) > 0 and len(avail) > 0:
            ann = min(avail, key=lambda a: len(a.active_assignments()))
            Assignment(annotator=ann, video=video, assigned_by=assigned_by, project=project).save()
            avail.remove(ann)
            assign_count += 1
        return assign_count

    def post(self, request):
        """
        Endpoint used by automatic assignment modal
        :param request:
        :return:
        """
        trip_id = request.POST.get('trip')
        aff_id = request.POST.get('affiliation')
        num = int(request.POST.get('num'))
        include_leads = bool(request.POST.get('include_leads', False))
        project = get_object_or_404(Project, id=request.POST.get('project'))

        annotators = FinprintUser.objects.filter(affiliation_id=aff_id, user__is_active=True).all()
        if not include_leads:
            annotators = list(a for a in annotators if not a.is_lead())
        video_count = 0
        assigned_count = 0
        new_count = 0
        for video in Video.objects.filter(set__trip_id=trip_id).exclude(files__isnull=True).all():
            video_count += 1
            new_count += self.assign_video(annotators, video, num, project)
            assigned_count += len(video.annotators_assigned(project))

        return JsonResponse(
            {
                'status': 'ok',
                'video_count': video_count,
                'assignments':
                {
                    'total': video_count * num,
                    'assigned': assigned_count,
                    'newly_assigned': new_count
                }
            }
        )


class AssignmentListView(UserAllowedMixin, View):
    """
    View to handle the assignment screen found at /assignment/
    """
    template_name = 'pages/annotation/assignment_list.html'

    def get(self, request):
        context = RequestContext(request, {
            'locations': Location.objects.order_by('name').all().prefetch_related('trip_set'),
            'trips': Trip.objects.order_by('code').all().prefetch_related('set_set'),
            'sites': Site.objects.order_by('name').all().prefetch_related('reef_set'),
            'affils': Affiliation.objects.order_by('name').all().prefetch_related('finprintuser_set'),
            'statuses': AnnotationState.objects.all(),
            'projects': Project.objects.order_by('id').all()
        })
        return render_to_response(self.template_name, context=context)


class AssignmentListTbodyView(UserAllowedMixin, View):
    """
    Endpoint used to provide table body to the assignment screen found at /assignment/
    """
    template_name = 'pages/annotation/assignment_list_tbody.html'

    def post(self, request):
        selected_related = [
            'video', 'video__set', 'video__set__trip', 'video__set__reef_habitat', 'annotator', 'annotator__user'
        ]
        query = Assignment.objects.all().select_related(*selected_related) \
            .prefetch_related('observation_set', 'video__files')
        unassigned = Set.objects.annotate(Count('video__assignment')) \
                                .filter(video__assignment__count=0) \
                                .exclude(video__files=None)

        trips = request.POST.getlist('trip[]')
        sets = request.POST.getlist('set[]')
        reefs = request.POST.getlist('reef[]')
        annos = request.POST.getlist('anno[]')
        status = request.POST.getlist('status[]')
        assigned = request.POST.get('assigned')
        assigned_ago = request.POST.get('assigned-ago')
        project_id = request.POST.get('project_id')

        if trips:
            query = query.filter(video__set__trip_id__in=(int(t) for t in trips))
            unassigned = unassigned.filter(trip_id__in=(int(t) for t in trips))

        if sets:
            query = query.filter(video__set__id__in=(int(s) for s in sets))
            unassigned = unassigned.filter(id__in=(int(s) for s in sets))

        if reefs:
            query = query.filter(video__set__reef_habitat__reef_id__in=(int(s) for s in reefs))
            unassigned = unassigned.filter(video__set__reef_habitat__reef_id__in=(int(s) for s in reefs))

        if annos:
            query = query.filter(annotator_id__in=(int(a) for a in annos))
            unassigned = unassigned.none()

        if status:
            query = query.filter(status_id__in=(int(s) for s in status))
            unassigned = unassigned.none()

        if assigned != '':
            if assigned == '5+':
                query = query.annotate(Count('video__assignment')).filter(video__assignment__count__gte=5)
                unassigned = unassigned.none()
            elif int(assigned) == 0:
                query = query.none()
            else:
                query = query.annotate(Count('video__assignment')) \
                    .filter(video__assignment__count=int(assigned))
                unassigned = unassigned.none()

        if assigned_ago != '':
            try:
                query = query.filter(create_datetime__gte=(date.today() - timedelta(days=int(assigned_ago))))
                unassigned = unassigned.none()
            except ValueError:
                pass

        if project_id != '':
            query = query.filter(project_id=project_id)
            unassigned = unassigned.none()

        context = RequestContext(request, {'assignments': sorted(query, key=lambda a: str(a.set())),
                                           'unassigned': sorted(unassigned, key=lambda s: str(s))
                                           })
        return render_to_response(self.template_name, context=context)


class AssignmentModalBodyView(UserAllowedMixin, View):
    """
    Endpoints used by the assignment modal found at /assignment/
    """
    template_name = 'pages/annotation/assignment_modal_body.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        project = get_object_or_404(Project, id=request.GET.get('project_id', 1))
        current_assignments = set.video.assignment_set.filter(project=project).all()
        context = RequestContext(request, {
            'set': set,
            'current': current_assignments,
            'current_annos': [a.annotator for a in current_assignments],
            'affiliations': Affiliation.objects.order_by('name').all(),
            'projects': Project.objects.order_by('id').all(),
            'current_project': project,
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        project = get_object_or_404(Project, id=request.POST.get('project'))
        for anno_id in request.POST.getlist('anno[]'):
            Assignment(
                annotator=FinprintUser.objects.get(id=anno_id),
                video=set.video,
                assigned_by=FinprintUser.objects.get(user_id=request.user),
                project=project
            ).save()
        return JsonResponse({'status': 'ok'})


class UnassignModalBodyView(UserAllowedMixin, View):
    template_name = 'pages/annotation/unassign_modal_body.html'

    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        context = RequestContext(request, {
            'assignment': assignment
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        # assign.remove() clears unfinished annotations and then deletes self
        assignment.remove()
        return JsonResponse({'status': 'ok'})


class AssignmentManageView(UserAllowedMixin, View):
    """
    View to handle assignment management page found at /assignment/manage/<assignment_id>
    """
    template_name = 'pages/annotation/assignment_manage.html'

    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        context = RequestContext(request, {
            'state_list': AnnotationState.objects.all(),
            'assignment': assignment,
            'trip': assignment.video.set.trip,
            'set': assignment.video.set,
            'observations': sorted(assignment.observation_set.all()
                                   .select_related('animalobservation__animal',
                                                   'assignment__annotator__user',
                                                   'assignment__annotator__affiliation',
                                                   'assignment__video__set__trip',)
                                   .prefetch_related('event_set', 'event_set__attribute'),
                                   key=lambda o: o.initial_observation_time(), reverse=True),
            'for': 'by {0}'.format(assignment.annotator)
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request, assignment_id):
        """
        Endpoint to handle state changes and/or deletion of assignment on assignment management screen
        :param request:
        :param assignment_id:
        :return:
        """
        action = request.POST.get('action')
        assignment_state = request.POST.get('assignment_state')
        assignment = get_object_or_404(Assignment, id=assignment_id)

        if action == 'delete' and assignment.status_id == 1:
            assignment.delete()
        elif action == 'update' and assignment_state is not None:
            assignment.status_id = int(assignment_state)
            assignment.save()

        return JsonResponse({'status': 'ok'})


class AssignMultipleVideosModel(UserAllowedMixin, View):
    """
    Endpoints used by the assignment modal found at /assignment/
    """
    template_name = 'pages/annotation/multiple_assignment_list_modal.html'

    def post(self, request):
        set_ids = np.asarray(dict(request.POST)['set_ids[]'])
        video_list = np.asarray(dict(request.POST)['video_ids[]'])

        #only gives assigned list not the unassigned
        assignment_list = Assignment.get_all_assignments(video_list)
        multiple_assignment_data_dic = {}
        project_list = []
        assigned_video_list=[]
        multiple_assignment_data_set = []

        #creating a dictionary wid name_of_video ,video_id and number_of_user_assigned for model
        for assignment in assignment_list :
            project_list.append(assignment.project_id)

            if assignment.video_id not in multiple_assignment_data_dic  :
                assigned_video_list.append(assignment.video_id)
                multiple_assignment_data_dic[assignment.video_id] = {"name": str(assignment.video), "count": 1, "video_id":assignment.video_id}

            else :
                new_count = multiple_assignment_data_dic.get(assignment.video_id)["count"] +1
                multiple_assignment_data_dic[assignment.video_id] = {"name": str(assignment.video), "count": new_count, "video_id":assignment.video_id}


        unassigned_list = self.filter_unassigned_list(video_list,assigned_video_list)

        unassigned_set = Set.objects.annotate(Count('video__assignment')) \
                                .filter(video__assignment__count=0) \
                                .filter(video_id__in = unassigned_list ) \
                                .exclude(video__files=None)

        # updating dictionary wid name_of_video ,video_id and number_of_user_assigned for model
        for unassigned in unassigned_set:
            multiple_assignment_data_dic[unassigned.video_id] = {"name": str(unassigned.video), "count": 0,
                                                                 "video_id": unassigned.video_id}
        set_ids_str = ','.join(str(x) for x in set_ids)
        for video_id in video_list :
            _dic = multiple_assignment_data_dic[int(video_id)]
            multiple_assignment_data_set.append(MultiVideoAssignmentData(_dic["name"],_dic["count"],_dic["video_id"]))

        set = get_object_or_404(Set, id=set_ids[0])
        project = get_object_or_404(Project, id=1)
        current_assignments = set.video.assignment_set.filter(project=project).all()
        context = RequestContext(request, {
            'current_set':multiple_assignment_data_set,
            'current': current_assignments,
            'current_annos': [a.annotator for a in current_assignments],
            'affiliations': Affiliation.objects.order_by('name').all(),
            'projects': Project.objects.order_by('id').all(),
            'current_project': project,
            'set_ids_str':set_ids_str,
        })

        return render_to_response(self.template_name, context=context)


    def filter_unassigned_list(self, video_list, assigned_video_list):
        unassigned_ids =[]
        for video_id in video_list :
            if video_id not in assigned_video_list :
                unassigned_ids.append(video_id)

        return unassigned_ids



class AssignMultipleVideoToAnnotators(UserAllowedMixin, View):
    """
    Endpoints used by the assignment modal found at /assignment/ for saving 
    multiple video assignment
    """
    def post(self, request):
        current_video_set = re.split(",", request.POST.get('set_ids_str'))
        project = get_object_or_404(Project, id=request.POST.get('project'))
        for set_id in current_video_set:
            set = get_object_or_404(Set, id=set_id)
            for anno_id in request.POST.getlist('anno[]'):
                Assignment(
                    annotator=FinprintUser.objects.get(id=anno_id),
                    video=set.video,
                    assigned_by=FinprintUser.objects.get(user_id=request.user),
                    project=project
                ).save()

        return JsonResponse({'status': 'ok'})

class RestrictFilterDropDown(UserAllowedMixin, View) :
    """
    Endpoints used by the auto assignment modal found at /assignment/ for restricting
    drop down of Reefs and Sets based on Trip selected
    """
    def post(self, request):

        post_dic = dict(request.POST)
        if 'trip' in post_dic :
            trip_id = dict(request.POST)['trip'][0]
        if 'reef[]' in post_dic:
            reef_ids = dict(request.POST)['reef[]']
           # reef_codes =""
        if 'trip' in post_dic and trip_id !='' and 'reef[]' not in post_dic:
            trip = Trip.objects.filter(id = trip_id).order_by('code').all().prefetch_related('set_set')
            sites = Site.objects.filter(location_id=trip[0].location_id).order_by('name').all().prefetch_related('reef_set')
        elif 'reef[]' in post_dic and trip_id !='':
            trip = Trip.objects.order_by('code').all().prefetch_related('set_set')
            sites = Site.objects.order_by('name').all().prefetch_related('reef_set')
        else :
            trip = Trip.objects.order_by('code').all().prefetch_related('set_set')
            sites = Site.objects.order_by('name').all().prefetch_related('reef_set')

        #find the code of each reef and remove those sets


        
        set_data = list(set(trip))[0].set_set
        print("set_group_name {}", str(set_data.instance))
        list_of_sets = []
        for s in set_data.all():
            list_of_sets.append({"id": s.id, "code": s.code, "group": str(set_data.instance)})
            print("set_id: {} set_name: {}", s.id, s.code)



        print("reef_data_group_name {}", str(set_data.instance.location))
        list_of_reefs=[]
        for s in sites:
           print("reef_set_group_name {}", str(s))
           for r in s.reef_set.all() :
             list_of_reefs.append({"reef_group": str(s), "id": r.id, "name": r.name})
             print("reef_set_id: {} reef_set_name: {}",r.id, r.name)

        if len(reef_ids)== 0 :
            return JsonResponse({'status': 'ok',"reefs":list_of_reefs, "sets":list_of_sets})
        else :
            return JsonResponse({'status': 'ok', "sets": list_of_sets})
