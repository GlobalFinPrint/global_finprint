from datetime import date, timedelta
from builtins import set as Set_util
import numpy as np
import re as re
from builtins import set as set_utils
from django.views.generic import View, ListView

from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.http.response import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ...core.mixins import UserAllowedMixin
from ...trip.models import Trip
from ...bruv.models import Set
from ...habitat.models import Location, Site
from ...core.models import Affiliation, FinprintUser
from ..models.video import Assignment, Video, AnnotationState
from ..models.project import Project
from ..models.custommodels import MultiVideoAssignmentData
from ..models.observation import Measurable, Event, MasterEvent, EventMeasurable, MasterEventMeasurable


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
        assigned_annotators_list = video.annotators_assigned(project)
        avail = [a for a in annotators if a not in assigned_annotators_list]
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
        post_dic = dict(request.POST)

        trip_id = request.POST.get('trip')
        aff_id = request.POST.get('affiliation')
        num = int(request.POST.get('num'))
        include_leads = bool(request.POST.get('include_leads', False))
        project = get_object_or_404(Project, id=request.POST.get('project'))

        if aff_id :
           annotators = FinprintUser.objects.filter(affiliation_id=aff_id, user__is_active=True).all()
        else :
           annotators = FinprintUser.objects.filter(user__is_active=True).all()

        if not include_leads:
            annotators = list(a for a in annotators if not a.is_lead())

        video_count = 0
        assigned_count = 0
        new_count = 0
        videos = None

        if trip_id != '':
            videos = Video.objects.filter(set__trip_id=trip_id).exclude(files__isnull=True).all()

        if 'auto-reef[]' in post_dic:
            reef_ids = post_dic['auto-reef[]']
            if trip_id != '':
                videos = videos.filter(set__reef_habitat__reef_id__in=reef_ids)
            elif len(reef_ids) > 0:
                videos = Video.objects.filter(set__reef_habitat__reef_id__in=reef_ids).exclude(
                    files__isnull=True).all()

        if 'auto-set[]' in post_dic:
            set_ids = post_dic['auto-set[]']
            if trip_id != '' or ('auto-reef[]' in post_dic and len(post_dic['auto-reef[]']) > 0):
                videos = videos.filter(set__code__in=set_ids).exclude(files__isnull=True).all()
            elif len(set_ids) > 0:
                videos = Video.objects.filter(set__code__in=set_ids).exclude(files__isnull=True).all()
        if videos != None:
            for video in videos:
                video_count += 1
                new_count += self.assign_video(annotators, video, num, project)
                assigned_count += len(video.annotators_assigned(project))
        else :
            video_count = 0
            new_count = 0
            assigned_count = 0

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

class VideoCountForAutoAssignView(UserAllowedMixin, View):
    """
        View to handle auto-assignment functionality found at /assignment/
        """
    def return_count_of_assign_video(self, annotators, video, num, project):
        """
        Assign a video to a number of annotators
        :param annotators: list of annotator objects
        :param video: video object
        :param num: integer denoting how many annotators should have this video assigned
        :param project: project object
        :return:
        """
        assigned_annotators_list = video.annotators_assigned(project)
        avail = [a for a in annotators if a not in assigned_annotators_list ]
        assign_count = 0
        assigned_annotators_num = len(video.annotators_assigned(project))
        num_of_annotators = len(annotators)

        if num_of_annotators > 0 :
            count1 = num - assigned_annotators_num
            count2 =  len(avail)
            if count2 > 0 and count1 > 0:
             if count1 <= count2 :
                assign_count = count1
             else :
                assign_count = count2

        return assign_count

    def post(self, request):
        """
        Endpoint used by automatic assignment modal to return counts of videos after filter applied
        :param request:
        :return:
        """
        post_dic = dict(request.POST)

        trip_id = request.POST.get('trip')
        aff_id = request.POST.get('affiliation')
        num = int(request.POST.get('num'))
        include_leads = bool(request.POST.get('include_leads', False))
        project = get_object_or_404(Project, id=request.POST.get('project'))

        if aff_id != '':
            annotators = FinprintUser.objects.filter(affiliation_id=aff_id, user__is_active=True).all()
        else:
            annotators = FinprintUser.objects.filter(user__is_active=True).all()

        if not include_leads:
            annotators = list(a for a in annotators if not a.is_lead())

        video_count = 0
        assigned_count = 0
        new_count = 0
        videos = None

        if trip_id != '':
            videos = Video.objects.filter(set__trip_id=trip_id).exclude(files__isnull=True).all()

        if 'auto-reef[]' in post_dic:
            reef_ids = post_dic['auto-reef[]']
            if trip_id != '':
                videos = videos.filter(set__reef_habitat__reef_id__in=reef_ids)
            elif len(reef_ids) > 0:
                videos = Video.objects.filter(set__reef_habitat__reef_id__in=reef_ids).exclude(
                    files__isnull=True).all()

        if 'auto-set[]' in post_dic:
            set_ids = post_dic['auto-set[]']
            if trip_id != '' or ('auto-reef[]' in post_dic and len(post_dic['auto-reef[]']) > 0):
                videos = videos.filter(set__code__in=set_ids).exclude(files__isnull=True).all()
            elif len(set_ids) > 0:
                videos = Video.objects.filter(set__code__in=set_ids).exclude(files__isnull=True).all()

        if videos is not None :
            for video in videos:
                video_count += 1
                new_count += self.return_count_of_assign_video(annotators, video, num, project)
                assigned_count += len(video.annotators_assigned(project))
        else :
            video_count = 0
            new_count = 0
            assigned_count = 0

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


class TotalVideoCountForAutoAssignment(UserAllowedMixin, View):
    """
        View to handle auto-assignment functionality found at /assignment/
        """

    def post(self, request):
        """
        Endpoint used by automatic assignment modal to return counts of videos after filter applied
        :param request:
        :return:
        """
        post_dic = dict(request.POST)
        trip_id = request.POST.get('trip')

        videos = None

        if trip_id!='' :
            videos = Video.objects.filter(set__trip_id=trip_id).exclude(files__isnull=True).all()

        if 'auto-reef[]' in post_dic:
            reef_ids = post_dic['auto-reef[]']
            if trip_id!='':
                videos = videos.filter(set__reef_habitat__reef_id__in=reef_ids)
            elif len(reef_ids) > 0 :
                videos = Video.objects.filter(set__reef_habitat__reef_id__in=reef_ids).exclude(
                    files__isnull=True).all()

        if 'auto-set[]' in post_dic :
            set_ids = post_dic['auto-set[]']
            if trip_id!='' or ('auto-reef[]' in post_dic and len(post_dic['auto-reef[]']) > 0):
                videos = videos.filter(set__code__in=set_ids).exclude(files__isnull=True).all()
            elif len(set_ids) > 0 :
                videos = Video.objects.filter(set__code__in=set_ids).exclude(files__isnull=True).all()

        if videos is not None and len(videos)!=0 :
            video_count = len(videos)
        else :
            video_count = 0


        return JsonResponse(
            {
                'status': 'ok',
                'video_count': video_count
            }
        )

class AssignmentListView(UserAllowedMixin, View):
    """
    View to handle the assignment screen found at /assignment/
    """
    template_name = 'pages/annotation/assignment_list.html'

    def get(self, request):
        context = {
            'locations': Location.objects.order_by('name').all().prefetch_related('trip_set'),
            'trips': Trip.objects.order_by('code').all().prefetch_related('set_set'),
            'sites': Site.objects.order_by('name').all().prefetch_related('reef_set'),
            'affils': Affiliation.objects.order_by('name').all().prefetch_related('finprintuser_set'),
            'statuses': AnnotationState.objects.all(),
            'projects': Project.objects.order_by('id').all()
        }
        return render(request, self.template_name, context=context)


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

        context = {'assignments': sorted(query, key=lambda a: str(a.set())),
                                           'unassigned': sorted(unassigned, key=lambda s: str(s))}
        return render(request, self.template_name, context=context)


class AssignmentModalBodyView(UserAllowedMixin, View):
    """
    Endpoints used by the assignment modal found at /assignment/
    """
    template_name = 'pages/annotation/assignment_modal_body.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        project = get_object_or_404(Project, id=request.GET.get('project_id', 1))
        current_assignments = set.video.assignment_set.filter(project=project).all()
        context = {
            'set': set,
            'current': current_assignments,
            'current_annos': [a.annotator for a in current_assignments],
            'affiliations': Affiliation.objects.order_by('name').all(),
            'projects': Project.objects.order_by('id').all(),
            'current_project': project,
        }
        return render(request, self.template_name, context=context)

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
        context = {
            'assignment': assignment
        }
        return render(request, self.template_name, context=context)

    def post(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        # assign.remove() clears unfinished annotations and then deletes self
        assignment.remove()
        return JsonResponse({'status': 'ok'})


class ManageAssignmentView(UserAllowedMixin, View):
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


class ObservationListView(UserAllowedMixin, ListView):
    """
    View for observation list by annotator found at /assignment/review/<assignment_id>
    """
    template_name = 'pages/observations/annotator_review.html'
    model = Assignment
    context_object_name = 'observations'

    def get_queryset(self):
        return sorted(get_object_or_404(Assignment, pk=self.kwargs['assignment_id']).observation_set.all(),
                                        key=lambda o: o.initial_observation_time(),
                                        reverse=True)

    def get_context_data(self, **kwargs):
        context = super(ObservationListView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['observations'], 50)
        try:
            context['observations'] = paginator.page(page)
        except PageNotAnInteger:
            context['observations'] = paginator.page(1)
        except EmptyPage:
            context['observations'] = paginator.page(paginator.num_pages)

        assignment = get_object_or_404(Assignment, pk=self.kwargs['assignment_id'])
        context['state_list'] = AnnotationState.objects.all()
        context['assignment'] = assignment
        context['trip'] = assignment.video.set.trip
        context['set'] = assignment.video.set
        context['for'] = ' by {}'.format(assignment.annotator.user.get_full_name())
        return context


class EditMeasurablesInline(UserAllowedMixin, View):
    """
    Endpoints for the measurables inline editing on obs review pages
    """

    def get(self, request, evt_id, **kwargs):
        event = MasterEvent.objects.get(id=evt_id) if ('is-master' in request.GET) else Event.objects.get(id=evt_id)
        return JsonResponse({
            'measurables': list({'name': m.name, 'id': m.id}
                                for m in Measurable.objects.filter(active=True)),
            'event_measurables': list({'measurable': m.measurable_id, 'value': m.value, 'id': m.id}
                                      for m in event.active_measurables()),
        })

    def post(self, request, evt_id, **kwargs):
        event = MasterEvent.objects.get(id=evt_id) if ('is-master' in request.POST) else Event.objects.get(id=evt_id)
        event.measurables.clear()
        measurables = request.POST.getlist('measurables[]', [])
        values = request.POST.getlist('values[]', [])
        print(list(zip(measurables, values)))
        for m, v in zip(measurables, values):
            if 'is-master' in request.POST:
                MasterEventMeasurable(master_event_id=event.id, measurable_id=m, value=v).save()
            else:
                EventMeasurable(event_id=event.id, measurable_id=m, value=v).save()
        event.refresh_from_db()
        return JsonResponse({'measurables': [{'name': str(em), 'id': em.id} for em in event.active_measurables()]})


class MeasurableDelete(UserAllowedMixin, View):
    """
    Endpoint to delete measurables
    """

    def post(self, request, measurable_id, **kwargs):
        if 'is-master' in request.POST:
            measurable = MasterEventMeasurable.objects.get(id=measurable_id)
            event = measurable.master_event
        else:
            measurable = EventMeasurable.objects.get(id=measurable_id)
            event = measurable.event
        measurable.delete()
        return JsonResponse({'measurables': [{'name': str(em), 'id': em.id} for em in event.active_measurables()]})


# todo:  rename this as "Modal" from "Model"  and re-format to minimal pep-8 standard.
class AssignMultipleVideosModel(UserAllowedMixin, View):
    """
    Endpoints used by the assignment modal found at /assignment/
    """
    template_name = 'pages/annotation/multiple_assignment_list_modal.html'

    def post(self, request):
        set_ids = list(Set_util(np.asarray(dict(request.POST)['set_ids[]'])))
        video_list = list(Set_util(np.asarray(dict(request.POST)['video_ids[]'])))

        #only gives assigned list not the unassigned
        assignment_list = Assignment.get_all_assignments(video_list)
        multiple_assignment_data_dic = {}
        project_list = []
        assigned_video_list=[]
        multiple_assignment_data_set = []
        total_count = 0

        #creating a dictionary wid name_of_video ,video_id and number_of_user_assigned for model
        for assignment in assignment_list :
            project_list.append(assignment.project_id)
            if assignment.video_id not in multiple_assignment_data_dic  :
                total_count = total_count + 1
                assigned_video_list.append(assignment.video_id)
                multiple_assignment_data_dic[assignment.video_id] = {"name": str(assignment.video), "count": 1, "video_id":assignment.video_id, "set_id":assignment.video.set.id}

            else :
                new_count = multiple_assignment_data_dic.get(assignment.video_id)["count"] +1
                multiple_assignment_data_dic[assignment.video_id] = {"name": str(assignment.video), "count": new_count, "video_id":assignment.video_id, "set_id":assignment.video.set.id}


        unassigned_list = self.filter_unassigned_list(video_list,assigned_video_list)

        unassigned_set = Set.objects.annotate(Count('video__assignment')) \
                                .filter(video__assignment__count=0) \
                                .filter(video_id__in = unassigned_list ) \
                                .exclude(video__files=None)

        # updating dictionary wid name_of_video ,video_id and number_of_user_assigned for model
        for unassigned in unassigned_set:
            total_count = total_count + 1
            multiple_assignment_data_dic[unassigned.video_id] = {"name": str(unassigned.video), "count": 0,
                                                                 "video_id": unassigned.video_id, "set_id":unassigned.video.set.id}
        set_ids_str = ','.join(str(x) for x in set_ids)
        for video_id in video_list :
            _dic = multiple_assignment_data_dic[int(video_id)]
            multiple_assignment_data_set.append(MultiVideoAssignmentData(_dic["name"],_dic["count"],_dic["video_id"], _dic["set_id"]))

        set = get_object_or_404(Set, id=set_ids[0])
        project = get_object_or_404(Project, id=1)
        current_assignments = set.video.assignment_set.filter(project=project).all()
        context = {
            'current_set':multiple_assignment_data_set,
            'current': current_assignments,
            'current_annos': [a.annotator for a in current_assignments],
            'affiliations': Affiliation.objects.order_by('name').all(),
            'projects': Project.objects.order_by('id').all(),
            'current_project': project,
            'set_ids_str':set_ids_str,
            'total_count':total_count,
        }

        return render(request, self.template_name, context=context)

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
        list_of_sets = []
        list_of_reefs = []

        if 'trip' in post_dic :
            trip_id = dict(request.POST)['trip'][0]
        if 'auto-reef[]' in post_dic:
            reef_ids = dict(request.POST)['auto-reef[]']

        #if trip change
        if 'trip' in post_dic and trip_id !='' and 'auto-reef[]' not in post_dic:
            trip = Trip.objects.filter(id = trip_id).order_by('code').all().prefetch_related('set_set')
            sites = Site.objects.filter(location_id=trip[0].location_id).order_by('name').all().prefetch_related('reef_set')
            # find the code of each reef and remove those sets
            set_data = list(set(trip))[0].set_set
            for s in set_data.all():
                list_of_sets.append({"id": s.id, "code": s.code, "group": str(set_data.instance)})

            for s in sites:
                for r in s.reef_set.all():
                    list_of_reefs.append({"reef_group": str(s), "id": r.id, "name": r.name})
        # if reef changes
        elif 'auto-reef[]' in post_dic:
            if 'trip' in post_dic and trip_id !='' :
                sets = Set.objects.filter(trip_id=trip_id).filter(reef_habitat__reef_id__in=reef_ids)
            else :
                sets = Set.objects.filter(reef_habitat__reef_id__in=reef_ids)

            for each_set in list(set_utils(sets)) :
                list_of_sets.append({"id": each_set.id, "code": each_set.code, "group": str(each_set.trip)})
        else :
            trip = Trip.objects.order_by('code').all().prefetch_related('set_set')
            sites = Site.objects.order_by('name').all().prefetch_related('reef_set')
            for trip_data in list(set(trip)) :
                set_data = trip_data.set_set
                for s in set_data.all():
                    list_of_sets.append({"id": s.id, "code": s.code, "group": str(set_data.instance)})

            for s in sites:
                for r in s.reef_set.all():
                    list_of_reefs.append({"reef_group": str(s), "id": r.id, "name": r.name})

        if 'auto-reef[]' not in post_dic :
            return JsonResponse({'status': 'ok',"reefs":list_of_reefs, "sets":list_of_sets})
        else :
            return JsonResponse({'status': 'ok', "sets": list_of_sets})

class AssignedAnnotatorPopup(UserAllowedMixin, View):
    """
    Endpoints used by the multiple assignment modal found at /assignment/
    """
    template_name = 'pages/annotation/assignment_annotator_popup.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        project = get_object_or_404(Project, id=request.GET.get('project_id', 1))
        current_assignments = set.video.assignment_set.filter(project=project).all()
        context = {
            'set': set,
            'current': current_assignments,
        }

        return render(request, self.template_name, context=context)
