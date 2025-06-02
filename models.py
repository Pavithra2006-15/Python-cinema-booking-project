from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Genre(models.Model):
    """Movie genres"""
    
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'genres'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Language(models.Model):
    """Movie languages"""
    
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=5, unique=True)  # e.g., 'en', 'hi', 'ta'
    
    class Meta:
        db_table = 'languages'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    """Movie model with all details"""
    
    MOVIE_STATUS_CHOICES = [
        ('coming_soon', 'Coming Soon'),
        ('now_showing', 'Now Showing'),
        ('ended', 'Ended'),
    ]
    
    CERTIFICATION_CHOICES = [
        ('U', 'Universal'),
        ('UA', 'Universal Adult'),
        ('A', 'Adult'),
        ('S', 'Restricted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    # Media
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    banner = models.ImageField(upload_to='movie_banners/', null=True, blank=True)
    trailer_url = models.URLField(blank=True)
    
    # Classifications
    genres = models.ManyToManyField(Genre, related_name='movies')
    languages = models.ManyToManyField(Language, related_name='movies')
    certification = models.CharField(max_length=5, choices=CERTIFICATION_CHOICES)
    status = models.CharField(max_length=20, choices=MOVIE_STATUS_CHOICES, default='coming_soon')
    
    # Cast and Crew
    director = models.CharField(max_length=200)
    cast = models.JSONField(default=list)  # List of actor names
    producer = models.CharField(max_length=200, blank=True)
    music_director = models.CharField(max_length=200, blank=True)
    
    # Ratings and Reviews
    imdb_rating = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    average_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'movies'
        ordering = ['-release_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_now_showing(self):
        today = timezone.now().date()
        return (
            self.status == 'now_showing' and
            self.release_date <= today and
            (self.end_date is None or self.end_date >= today)
        )
    
    @property
    def is_coming_soon(self):
        today = timezone.now().date()
        return self.status == 'coming_soon' and self.release_date > today
    
    def get_duration_display(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"


class MovieReview(models.Model):
    """User reviews for movies"""
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField(blank=True)
    is_verified_booking = models.BooleanField(default=False)  # User has booked this movie
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'movie_reviews'
        unique_together = ['movie', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.movie.title} ({self.rating}/5)"


class MovieFormat(models.Model):
    """Movie formats like 2D, 3D, IMAX, etc."""
    
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    additional_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'movie_formats'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MovieWishlist(models.Model):
    """User wishlist for movies"""
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movie_wishlists'
        unique_together = ['user', 'movie']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.movie.title}"
