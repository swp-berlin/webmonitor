from django.db import transaction
from rest_framework import serializers

from swp.api.serializers.fields import MonitorField
from swp.api.serializers.publicationfilter import PublicationFilterSerializer
from swp.models import Publication, PublicationFilter, ThinktankFilter
from swp.models.publicationfilter import as_query
from swp.models.thinktankfilter import as_query as as_thinktank_filter_query


class ThinktankFilterSerializer(serializers.ModelSerializer):
    filters = PublicationFilterSerializer(source='publication_filters', many=True, required=False)
    publication_count = serializers.IntegerField(read_only=True)
    new_publication_count = serializers.IntegerField(read_only=True)
    monitor = MonitorField(read_only=True)

    class Meta:
        model = ThinktankFilter
        fields = [
            'id',
            'name',
            'monitor',
            'thinktank',
            'filters',
            'publication_count',
            'new_publication_count',
            'last_publication_count_update',
        ]

    @transaction.atomic
    def create(self, validated_data):
        publication_filters = validated_data.pop('publication_filters', [])

        thinktank_filter = super().create(validated_data)
        self.create_publication_filters(thinktank_filter, publication_filters)

        return thinktank_filter

    def create_publication_filters(self, thinktank_filter, publication_filters):
        PublicationFilter.objects.bulk_create([
            PublicationFilter(thinktank_filter=thinktank_filter, **filter) for filter in publication_filters
        ])

    @transaction.atomic
    def update(self, instance, validated_data):
        publication_filters = validated_data.pop('publication_filters', [])

        thinktank_filter = super().update(instance, validated_data)
        self.update_publication_filters(instance, publication_filters)

        return thinktank_filter

    def update_publication_filters(self, thinktank_filter, publication_filters):
        ids = [filter.get('id') for filter in publication_filters if filter.get('id')]

        PublicationFilter.objects.filter(thinktank_filter=thinktank_filter).exclude(pk__in=ids).delete()

        for filter in publication_filters:
            id = filter.get('id')

            if id:
                PublicationFilter.objects.filter(thinktank_filter=thinktank_filter, pk=id).update(**filter)
            else:
                PublicationFilter.objects.create(thinktank_filter=thinktank_filter, **filter)

    def preview(self):
        thinktank = self.validated_data.get('thinktank')
        publication_filters = self.validated_data.get('publication_filters', [])
        queries = [
            as_query(
                publication_filter.get('field'),
                publication_filter.get('comparator'),
                publication_filter.get('values'),
            )
            for publication_filter in publication_filters
        ]

        query = as_thinktank_filter_query(thinktank, queries)

        return Publication.objects.active().filter(query)
