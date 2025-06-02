from django.contrib import admin
from .models import Seat, Booking, BookingSeat


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'row', 'number', 'seat_type', 'is_active']
    list_filter = ['theater', 'seat_type', 'is_active']
    search_fields = ['theater__name', 'row']
    list_editable = ['seat_type', 'is_active']
    ordering = ['theater', 'row', 'number']


class BookingSeatInline(admin.TabularInline):
    model = BookingSeat
    extra = 0
    readonly_fields = ['booked_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'showtime', 'total_amount', 'status', 'booking_time']
    list_filter = ['status', 'booking_time', 'showtime__show_date']
    search_fields = ['booking_id', 'user__username', 'showtime__movie__title']
    readonly_fields = ['booking_id', 'booking_time', 'payment_deadline']
    inlines = [BookingSeatInline]
    date_hierarchy = 'booking_time'
    ordering = ['-booking_time']


@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = ['booking', 'seat', 'showtime', 'is_booked', 'booked_at']
    list_filter = ['is_booked', 'booked_at', 'showtime__show_date']
    search_fields = ['booking__booking_id', 'seat__row']
    readonly_fields = ['booked_at']
