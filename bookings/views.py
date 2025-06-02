from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.utils import timezone
from movies.models import Showtime
from .models import Seat, Booking, BookingSeat
import json


class SeatSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings/seat_selection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        showtime_id = kwargs['showtime_id']
        showtime = get_object_or_404(Showtime, id=showtime_id)

        # Get all seats for this theater
        seats = Seat.objects.filter(theater=showtime.theater).order_by('row', 'number')

        # Get booked seats for this showtime
        booked_seats = BookingSeat.objects.filter(
            showtime=showtime,
            is_booked=True
        ).values_list('seat_id', flat=True)

        context['showtime'] = showtime
        context['seats'] = seats
        context['booked_seats'] = list(booked_seats)
        return context


class BookSeatsView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            showtime_id = data.get('showtime_id')
            seat_ids = data.get('seat_ids', [])

            if not seat_ids:
                return JsonResponse({'error': 'No seats selected'}, status=400)

            showtime = get_object_or_404(Showtime, id=showtime_id)
            seats = Seat.objects.filter(id__in=seat_ids)

            # Check if seats are available
            booked_seats = BookingSeat.objects.filter(
                showtime=showtime,
                seat__in=seats,
                is_booked=True
            )

            if booked_seats.exists():
                return JsonResponse({'error': 'Some seats are already booked'}, status=400)

            # Calculate total amount
            total_amount = showtime.price * len(seats)

            # Create booking
            with transaction.atomic():
                booking = Booking.objects.create(
                    user=request.user,
                    showtime=showtime,
                    total_amount=total_amount,
                    status='PENDING'
                )

                # Create booking seats
                for seat in seats:
                    BookingSeat.objects.create(
                        booking=booking,
                        seat=seat,
                        showtime=showtime,
                        is_booked=True
                    )

                # Update available seats
                showtime.available_seats -= len(seats)
                showtime.save()

            return JsonResponse({
                'success': True,
                'booking_id': str(booking.booking_id),
                'redirect_url': f'/bookings/booking-confirmation/{booking.booking_id}/'
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class BookingConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings/booking_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = kwargs['booking_id']
        booking = get_object_or_404(Booking, booking_id=booking_id, user=self.request.user)
        context['booking'] = booking
        return context


class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

        if booking.status in ['CONFIRMED', 'PENDING']:
            booking.cancel_booking("Cancelled by user")
            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel this booking.')

        return redirect('accounts:user_bookings')


class TicketView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings/ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = kwargs['booking_id']
        booking = get_object_or_404(Booking, booking_id=booking_id, user=self.request.user)

        if booking.status != 'CONFIRMED':
            messages.error(self.request, 'Ticket not available for this booking.')
            return redirect('accounts:user_bookings')

        context['booking'] = booking
        return context


class TicketPDFView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from io import BytesIO

        booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

        if booking.status != 'CONFIRMED':
            messages.error(request, 'Ticket not available for this booking.')
            return redirect('accounts:user_bookings')

        # Create PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Title
        p.setFont("Helvetica-Bold", 24)
        p.drawString(50, height - 50, "CINEMA E-TICKET")

        # Movie title
        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, height - 100, f"Movie: {booking.showtime.movie.title}")

        # Theater info
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 130, f"Theater: {booking.showtime.theater.name}")
        p.drawString(50, height - 150, f"Location: {booking.showtime.theater.location}")

        # Show details
        p.drawString(50, height - 180, f"Date: {booking.showtime.show_date.strftime('%A, %B %d, %Y')}")
        p.drawString(50, height - 200, f"Time: {booking.showtime.show_time.strftime('%I:%M %p')}")

        # Seats
        seats = ", ".join([f"{bs.seat.row}{bs.seat.number}" for bs in booking.booking_seats.all()])
        p.drawString(50, height - 230, f"Seats: {seats}")

        # Booking details
        p.drawString(50, height - 260, f"Booking ID: {booking.booking_id}")
        p.drawString(50, height - 280, f"Customer: {booking.user.get_full_name() or booking.user.username}")
        p.drawString(50, height - 300, f"Total Amount: ${booking.total_amount}")

        # QR Code placeholder
        p.rect(50, height - 450, 100, 100, stroke=1, fill=0)
        p.drawString(55, height - 470, "QR CODE")
        p.drawString(55, height - 485, str(booking.booking_id)[:8])

        # Important notes
        p.setFont("Helvetica-Bold", 10)
        p.drawString(200, height - 380, "IMPORTANT INFORMATION:")
        p.setFont("Helvetica", 9)
        notes = [
            "• Arrive 15 minutes before showtime",
            "• Carry valid photo ID for verification",
            "• No outside food and beverages allowed",
            "• Mobile phones on silent mode",
            "• This ticket is non-transferable"
        ]

        y_pos = height - 400
        for note in notes:
            p.drawString(200, y_pos, note)
            y_pos -= 15

        # Footer
        p.setFont("Helvetica", 8)
        p.drawString(50, 50, "Customer Support: +1 (555) 123-4567 | support@cinemabooking.com")
        p.drawString(50, 35, "Thank you for choosing Cinema Booking System!")

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{booking.booking_id}.pdf"'
        return response
