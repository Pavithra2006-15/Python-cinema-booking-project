from django.core.management.base import BaseCommand
from movies.models import Movie, Showtime, Theater
from datetime import date


class Command(BaseCommand):
    help = 'Display all movie showtimes'

    def handle(self, *args, **options):
        self.stdout.write('🎬 CINEMA BOOKING SYSTEM - SHOW TIMINGS 🎬\n')
        
        # Get all movies
        movies = Movie.objects.all().order_by('title')
        
        if not movies.exists():
            self.stdout.write('❌ No movies found!')
            return
        
        self.stdout.write(f'Found {movies.count()} movies:\n')
        
        total_showtimes = 0
        today = date.today()
        
        for movie in movies:
            self.stdout.write(f'🎬 {movie.title}')
            self.stdout.write(f'   📝 {movie.get_genre_display()} | ⏱️  {movie.duration_display} | 🎭 {movie.get_rating_display()}')
            
            # Get showtimes for this movie
            showtimes = Showtime.objects.filter(
                movie=movie, 
                is_active=True
            ).order_by('show_date', 'show_time')
            
            if showtimes.exists():
                self.stdout.write(f'   📅 Showtimes ({showtimes.count()} total):')
                
                current_date = None
                for showtime in showtimes:
                    total_showtimes += 1
                    
                    # Group by date
                    if current_date != showtime.show_date:
                        current_date = showtime.show_date
                        
                        # Determine if date is past, today, or future
                        if showtime.show_date < today:
                            status = "📜 (Past)"
                        elif showtime.show_date == today:
                            status = "🔥 (Today)"
                        else:
                            status = "🔮 (Upcoming)"
                        
                        self.stdout.write(f'      📆 {showtime.show_date.strftime("%A, %B %d, %Y")} {status}')
                    
                    self.stdout.write(f'         🕐 {showtime.show_time.strftime("%I:%M %p")} - 🏛️  {showtime.theater.name}')
                    self.stdout.write(f'            📍 {showtime.theater.location}')
                    self.stdout.write(f'            💰 ${showtime.price} | 🪑 {showtime.available_seats} seats available')
            else:
                self.stdout.write('   ❌ No showtimes scheduled')
            
            self.stdout.write('')  # Empty line between movies
        
        # Summary
        self.stdout.write('=' * 60)
        self.stdout.write('📊 SUMMARY STATISTICS')
        self.stdout.write('=' * 60)
        
        # Count different types of showtimes
        upcoming_showtimes = Showtime.objects.filter(
            is_active=True, 
            show_date__gte=today
        ).count()
        
        past_showtimes = Showtime.objects.filter(
            is_active=True, 
            show_date__lt=today
        ).count()
        
        today_showtimes = Showtime.objects.filter(
            is_active=True, 
            show_date=today
        ).count()
        
        self.stdout.write(f'🎬 Total Movies: {movies.count()}')
        self.stdout.write(f'📅 Total Showtimes: {total_showtimes}')
        self.stdout.write(f'📜 Past Showtimes: {past_showtimes}')
        self.stdout.write(f'🔥 Today\'s Showtimes: {today_showtimes}')
        self.stdout.write(f'🔮 Upcoming Showtimes: {upcoming_showtimes}')
        
        # Theater info
        theaters = Theater.objects.filter(is_active=True)
        self.stdout.write(f'🏛️  Active Theaters: {theaters.count()}')
        
        if total_showtimes > 0:
            earliest = Showtime.objects.filter(is_active=True).order_by('show_date').first()
            latest = Showtime.objects.filter(is_active=True).order_by('-show_date').first()
            self.stdout.write(f'📅 Date Range: {earliest.show_date} to {latest.show_date}')
        
        # Theater details
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏛️  THEATER INFORMATION')
        self.stdout.write('=' * 60)
        
        for theater in theaters:
            theater_showtimes = Showtime.objects.filter(
                theater=theater, 
                is_active=True
            ).count()
            
            self.stdout.write(f'🏛️  {theater.name}')
            self.stdout.write(f'   📍 {theater.location}')
            self.stdout.write(f'   🪑 {theater.total_seats} total seats')
            self.stdout.write(f'   📅 {theater_showtimes} scheduled showtimes')
            self.stdout.write('')
        
        self.stdout.write('✅ Showtime check completed!')
