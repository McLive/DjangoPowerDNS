"""DjangoPowerDNS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import dpdns.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^login/$', dpdns.views.login, name='login'),
    url(r'^logout/$', dpdns.views.logout, name='logout'),

    url(r'^domains/$', dpdns.views.domains, name='domains'),
    url(r'^domain/add$', dpdns.views.domain_add, name='domain-add'),

    url(r'^domain/(?P<id>[0-9]+)/json/get-records$', dpdns.views.domain_json_get_records, name='domain-json-get-records'),
    url(r'^domain/(?P<id>[0-9]+)/json/update-record$', dpdns.views.domain_json_update_record, name='domain-json-update-record'),
    url(r'^domain/(?P<id>[0-9]+)/json/delete-record$', dpdns.views.domain_json_delete_record, name='domain-json-delete-record'),

    url(r'^domain/(?P<id>[0-9]+)/users$', dpdns.views.domain_users, name='domain-users'),
    url(r'^domain/(?P<id>[0-9]+)/user/add$', dpdns.views.domain_user_add, name='domain-user-add'),

    url(r'^domain/(?P<id>[0-9]+)$', dpdns.views.domain, name='domain'),


    url(r'^api/domain/(?P<pk>[0-9]+)/get-records$', dpdns.views.api_get_records, name='api-get-records'),
    url(r'^api/domain/(?P<pk>[0-9]+)/record/(?P<id>[0-9]+)$', dpdns.views.api_record, name='api-record'),

    url(r'^$', dpdns.views.index, name='index'),
]
