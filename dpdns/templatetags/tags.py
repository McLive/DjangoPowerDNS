from django import template
import datetime

from DjangoPowerDNS import settings

register = template.Library()


def enabled_record_types():
    RECORD_TYPE_CHOICES = []
    for enabled_rr_type in settings.PDNS_ENABLED_RR_TYPES:
        RECORD_TYPE_CHOICES.append((enabled_rr_type, enabled_rr_type))

    return RECORD_TYPE_CHOICES


register.filter()
