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
