# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.models import Site
from django.views.defaults import bad_request, permission_denied, page_not_found, server_error

from global_finprint.core.views import UrlRedirect, UserInfoView
from global_finprint.core.forms import FinprintAuthenticationForm
from global_finprint.bruv.views.benthic_category import BenthicCategoryView


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name='pages/home.html'), name="home"),

    url(r"^admin/", include(admin.site.urls)),

    url(r'^trips/', include('global_finprint.trip.urls')),
    url(r'^reports/', include('global_finprint.report.urls')),
    url(r'^api/', include('global_finprint.api.urls')),
    url(r"^assignment/", include('global_finprint.annotation.urls.assignment')),

    url(r"^substrate/$", BenthicCategoryView.as_view(), name="ajax_substrate"),

    url(r"^about/$", TemplateView.as_view(template_name='pages/about.html'), name="about"),

    url(r"^user/info/(?P<id>\d+)$", UserInfoView.as_view(), name="user_info_view"),

    # User management
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', login, {'template_name': 'registration/login.html',
                                      'authentication_form': FinprintAuthenticationForm}, name='finprint_login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/logged_out.html'}, name='finprint_logout'),
    url(r'^accounts/password_change/$', login_required(password_change),
        {'password_change_form': PasswordChangeForm},
        name='password_change'),
    url(r'^accounts/password_change_done/$', login_required(password_change_done),
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
    url(r'^accounts/profile/$', UrlRedirect.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# remove confusing 'Sites' from admin page:
admin.site.unregister(Site)

# Admin site title
admin.site.site_header = 'Global FinPrint data administration'

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', bad_request),
        url(r'^403/$', permission_denied),
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
