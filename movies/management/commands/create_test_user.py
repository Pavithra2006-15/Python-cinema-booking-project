from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from movies.models import Movie, Theater, Showtime
from bookings.models import Seat, Booking, BookingSeat
from payments.models import Payment


class Command(BaseCommand):
    help = 'Create a test user with sample bookings'

    def handle(self, *args, **options):
        # Create test user
        username = 'testuser'
        password = 'testpass123'
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(f'Created test user: {username}')
        else:
            self.stdout.write(f'Test user already exists: {username}')
        
        # Create a sample confirmed booking
        try:
            movie = Movie.objects.first()
            theater = Theater.objects.first()
            showtime = Showtime.objects.filter(
                show_date__gte=timezone.now().date()
            ).first()
            
            if showtime:
                # Get some seats
                seats = Seat.objects.filter(theater=theater)[:2]
                
                if seats.exists():
                    # Create booking
                    booking = Booking.objects.create(
                        user=user,
                        showtime=showtime,
                        total_amount=showtime.price * seats.count(),
                        status='CONFIRMED',
                        confirmation_time=timezone.now()
                    )
                    
                    # Create booking seats
                    for seat in seats:
                        BookingSeat.objects.create(
                            booking=booking,
                            seat=seat,
                            showtime=showtime,
                            is_booked=True
                        )
                    
                    # Create payment
                    Payment.objects.create(
                        booking=booking,
                        user=user,
                        amount=booking.total_amount,
                        payment_method='STRIPE',
                        status='COMPLETED',
                        completed_at=timezone.now()
                    )
                    
                    self.stdout.write(f'Created sample booking: {booking.booking_id}')
                    
        except Exception as e:
            self.stdout.write(f'Error creating sample booking: {e}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Test user created successfully!\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'You can now login and test the booking system.'
            )
        )
