from django.contrib import admin
from .models import Movie, Theater, Showtime


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'rating', 'duration', 'release_date', 'is_active']
    list_filter = ['genre', 'rating', 'release_date', 'is_active']
    search_fields = ['title', 'director', 'cast']
    list_editable = ['is_active']
    date_hierarchy = 'release_date'
    ordering = ['-release_date']


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'total_seats', 'rows', 'seats_per_row', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'location']
    list_editable = ['is_active']


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theater', 'show_date', 'show_time', 'price', 'available_seats', 'is_active']
    list_filter = ['show_date', 'theater', 'is_active']
    search_fields = ['movie__title', 'theater__name']
    list_editable = ['price', 'is_active']
    date_hierarchy = 'show_date'
    ordering = ['show_date', 'show_time']
