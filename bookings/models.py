from django.db import models
from django.contrib.auth.models import User
from movies.models import Showtime, Theater
import uuid
from django.utils import timezone


class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField()
    seat_type = models.CharField(max_length=20, choices=[
        ('REGULAR', 'Regular'),
        ('PREMIUM', 'Premium'),
        ('VIP', 'VIP'),
    ], default='REGULAR')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['theater', 'row', 'number']
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row}{self.number}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ]

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ManyToManyField(Seat, through='BookingSeat')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    booking_time = models.DateTimeField(auto_now_add=True)
    payment_deadline = models.DateTimeField()
    confirmation_time = models.DateTimeField(null=True, blank=True)
    cancellation_time = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-booking_time']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.payment_deadline:
            # Set payment deadline to 15 minutes from booking time
            self.payment_deadline = timezone.now() + timezone.timedelta(minutes=15)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.payment_deadline and self.status == 'PENDING'

    @property
    def seat_numbers(self):
        return [str(booking_seat.seat) for booking_seat in self.booking_seats.all()]

    def cancel_booking(self, reason=""):
        self.status = 'CANCELLED'
        self.cancellation_time = timezone.now()
        self.cancellation_reason = reason
        self.save()

        # Release seats
        for booking_seat in self.booking_seats.all():
            booking_seat.is_booked = False
            booking_seat.save()

        # Update available seats in showtime
        self.showtime.available_seats += self.booking_seats.count()
        self.showtime.save()


class BookingSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_seats')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['seat', 'showtime']

    def __str__(self):
        return f"{self.booking.booking_id} - {self.seat}"
