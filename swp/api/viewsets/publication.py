import django_filters as filters

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from elasticsearch_dsl import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated

from swp.api.router import default_router
from swp.api.serializers import PublicationSerializer, ResearchSerializer
from swp.documents import PublicationDocument
from swp.models import Monitor, Publication, ThinktankFilter
from swp.utils.translation import get_language


class CanResearch(BasePermission):

    def has_permission(self, request, view):
        return request.user.can_research


class PublicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class MonitorFilter(filters.ModelChoiceFilter):

    def filter(self, qs, monitor: Monitor):
        if monitor:
            return qs.filter(monitor.as_query)

        return qs


class ThinktankFilterFilter(filters.ModelChoiceFilter):

    def filter(self, qs, thinktankfilter: ThinktankFilter):
        if thinktankfilter:
            return qs.filter(thinktankfilter.as_query)

        return qs


class PublicationFilter(filters.FilterSet):
    monitor = MonitorFilter(label=_('Monitor'), queryset=Monitor.objects)
    thinktankfilter = ThinktankFilterFilter(label=_('Think Tank Filter'), queryset=ThinktankFilter.objects)
    since = filters.DateTimeFilter('last_access', 'gte')
    is_active = filters.BooleanFilter('thinktank__is_active')

    class Meta:
        model = Publication
        fields = [
            'thinktank_id',
            'monitor',
            'thinktankfilter',
            'since',
        ]


class ResearchFilter(filters.FilterSet):
    start_date = filters.DateFilter(label=_('Start Date'), required=False)
    end_date = filters.DateFilter(label=_('End Date'), required=False)
    query = filters.CharFilter(label=_('Query'), required=True)

    def filter_queryset(self, queryset, *, using=None):
        data = self.form.cleaned_data
        query = self.get_search_query(**data)

        return PublicationDocument.search(using=using).query(query).source(False)

    @staticmethod
    def get_result_queryset(search):
        return Publication.objects.filter(
            id__in=[result.meta.id for result in search],
        ).annotate(
            score=models.Case(
                *[models.When(id=result.meta.id, then=result.meta.score) for result in search],
                output_field=models.FloatField(default=0.),
            ),
        ).order_by(
            '-score',
        )

    def get_search_query(self, query, start_date=None, end_date=None):
        language = get_language(request=self.request)
        fields = PublicationDocument.get_search_fields(language)
        query = Q('simple_query_string', query=query, fields=fields)

        if start_date or end_date:
            created = {'time_zone': settings.TIME_ZONE}

            if start_date:
                created['gte'] = start_date

            if end_date:
                created['lte'] = end_date

            query &= Q('range', created=created)

        return query


@default_router.register('publication', basename='publication')
class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects
    filterset_class = PublicationFilter
    ordering = ['-last_access', '-created']
    pagination_class = PublicationPagination
    serializer_class = PublicationSerializer

    @action(
        detail=False,
        ordering=None,
        filterset_class=ResearchFilter,
        serializer_class=ResearchSerializer,
        permission_classes=[IsAuthenticated & CanResearch],
    )
    def research(self, request):
        return self.list(request)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'research':
            args = ResearchFilter.get_result_queryset(*args),

        return super(PublicationViewSet, self).get_serializer(*args, **kwargs)
