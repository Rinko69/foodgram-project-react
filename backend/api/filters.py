import django_filters as filters
from recipes.models import Tag


class TagFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    slug = filters.CharFilter(field_name='slug')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Tag
        fields = '__all__'
