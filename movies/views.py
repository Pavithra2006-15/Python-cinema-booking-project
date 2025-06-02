from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import date
from .models import Movie, Showtime


class HomeView(ListView):
    model = Movie
    template_name = 'movies/home.html'
    context_object_name = 'movies'
    paginate_by = 6

    def get_queryset(self):
        return Movie.objects.filter(is_active=True).order_by('-release_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_movies'] = Movie.objects.filter(
            is_active=True,
            release_date__lte=date.today()
        ).order_by('-release_date')[:3]
        return context


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        queryset = Movie.objects.filter(is_active=True)

        # Filter by genre
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset.order_by('-release_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Movie.GENRE_CHOICES
        context['current_genre'] = self.request.GET.get('genre', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get upcoming showtimes for this movie
        context['showtimes'] = Showtime.objects.filter(
            movie=self.object,
            is_active=True,
            show_date__gte=date.today()
        ).order_by('show_date', 'show_time')[:10]
        return context


class ShowtimeListView(ListView):
    model = Showtime
    template_name = 'movies/showtime_list.html'
    context_object_name = 'showtimes'

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Showtime.objects.filter(
            movie_id=movie_id,
            is_active=True,
            show_date__gte=date.today()
        ).order_by('show_date', 'show_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, id=self.kwargs['movie_id'])
        return context
