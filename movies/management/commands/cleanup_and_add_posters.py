from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from movies.models import Movie, Showtime
from bookings.models import Booking, BookingSeat
from payments.models import Payment
from io import BytesIO
from PIL import Image


class Command(BaseCommand):
    help = 'Remove duplicate movies and add movie posters'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning up duplicate movies and adding posters...')

        # First, let's see what movies we have
        movies = Movie.objects.all()
        self.stdout.write(f'Found {movies.count()} movies total')

        # Group movies by title to find duplicates
        movie_titles = {}
        for movie in movies:
            if movie.title not in movie_titles:
                movie_titles[movie.title] = []
            movie_titles[movie.title].append(movie)

        # Remove duplicates, keeping the first one
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
                    movie.delete()
                    self.stdout.write(f'Deleted duplicate movie: {movie.title} (ID: {movie.id})')

        # Now add posters to remaining movies
        remaining_movies = Movie.objects.all()
        self.stdout.write(f'Adding posters to {remaining_movies.count()} unique movies...')

        # Create colored posters for movies
        colors = {
            'The Amazing Adventure': (255, 107, 107),  # Red
            'Comedy Central': (78, 205, 196),         # Teal
            'Space Odyssey': (69, 183, 209),          # Blue
            'Horror Nights': (150, 206, 180)          # Green
        }

        for movie in remaining_movies:
            if not movie.poster:
                try:
                    # Create a simple colored poster
                    color = colors.get(movie.title, (204, 204, 204))  # Default gray
                    img = Image.new('RGB', (300, 450), color=color)

                    # Save to BytesIO
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG', quality=85)
                    img_io.seek(0)

                    # Save to movie poster field
                    movie.poster.save(
                        f'{movie.title.lower().replace(" ", "_")}_poster.jpg',
                        ContentFile(img_io.getvalue()),
                        save=True
                    )

                    self.stdout.write(f'Added poster for: {movie.title}')

                except Exception as e:
                    self.stdout.write(f'Error adding poster for {movie.title}: {e}')

        # Update movie information with better descriptions and cast
        movie_updates = {
            'The Amazing Adventure': {
                'description': 'Join our hero on an epic quest through dangerous lands filled with mythical creatures and ancient mysteries. This action-packed adventure will keep you on the edge of your seat from start to finish.',
                'cast': 'Chris Evans, Scarlett Johansson, Robert Downey Jr., Mark Ruffalo',
                'trailer_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            },
            'Comedy Central': {
                'description': 'A laugh-out-loud comedy about a group of friends who accidentally become the most unlikely heroes in their small town. Featuring hilarious mishaps and heartwarming moments.',
                'cast': 'Ryan Reynolds, Emma Stone, Jonah Hill, Amy Poehler',
                'trailer_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            },
            'Space Odyssey': {
                'description': 'A mind-bending journey through the cosmos that explores the mysteries of space and time. Stunning visuals and a compelling story make this a must-see sci-fi epic.',
                'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine',
                'trailer_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            },
            'Horror Nights': {
                'description': 'A terrifying supernatural thriller that will haunt your dreams. When a family moves into an old mansion, they discover they are not alone. Prepare for spine-chilling scares.',
                'cast': 'Vera Farmiga, Patrick Wilson, Madison Wolfe, Frances OConnor',
                'trailer_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            }
        }

        for movie in remaining_movies:
            if movie.title in movie_updates:
                updates = movie_updates[movie.title]
                movie.description = updates['description']
                movie.cast = updates['cast']
                movie.trailer_url = updates['trailer_url']
                movie.save()
                self.stdout.write(f'Updated information for: {movie.title}')

        final_count = Movie.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Cleanup completed! Now have {final_count} unique movies with posters and updated information.'
            )
        )
