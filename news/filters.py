import django_filters
from django_filters import FilterSet
from .models import Post, Category


class PostFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    categoryType = django_filters.ChoiceFilter(choices=Post.CATEGORY_CHOICES)
    dateCreation = django_filters.DateFilter(field_name='dateCreation', lookup_expr='gte', label='Date (after)')

    class Meta:
        model = Post

        fields = {
             'title': [ 'iexact'],
             'categoryType': ['exact'],
             'dateCreation': ['gte', 'lte', 'exact'],
    }