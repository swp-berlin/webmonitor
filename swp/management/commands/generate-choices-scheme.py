from django.utils import translation

from swp.management.scheme import GenerateSchemeCommand
from swp.models.choices import (
    Comparator,
    DataResolverKey,
    FilterField,
    Interval,
    ListResolverType,
    PaginatorType,
    ResolverType,
    UniqueKey,
)


class Command(GenerateSchemeCommand):
    PROPERTIES = [
        ('interval', Interval.choices),
        ('ResolverType', ResolverType.choices),
        ('ListResolverType', ListResolverType.choices),
        ('DataResolverKey', DataResolverKey.choices),
        ('UniqueKey', UniqueKey.choices),
        ('Comparator', Comparator.choices),
        ('PaginatorType', PaginatorType.choices),
        ('FilterField', FilterField.choices),
    ]

    filename = 'choices.json'

    @translation.override(None)
    def get_data(self, **options):
        return {
            prop: [
                {'value': value, 'label': f'{label}'}
                for value, label in choices
            ] for prop, choices in self.PROPERTIES
        }
