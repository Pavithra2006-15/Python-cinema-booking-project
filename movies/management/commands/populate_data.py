from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta
from movies.models import Movie, Theater, Showtime
from bookings.models import Seat


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create theaters
        theater1 = Theater.objects.create(
            name='Grand Cinema',
            location='Downtown Mall',
            total_seats=100,
            rows=10,
            seats_per_row=10
        )

        theater2 = Theater.objects.create(
            name='Multiplex Theater',
            location='City Center',
            total_seats=150,
            rows=15,
            seats_per_row=10
        )

        # Create seats for theaters
        self.create_seats(theater1)
        self.create_seats(theater2)

        # Create movies
        movies_data = [
            {
                'title': 'The Amazing Adventure',
                'description': 'An epic adventure story that will keep you on the edge of your seat.',
                'genre': 'ACTION',
                'rating': 'PG_13',
                'duration': 120,
                'release_date': date.today() - timedelta(days=30),
                'director': 'John Director',
                'cast': 'Actor One, Actress Two, Actor Three',
                'language': 'English'
            },
            {
                'title': 'Comedy Central',
                'description': 'A hilarious comedy that will make you laugh out loud.',
                'genre': 'COMEDY',
                'rating': 'PG',
                'duration': 95,
                'release_date': date.today() - timedelta(days=15),
                'director': 'Jane Comedy',
                'cast': 'Funny Actor, Comedy Queen, Laugh Master',
                'language': 'English'
            },
            {
                'title': 'Space Odyssey',
                'description': 'A mind-bending science fiction journey through space and time.',
                'genre': 'SCI_FI',
                'rating': 'PG_13',
                'duration': 140,
                'release_date': date.today() - timedelta(days=7),
                'director': 'Sci Fi Director',
                'cast': 'Space Hero, Alien Princess, Robot Companion',
                'language': 'English'
            },
            {
                'title': 'Horror Nights',
                'description': 'A terrifying horror movie that will haunt your dreams.',
                'genre': 'HORROR',
                'rating': 'R',
                'duration': 105,
                'release_date': date.today(),
                'director': 'Horror Master',
                'cast': 'Scream Queen, Final Girl, Monster Actor',
                'language': 'English'
            }
        ]

        movies = []
        for movie_data in movies_data:
            movie = Movie.objects.create(**movie_data)
            movies.append(movie)

        # Create showtimes
        today = date.today()
        times = [time(10, 0), time(13, 30), time(17, 0), time(20, 30)]

        for i in range(7):  # Next 7 days
            show_date = today + timedelta(days=i)
            for theater in [theater1, theater2]:
                for j, show_time in enumerate(times):
                    # Assign different movies to different time slots
                    movie = movies[j % len(movies)]
                    Showtime.objects.create(
                        movie=movie,
                        theater=theater,
                        show_date=show_date,
                        show_time=show_time,
                        price=12.50,
                        available_seats=theater.total_seats
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(movies)} movies, '
                f'2 theaters, and multiple showtimes'
            )
        )

    def create_seats(self, theater):
        """Create seats for a theater"""
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

        for i in range(theater.rows):
            row_letter = rows[i]
            for seat_num in range(1, theater.seats_per_row + 1):
                seat_type = 'REGULAR'
                if i < 3:  # First 3 rows are premium
                    seat_type = 'PREMIUM'
                elif i >= theater.rows - 2:  # Last 2 rows are VIP
                    seat_type = 'VIP'

                Seat.objects.create(
                    theater=theater,
                    row=row_letter,
                    number=seat_num,
                    seat_type=seat_type
                )
