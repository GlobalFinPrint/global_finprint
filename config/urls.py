# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout

from global_finprint.core.views import UrlRedirect
from global_finprint.trip.views import TripListView, trip_detail
from global_finprint.bruv.views import set_detail


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name='pages/home.html'), name="home"),

    # Django Admin
    url(r"^admin/", include(admin.site.urls)),
    url(r'^sets/', include('global_finprint.bruv.urls.sets')),
    url(r'^observations/', include('global_finprint.bruv.urls.observations')),
    url(r'^trips/', include('global_finprint.trip.urls')),
    url(r'^reports/', include('global_finprint.report.urls')),

    url(r"^api/trips/(?P<pk>\d+)/$", trip_detail, name='api_trip_detail'),
    url(r"^api/sets/(?P<pk>\d+)/$", set_detail, name='api_set_detail'),

    url(r"^about/$", TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # User management
    url(r'^accounts/login/$', login, {'template_name': 'registration/login.html'}, name='finprint_login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logged_out.html'}, name='finprint_logout'),
    url(r'^accounts/profile/$', UrlRedirect.as_view()),

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
