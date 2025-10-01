import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter('title', lookup_expr='icontains')
    author = django_filters.CharFilter('author', lookup_expr='icontains')
    publication_year_above = django_filters.NumberFilter('publication_year', lookup_expr='gte')
    publication_year_below = django_filters.NumberFilter('publication_year', lookup_expr='lte')

    class Meta:
        model= Book
        fields = ['author', 'title']