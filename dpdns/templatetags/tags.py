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

from django import template
import datetime

from django.urls import reverse

from DjangoPowerDNS import settings

register = template.Library()


def enabled_record_types():
    RECORD_TYPE_CHOICES = []
    for enabled_rr_type in settings.PDNS_ENABLED_RR_TYPES:
        RECORD_TYPE_CHOICES.append((enabled_rr_type, enabled_rr_type))

    return RECORD_TYPE_CHOICES


@register.simple_tag()
def api_url(url, domain, record=False):
    args = {'pk': domain}
    if record:
        args['id'] = 0

    return reverse(url, kwargs=args).replace("0", "<record-id>")


register.filter()
