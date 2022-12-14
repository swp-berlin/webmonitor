from rest_framework import serializers

from swp.api.serializers.thinktankfilter import ThinktankFilterSerializer
from swp.models import Monitor

from .fields import RecipientsField


class MonitorSerializer(serializers.ModelSerializer):
    recipient_count = serializers.IntegerField(read_only=True)
    publication_count = serializers.IntegerField(read_only=True)
    new_publication_count = serializers.IntegerField(read_only=True)

    recipients = RecipientsField()
    filters = ThinktankFilterSerializer(source='thinktank_filters', many=True, read_only=True)

    class Meta:
        model = Monitor
        fields = [
            'id',
            'name',
            'description',
            'last_sent',
            'interval',
            'recipient_count',
            'publication_count',
            'new_publication_count',
            'last_publication_count_update',
            'created',
            'recipients',
            'zotero_keys',
            'filters',
            'is_active',
        ]


class MonitorDetailSerializer(MonitorSerializer):
    transferred_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Monitor
        fields = [
            *MonitorSerializer.Meta.fields,
            'transferred_count',
        ]
