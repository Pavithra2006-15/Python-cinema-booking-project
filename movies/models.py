from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    GENRE_CHOICES = [
        ('ACTION', 'Action'),
        ('COMEDY', 'Comedy'),
        ('DRAMA', 'Drama'),
        ('HORROR', 'Horror'),
        ('ROMANCE', 'Romance'),
        ('THRILLER', 'Thriller'),
        ('SCI_FI', 'Science Fiction'),
        ('FANTASY', 'Fantasy'),
        ('ANIMATION', 'Animation'),
        ('DOCUMENTARY', 'Documentary'),
    ]

    RATING_CHOICES = [
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance'),
        ('PG_13', 'PG-13'),
        ('R', 'Restricted'),
        ('NC_17', 'Adults Only'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    director = models.CharField(max_length=100)
    cast = models.TextField(help_text="Comma-separated list of main cast")
    language = models.CharField(max_length=50, default='English')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title

    @property
    def duration_display(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"


class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    total_seats = models.PositiveIntegerField()
    rows = models.PositiveIntegerField(default=10)
    seats_per_row = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    show_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['theater', 'show_date', 'show_time']
        ordering = ['show_date', 'show_time']

    def __str__(self):
        return f"{self.movie.title} - {self.show_date} {self.show_time}"

    def save(self, *args, **kwargs):
        if not self.available_seats:
            self.available_seats = self.theater.total_seats
        super().save(*args, **kwargs)
