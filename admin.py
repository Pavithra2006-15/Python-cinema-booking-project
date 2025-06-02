from django.contrib import admin
from .models import Movie, Genre, Language, MovieReview, MovieFormat, MovieWishlist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin configuration for Genre model"""
    
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Admin configuration for Language model"""
    
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(MovieFormat)
class MovieFormatAdmin(admin.ModelAdmin):
    """Admin configuration for MovieFormat model"""
    
    list_display = ['name', 'additional_cost']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin configuration for Movie model"""
    
    list_display = [
        'title', 'director', 'release_date', 'status', 'certification',
        'average_rating', 'total_reviews', 'is_active'
    ]
    list_filter = [
        'status', 'certification', 'release_date', 'is_active',
        'genres', 'languages'
    ]
    search_fields = ['title', 'director', 'cast']
    filter_horizontal = ['genres', 'languages']
    readonly_fields = ['average_rating', 'total_reviews', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'duration', 'certification')
        }),
        ('Release Information', {
            'fields': ('release_date', 'end_date', 'status', 'is_active')
        }),
        ('Media', {
            'fields': ('poster', 'banner', 'trailer_url')
        }),
        ('Classifications', {
            'fields': ('genres', 'languages')
        }),
        ('Cast & Crew', {
            'fields': ('director', 'cast', 'producer', 'music_director')
        }),
        ('Ratings', {
            'fields': ('imdb_rating', 'average_rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    """Admin configuration for MovieReview model"""
    
    list_display = [
        'movie', 'user', 'rating', 'is_verified_booking', 'created_at'
    ]
    list_filter = ['rating', 'is_verified_booking', 'created_at']
    search_fields = ['movie__title', 'user__email', 'review_text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MovieWishlist)
class MovieWishlistAdmin(admin.ModelAdmin):
    """Admin configuration for MovieWishlist model"""
    
    list_display = ['user', 'movie', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'movie__title']
    readonly_fields = ['created_at']
