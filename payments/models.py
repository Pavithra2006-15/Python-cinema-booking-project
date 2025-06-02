from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking
import uuid


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('STRIPE', 'Stripe'),
        ('RAZORPAY', 'Razorpay'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Cash'),
    ]

    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    # Payment gateway specific fields
    gateway_payment_id = models.CharField(max_length=100, blank=True, null=True)
    gateway_response = models.JSONField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Refund information
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refund_reason = models.TextField(blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.payment_id} - {self.amount}"

    @property
    def is_successful(self):
        return self.status == 'COMPLETED'

    def mark_completed(self):
        from django.utils import timezone
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save()

        # Update booking status
        self.booking.status = 'CONFIRMED'
        self.booking.confirmation_time = timezone.now()
        self.booking.save()

    def mark_failed(self):
        self.status = 'FAILED'
        self.save()

        # Cancel the booking
        self.booking.cancel_booking("Payment failed")


class PaymentTransaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=[
        ('CHARGE', 'Charge'),
        ('REFUND', 'Refund'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway_transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    gateway_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
