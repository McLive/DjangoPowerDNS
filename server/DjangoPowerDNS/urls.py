# --
# DjangoPowerDNS - A PowerDNS web interface
# Copyright (C) 2017 McLive
# --
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU AFFERO General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# --

""""DjangoPowerDNS URL Configuration

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
    url(r'^domain/claim$', dpdns.views.domain_claim, name='domain-claim'),

    url(r'^domain/(?P<id>[0-9]+)/json/get-records$', dpdns.views.domain_json_get_records, name='domain-json-get-records'),
    url(r'^domain/(?P<id>[0-9]+)/json/update-record$', dpdns.views.domain_json_update_record, name='domain-json-update-record'),
    url(r'^domain/(?P<id>[0-9]+)/json/delete-record$', dpdns.views.domain_json_delete_record, name='domain-json-delete-record'),

    url(r'^domain/(?P<id>[0-9]+)/users$', dpdns.views.domain_users, name='domain-users'),
    url(r'^domain/(?P<id>[0-9]+)/user/add$', dpdns.views.domain_user_add, name='domain-user-add'),
    url(r'^domain/(?P<id>[0-9]+)/api$', dpdns.views.domain_api, name='domain-api'),
    url(r'^domain/(?P<id>[0-9]+)/delete$', dpdns.views.domain_delete, name='domain-delete'),

    url(r'^domain/(?P<id>[0-9]+)$', dpdns.views.domain, name='domain'),


    url(r'^api/domain/(?P<pk>[0-9]+)/get-records$', dpdns.views.api_get_records, name='api-get-records'),
    url(r'^api/domain/(?P<pk>[0-9]+)/record/(?P<id>[0-9]+)$', dpdns.views.api_record, name='api-record'),

    url(r'^$', dpdns.views.index, name='index'),
]
