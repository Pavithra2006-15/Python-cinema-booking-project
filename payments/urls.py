from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/<uuid:booking_id>/', views.PaymentProcessView.as_view(), name='process_payment'),
    path('success/<uuid:payment_id>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('cancel/<uuid:payment_id>/', views.PaymentCancelView.as_view(), name='payment_cancel'),
    path('stripe-webhook/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
]
