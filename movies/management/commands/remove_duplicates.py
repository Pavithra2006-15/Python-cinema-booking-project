from django.core.management.base import BaseCommand
from movies.models import Movie, Showtime
from bookings.models import Booking, BookingSeat
from payments.models import Payment


class Command(BaseCommand):
    help = 'Remove duplicate movies'

    def handle(self, *args, **options):
        self.stdout.write('Removing duplicate movies...')
        
        # Get all movies
        movies = Movie.objects.all()
        self.stdout.write(f'Found {movies.count()} movies total')
        
        # Group movies by title to find duplicates
        movie_titles = {}
        for movie in movies:
            if movie.title not in movie_titles:
                movie_titles[movie.title] = []
            movie_titles[movie.title].append(movie)
        
        # Remove duplicates, keeping the first one
        deleted_count = 0
        for title, movie_list in movie_titles.items():
            if len(movie_list) > 1:
                self.stdout.write(f'Found {len(movie_list)} duplicates for "{title}"')
                # Keep the first movie, delete the rest
                movies_to_delete = movie_list[1:]
                for movie in movies_to_delete:
                    # First, delete related showtimes and bookings
                    showtimes = Showtime.objects.filter(movie=movie)
                    for showtime in showtimes:
                        # Delete bookings for this showtime
                        bookings = Booking.objects.filter(showtime=showtime)
                        for booking in bookings:
                            # Delete payments
                            Payment.objects.filter(booking=booking).delete()
                            # Delete booking seats
                            BookingSeat.objects.filter(booking=booking).delete()
                        # Delete bookings
                        bookings.delete()
                    # Delete showtimes
                    showtimes.delete()
                    # Finally delete the movie
                    self.stdout.write(f'Deleting duplicate movie: {movie.title} (ID: {movie.id})')
                    movie.delete()
                    deleted_count += 1
        
        final_count = Movie.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Cleanup completed! Deleted {deleted_count} duplicate movies. '
                f'Now have {final_count} unique movies.'
            )
        )
