from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from bookings.models import Booking
from .models import Payment
import json


class PaymentProcessView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/payment_process.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = kwargs['booking_id']
        booking = get_object_or_404(Booking, booking_id=booking_id, user=self.request.user)

        if booking.status != 'PENDING':
            messages.error(self.request, 'Payment not available for this booking.')
            return redirect('accounts:user_bookings')

        # Create or get payment
        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                'user': self.request.user,
                'amount': booking.total_amount,
                'payment_method': 'STRIPE',
                'status': 'PENDING'
            }
        )

        context['booking'] = booking
        context['payment'] = payment
        context['stripe_public_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_id = kwargs['payment_id']
        payment = get_object_or_404(Payment, payment_id=payment_id, user=self.request.user)

        # Mark payment as completed if not already
        if payment.status == 'PENDING':
            payment.mark_completed()

        context['payment'] = payment
        context['booking'] = payment.booking
        return context


class PaymentCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/payment_cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_id = kwargs['payment_id']
        payment = get_object_or_404(Payment, payment_id=payment_id, user=self.request.user)

        # Mark payment as failed
        if payment.status == 'PENDING':
            payment.mark_failed()

        context['payment'] = payment
        context['booking'] = payment.booking
        return context


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request):
        # This is a placeholder for Stripe webhook handling
        # In a real implementation, you would verify the webhook signature
        # and handle different event types

        try:
            payload = request.body
            event = json.loads(payload)

            # Handle the event
            if event['type'] == 'payment_intent.succeeded':
                # Handle successful payment
                payment_intent = event['data']['object']
                # Update payment status based on payment_intent
                pass
            elif event['type'] == 'payment_intent.payment_failed':
                # Handle failed payment
                payment_intent = event['data']['object']
                # Update payment status based on payment_intent
                pass

            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=400)
