from django.urls import path
from . import views

urlpatterns = [
    # Movie listings
    path('', views.MovieListView.as_view(), name='movie-list'),
    path('<uuid:id>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('now-showing/', views.NowShowingMoviesView.as_view(), name='now-showing'),
    path('coming-soon/', views.ComingSoonMoviesView.as_view(), name='coming-soon'),
    path('top-rated/', views.TopRatedMoviesView.as_view(), name='top-rated'),

    # Search and recommendations
    path('search/', views.movie_search, name='movie-search'),
    path('recommendations/', views.movie_recommendations, name='movie-recommendations'),
    path('sample/', views.sample_movies, name='sample-movies'),

    # Reviews
    path('<uuid:movie_id>/reviews/', views.MovieReviewListCreateView.as_view(), name='movie-reviews'),
    path('reviews/<int:pk>/', views.MovieReviewDetailView.as_view(), name='movie-review-detail'),

    # Wishlist
    path('wishlist/', views.MovieWishlistView.as_view(), name='movie-wishlist'),
    path('wishlist/<int:pk>/', views.MovieWishlistDetailView.as_view(), name='movie-wishlist-detail'),
    path('<uuid:movie_id>/toggle-wishlist/', views.toggle_wishlist, name='toggle-wishlist'),

    # Metadata
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('languages/', views.LanguageListView.as_view(), name='language-list'),
    path('formats/', views.MovieFormatListView.as_view(), name='format-list'),
]
