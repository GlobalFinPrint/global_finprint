# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from global_finprint.core.views import UrlRedirect

from global_finprint.trip.views import TripListView, TripCreateView, TripUpdateView, trip_detail
from global_finprint.bruv.views import SetListView, SetCreateView, SetUpdateView, set_detail, ObservationListView


urlpatterns = [
    #url(r"^$", TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r"^$", TripListView.as_view(), name="home"),

    url(r"^trips/$", TripListView.as_view(), name='trip_list'),

    url(r"^trips/create/$", TripCreateView.as_view(), name='trip_create'),
    url(r"^trips/(?P<pk>\d+)/$", TripUpdateView.as_view(), name='trip_update'),

    url(r"^trips/(?P<trip_pk>\d+)/sets/$", SetListView.as_view(), name='trip_set_list'),

    url(r"^api/trips/(?P<pk>\d+)/$", trip_detail, name='api_trip_detail'),
    url(r"^api/sets/(?P<pk>\d+)/$", set_detail, name='api_set_detail'),

    url(r"^sets/create/$", SetCreateView.as_view(), name='set_create'),
    url(r"^sets/(?P<pk>\d+)/$", SetUpdateView.as_view(), name='set_update'),

    url(r"^sets/(?P<set_pk>\d+)/observations/$", ObservationListView.as_view(), name='set_observations_list'),


    url(r"^about/$", TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Django Admin
    url(r"^admin/", include(admin.site.urls)),

    # User management
    #url(r"^users/", include("global_finprint.users.urls", namespace="users")),
    #url(r"^accounts/", include('allauth.urls')),
    url(r'^accounts/login/$', login, {'template_name': 'registration/login.html'}, name='finprint_login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logged_out.html'}, name='finprint_logout'),
    url(r'^accounts/profile/$', UrlRedirect.as_view()),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
