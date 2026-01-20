from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer
from .serializers import CustomerSerializer, CustomerDetailSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customers.
    Supports CRUD operations and customer analytics.
    """
    queryset = Customer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_vip']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at', 'loyalty_points']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerSerializer

    @action(detail=False, methods=['get'])
    def vip(self, request):
        """Get VIP customers"""
        vip_customers = self.queryset.filter(is_vip=True)
        serializer = self.get_serializer(vip_customers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def order_history(self, request, pk=None):
        """Get customer's order history"""
        customer = self.get_object()
        from orders.serializers import OrderSerializer
        orders = customer.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reservation_history(self, request, pk=None):
        """Get customer's reservation history"""
        customer = self.get_object()
        from reservations.serializers import ReservationSerializer
        reservations = customer.reservations.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_loyalty_points(self, request, pk=None):
        """Manually add loyalty points to customer"""
        customer = self.get_object()
        points = request.data.get('points', 0)

        try:
            points = int(points)
            if points <= 0:
                return Response({'error': 'Points must be positive'}, status=400)

            customer.loyalty_points += points
            if customer.loyalty_points >= 100 and not customer.is_vip:
                customer.is_vip = True

            customer.save()
            serializer = self.get_serializer(customer)
            return Response(serializer.data)

        except ValueError:
            return Response({'error': 'Invalid points value'}, status=400)
