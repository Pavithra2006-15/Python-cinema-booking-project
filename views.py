from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Movie, Genre, Language, MovieReview, MovieFormat, MovieWishlist
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, GenreSerializer,
    LanguageSerializer, MovieReviewSerializer, MovieFormatSerializer,
    MovieWishlistSerializer, MovieSearchSerializer
)
from .filters import MovieFilter


class MovieListView(generics.ListAPIView):
    """List all movies with filtering and search"""

    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'director', 'cast']
    ordering_fields = ['release_date', 'title', 'average_rating']
    ordering = ['-release_date']


class MovieDetailView(generics.RetrieveAPIView):
    """Get movie details"""

    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


class NowShowingMoviesView(generics.ListAPIView):
    """List movies currently showing"""

    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'director']
    ordering_fields = ['release_date', 'title', 'average_rating']
    ordering = ['-average_rating']

    def get_queryset(self):
        return Movie.objects.filter(
            is_active=True,
            status='now_showing'
        )


class ComingSoonMoviesView(generics.ListAPIView):
    """List upcoming movies"""

    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'director']
    ordering_fields = ['release_date', 'title']
    ordering = ['release_date']

    def get_queryset(self):
        return Movie.objects.filter(
            is_active=True,
            status='coming_soon'
        )


class TopRatedMoviesView(generics.ListAPIView):
    """List top rated movies"""

    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'director']

    def get_queryset(self):
        return Movie.objects.filter(
            is_active=True,
            average_rating__gte=4.0
        ).order_by('-average_rating', '-total_reviews')


class GenreListView(generics.ListAPIView):
    """List all genres"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]


class LanguageListView(generics.ListAPIView):
    """List all languages"""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.AllowAny]


class MovieFormatListView(generics.ListAPIView):
    """List all movie formats"""

    queryset = MovieFormat.objects.all()
    serializer_class = MovieFormatSerializer
    permission_classes = [permissions.AllowAny]


class MovieReviewListCreateView(generics.ListCreateAPIView):
    """List and create movie reviews"""

    serializer_class = MovieReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return MovieReview.objects.filter(movie_id=movie_id).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['movie'] = Movie.objects.get(id=self.kwargs['movie_id'])
        return context

    def perform_create(self, serializer):
        movie = Movie.objects.get(id=self.kwargs['movie_id'])
        review = serializer.save()

        # Update movie average rating
        avg_rating = MovieReview.objects.filter(movie=movie).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']

        movie.average_rating = round(avg_rating, 1) if avg_rating else 0.0
        movie.total_reviews = MovieReview.objects.filter(movie=movie).count()
        movie.save()


class MovieReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a movie review"""

    serializer_class = MovieReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MovieReview.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        review = serializer.save()

        # Update movie average rating
        movie = review.movie
        avg_rating = MovieReview.objects.filter(movie=movie).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']

        movie.average_rating = round(avg_rating, 1) if avg_rating else 0.0
        movie.save()

    def perform_destroy(self, instance):
        movie = instance.movie
        instance.delete()

        # Update movie average rating
        avg_rating = MovieReview.objects.filter(movie=movie).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']

        movie.average_rating = round(avg_rating, 1) if avg_rating else 0.0
        movie.total_reviews = MovieReview.objects.filter(movie=movie).count()
        movie.save()


class MovieWishlistView(generics.ListCreateAPIView):
    """List and add movies to wishlist"""

    serializer_class = MovieWishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MovieWishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieWishlistDetailView(generics.DestroyAPIView):
    """Remove movie from wishlist"""

    serializer_class = MovieWishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MovieWishlist.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_wishlist(request, movie_id):
    """Toggle movie in user's wishlist"""

    try:
        movie = Movie.objects.get(id=movie_id, is_active=True)
        wishlist_item, created = MovieWishlist.objects.get_or_create(
            user=request.user,
            movie=movie
        )

        if not created:
            wishlist_item.delete()
            return Response({
                'message': 'Movie removed from wishlist',
                'is_wishlisted': False
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Movie added to wishlist',
            'is_wishlisted': True
        }, status=status.HTTP_201_CREATED)

    except Movie.DoesNotExist:
        return Response({
            'error': 'Movie not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def movie_search(request):
    """Advanced movie search"""

    serializer = MovieSearchSerializer(data=request.query_params)
    if serializer.is_valid():
        data = serializer.validated_data
        queryset = Movie.objects.filter(is_active=True)

        # Apply filters
        if data.get('query'):
            queryset = queryset.filter(
                Q(title__icontains=data['query']) |
                Q(director__icontains=data['query']) |
                Q(cast__icontains=data['query'])
            )

        if data.get('genre'):
            queryset = queryset.filter(genres__name__icontains=data['genre'])

        if data.get('language'):
            queryset = queryset.filter(languages__name__icontains=data['language'])

        if data.get('status'):
            queryset = queryset.filter(status=data['status'])

        if data.get('certification'):
            queryset = queryset.filter(certification=data['certification'])

        if data.get('min_rating'):
            queryset = queryset.filter(average_rating__gte=data['min_rating'])

        # Apply sorting
        sort_by = data.get('sort_by', '-release_date')
        queryset = queryset.order_by(sort_by)

        # Remove duplicates
        queryset = queryset.distinct()

        # Paginate results
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)

        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            page = 1
            page_size = 20

        start = (page - 1) * page_size
        end = start + page_size

        movies = queryset[start:end]
        serializer = MovieListSerializer(movies, many=True, context={'request': request})

        return Response({
            'results': serializer.data,
            'count': queryset.count(),
            'page': page,
            'page_size': page_size,
            'total_pages': (queryset.count() + page_size - 1) // page_size
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def movie_recommendations(request):
    """Get movie recommendations based on user preferences"""

    if request.user.is_authenticated:
        # Get user's preferred genres
        user_genres = request.user.preferred_genres

        # Get user's wishlist and review history
        wishlisted_movies = MovieWishlist.objects.filter(user=request.user).values_list('movie', flat=True)
        reviewed_movies = MovieReview.objects.filter(user=request.user).values_list('movie', flat=True)

        # Exclude already wishlisted and reviewed movies
        excluded_movies = list(wishlisted_movies) + list(reviewed_movies)

        queryset = Movie.objects.filter(
            is_active=True,
            status='now_showing'
        ).exclude(id__in=excluded_movies)

        # Filter by user's preferred genres if available
        if user_genres:
            queryset = queryset.filter(genres__name__in=user_genres)

        # Order by rating and popularity
        queryset = queryset.order_by('-average_rating', '-total_reviews').distinct()[:10]
    else:
        # For anonymous users, show top rated movies
        queryset = Movie.objects.filter(
            is_active=True,
            status='now_showing',
            average_rating__gte=4.0
        ).order_by('-average_rating', '-total_reviews')[:10]

    serializer = MovieListSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def sample_movies(request):
    """Get sample movie data for testing"""
    from .sample_data import SAMPLE_MOVIES

    return Response({
        'count': len(SAMPLE_MOVIES),
        'results': SAMPLE_MOVIES
    }, status=status.HTTP_200_OK)
