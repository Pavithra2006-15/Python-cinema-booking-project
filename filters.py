import django_filters
from .models import Movie, Genre, Language


class MovieFilter(django_filters.FilterSet):
    """Filter for movies"""
    
    title = django_filters.CharFilter(lookup_expr='icontains')
    director = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genres',
        queryset=Genre.objects.all(),
        to_field_name='name'
    )
    language = django_filters.ModelMultipleChoiceFilter(
        field_name='languages',
        queryset=Language.objects.all(),
        to_field_name='name'
    )
    certification = django_filters.ChoiceFilter(choices=Movie.CERTIFICATION_CHOICES)
    status = django_filters.ChoiceFilter(choices=Movie.MOVIE_STATUS_CHOICES)
    min_rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='lte')
    release_date_from = django_filters.DateFilter(field_name='release_date', lookup_expr='gte')
    release_date_to = django_filters.DateFilter(field_name='release_date', lookup_expr='lte')
    
    class Meta:
        model = Movie
        fields = [
            'title', 'director', 'genre', 'language', 'certification',
            'status', 'min_rating', 'max_rating', 'release_date_from',
            'release_date_to'
        ]
