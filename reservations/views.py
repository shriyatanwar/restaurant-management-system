from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer, ReservationDetailSerializer


class TableViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing restaurant tables.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_available', 'capacity']
    ordering_fields = ['table_number', 'capacity']

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get available tables"""
        date = request.query_params.get('date')
        time = request.query_params.get('time')

        if not date or not time:
            # Return all available tables
            tables = self.queryset.filter(is_available=True)
        else:
            # Check which tables are free at the specified time
            try:
                reservation_date = datetime.strptime(date, '%Y-%m-%d').date()
                reservation_time = datetime.strptime(time, '%H:%M').time()
            except ValueError:
                return Response(
                    {'error': 'Invalid date or time format. Use YYYY-MM-DD and HH:MM'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Find tables with no reservations at this time
            reserved_tables = Reservation.objects.filter(
                reservation_date=reservation_date,
                reservation_time=reservation_time,
                status__in=['PENDING', 'CONFIRMED', 'SEATED']
            ).values_list('table_id', flat=True)

            tables = self.queryset.filter(is_available=True).exclude(id__in=reserved_tables)

        serializer = self.get_serializer(tables, many=True)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing table reservations.
    Includes booking validation and status updates.
    """
    queryset = Reservation.objects.select_related('customer', 'table').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'table', 'reservation_date']
    search_fields = ['customer__name', 'customer__email']
    ordering_fields = ['reservation_date', 'reservation_time', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReservationDetailSerializer
        return ReservationSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update reservation status"""
        reservation = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Reservation.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = new_status
        reservation.save()

        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's reservations"""
        today = timezone.now().date()
        reservations = self.queryset.filter(reservation_date=today)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming reservations"""
        today = timezone.now().date()
        upcoming = self.queryset.filter(
            reservation_date__gte=today,
            status__in=['PENDING', 'CONFIRMED']
        ).order_by('reservation_date', 'reservation_time')

        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
