from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = 'Fix duplicate movies and update descriptions'

    def handle(self, *args, **options):
        # Get unique movie titles
        unique_titles = set()
        movies_to_keep = []
        movies_to_delete = []
        
        for movie in Movie.objects.all().order_by('id'):
            if movie.title not in unique_titles:
                unique_titles.add(movie.title)
                movies_to_keep.append(movie)
            else:
                movies_to_delete.append(movie)
        
        # Delete duplicates
        for movie in movies_to_delete:
            self.stdout.write(f'Deleting duplicate: {movie.title} (ID: {movie.id})')
            movie.delete()
        
        # Update remaining movies
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
        
        for movie in movies_to_keep:
            if movie.title in movie_updates:
                updates = movie_updates[movie.title]
                movie.description = updates['description']
                movie.cast = updates['cast']
                movie.trailer_url = updates['trailer_url']
                movie.save()
                self.stdout.write(f'Updated: {movie.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Fixed movies! Now have {Movie.objects.count()} unique movies.'
            )
        )
