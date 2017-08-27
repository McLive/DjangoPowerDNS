from rest_framework import serializers

from dpdns.models import Records


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ('id', 'domain', 'name', 'type', 'content', 'ttl', 'prio')
        read_only_fields = ('id', 'domain')
