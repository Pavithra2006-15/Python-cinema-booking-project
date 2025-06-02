from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('seat-selection/<int:showtime_id>/', views.SeatSelectionView.as_view(), name='seat_selection'),
    path('book-seats/', views.BookSeatsView.as_view(), name='book_seats'),
    path('booking-confirmation/<uuid:booking_id>/', views.BookingConfirmationView.as_view(), name='booking_confirmation'),
    path('cancel-booking/<uuid:booking_id>/', views.CancelBookingView.as_view(), name='cancel_booking'),
    path('ticket/<uuid:booking_id>/', views.TicketView.as_view(), name='ticket'),
    path('ticket-pdf/<uuid:booking_id>/', views.TicketPDFView.as_view(), name='ticket_pdf'),
]
