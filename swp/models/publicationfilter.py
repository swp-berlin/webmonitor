from django.db import models
from django.utils.translation import gettext_lazy as _

from swp.models.choices import Comparator, DataResolverKey
from swp.models.fields import ChoiceField


class PublicationFilter(models.Model):
    FILTERS = {
        Comparator.CONTAINS: 'icontains',
        Comparator.STARTS_WITH: 'istartswith',
        Comparator.ENDS_WITH: 'iendswith'
    }

    thinktank_filter = models.ForeignKey(
        'swp.ThinktankFilter',
        on_delete=models.CASCADE,
        related_name='publication_filters',
        verbose_name=_('think tank filter'),

    )

    field = ChoiceField(_('field'), choices=DataResolverKey.choices)
    comparator = ChoiceField(_('comparator'), choices=Comparator.choices)
    value = models.CharField(_('value'), max_length=255)

    class Meta:
        verbose_name = _('publication filter')
        verbose_name_plural = _('publication filters')

    def __str__(self):
        return f'{self.field} {self.comparator} "{self.value}"'

    @property
    def as_query(self):
        field = self.field

        if field == 'author':
            field = 'authors'

        return models.Q(**{f'{field}__{self.FILTERS[self.comparator]}': self.value})