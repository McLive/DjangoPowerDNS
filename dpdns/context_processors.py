from DjangoPowerDNS import settings


def enabled_record_types(request):
    return {'enabled_record_types': settings.PDNS_ENABLED_RR_TYPES}
