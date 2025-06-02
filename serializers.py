from rest_framework import serializers
from .models import Movie, Genre, Language, MovieReview, MovieFormat, MovieWishlist


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model"""
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language model"""
    
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']


class MovieFormatSerializer(serializers.ModelSerializer):
    """Serializer for MovieFormat model"""
    
    class Meta:
        model = MovieFormat
        fields = ['id', 'name', 'description', 'additional_cost']


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for movie list view"""
    
    genres = GenreSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'poster', 'duration', 'duration_display',
            'release_date', 'genres', 'languages', 'certification',
            'status', 'average_rating', 'total_reviews', 'is_now_showing',
            'is_coming_soon'
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for movie detail view"""
    
    genres = GenreSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    is_wishlisted = serializers.SerializerMethodField()
    user_review = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'duration', 'duration_display',
            'release_date', 'end_date', 'poster', 'banner', 'trailer_url',
            'genres', 'languages', 'certification', 'status', 'director',
            'cast', 'producer', 'music_director', 'imdb_rating',
            'average_rating', 'total_reviews', 'is_now_showing',
            'is_coming_soon', 'is_wishlisted', 'user_review'
        ]
    
    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return MovieWishlist.objects.filter(user=request.user, movie=obj).exists()
        return False
    
    def get_user_review(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                review = MovieReview.objects.get(user=request.user, movie=obj)
                return MovieReviewSerializer(review).data
            except MovieReview.DoesNotExist:
                return None
        return None


class MovieReviewSerializer(serializers.ModelSerializer):
    """Serializer for movie reviews"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = MovieReview
        fields = [
            'id', 'rating', 'review_text', 'is_verified_booking',
            'user_name', 'user_email', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_name', 'user_email', 'is_verified_booking', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['movie'] = self.context['movie']
        
        # Check if user has booked this movie
        from apps.bookings.models import Booking
        has_booking = Booking.objects.filter(
            user=validated_data['user'],
            show__movie=validated_data['movie'],
            status='confirmed'
        ).exists()
        validated_data['is_verified_booking'] = has_booking
        
        return super().create(validated_data)


class MovieWishlistSerializer(serializers.ModelSerializer):
    """Serializer for movie wishlist"""
    
    movie = MovieListSerializer(read_only=True)
    
    class Meta:
        model = MovieWishlist
        fields = ['id', 'movie', 'created_at']
        read_only_fields = ['id', 'created_at']


class MovieSearchSerializer(serializers.Serializer):
    """Serializer for movie search parameters"""
    
    query = serializers.CharField(required=False, allow_blank=True)
    genre = serializers.CharField(required=False, allow_blank=True)
    language = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=Movie.MOVIE_STATUS_CHOICES,
        required=False,
        allow_blank=True
    )
    certification = serializers.ChoiceField(
        choices=Movie.CERTIFICATION_CHOICES,
        required=False,
        allow_blank=True
    )
    min_rating = serializers.FloatField(required=False, min_value=0.0, max_value=5.0)
    sort_by = serializers.ChoiceField(
        choices=[
            ('release_date', 'Release Date'),
            ('-release_date', 'Release Date (Desc)'),
            ('title', 'Title'),
            ('-title', 'Title (Desc)'),
            ('average_rating', 'Rating'),
            ('-average_rating', 'Rating (Desc)'),
        ],
        required=False,
        default='-release_date'
    )
