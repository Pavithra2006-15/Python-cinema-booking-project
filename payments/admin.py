from django.contrib import admin
from .models import Payment, PaymentTransaction


class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'booking', 'user', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['payment_id', 'booking__booking_id', 'user__username']
    readonly_fields = ['payment_id', 'created_at', 'updated_at']
    inlines = [PaymentTransactionInline]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['payment', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['payment__payment_id', 'gateway_transaction_id']
    readonly_fields = ['created_at']
