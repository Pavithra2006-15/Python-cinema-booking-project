from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('<int:movie_id>/showtimes/', views.ShowtimeListView.as_view(), name='showtime_list'),
]
