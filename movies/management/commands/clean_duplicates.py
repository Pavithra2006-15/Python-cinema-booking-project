from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = 'Clean duplicate movies and update information'

    def handle(self, *args, **options):
        self.stdout.write('Starting cleanup...')
        
        # Get all movies
        all_movies = list(Movie.objects.all().order_by('id'))
        self.stdout.write(f'Found {len(all_movies)} total movies')
        
        # Track unique titles
        seen_titles = set()
        kept_movies = []
        deleted_count = 0
        
        # Process each movie
        for movie in all_movies:
            if movie.title not in seen_titles:
                seen_titles.add(movie.title)
                kept_movies.append(movie)
                self.stdout.write(f'Keeping: {movie.title} (ID: {movie.id})')
            else:
                self.stdout.write(f'Deleting duplicate: {movie.title} (ID: {movie.id})')
                movie.delete()
                deleted_count += 1
        
        self.stdout.write(f'Deleted {deleted_count} duplicate movies')
        
        # Update information for remaining movies
        movie_info = {
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
        
        # Update remaining movies
        updated_count = 0
        for movie in Movie.objects.all():
            if movie.title in movie_info:
                info = movie_info[movie.title]
                movie.description = info['description']
                movie.cast = info['cast']
                movie.trailer_url = info['trailer_url']
                movie.save()
                updated_count += 1
                self.stdout.write(f'Updated: {movie.title}')
        
        final_count = Movie.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Cleanup completed!\n'
                f'- Deleted: {deleted_count} duplicates\n'
                f'- Updated: {updated_count} movies\n'
                f'- Final count: {final_count} unique movies'
            )
        )
        
        # List final movies
        self.stdout.write('\nFinal movie list:')
        for movie in Movie.objects.all().order_by('title'):
            self.stdout.write(f'  - {movie.title}')
