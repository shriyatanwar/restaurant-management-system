from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderDetailSerializer, OrderCreateSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    Supports creating, updating, and tracking orders.
    """
    queryset = Order.objects.select_related('customer').prefetch_related('items').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'table_number']
    search_fields = ['customer__name', 'customer__email']
    ordering_fields = ['created_at', 'total', 'status']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # Add loyalty points to customer
        order.customer.add_loyalty_points(float(order.total))

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status"""
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Add item to existing order"""
        order = self.get_object()

        if order.status in ['COMPLETED', 'CANCELLED']:
            return Response(
                {'error': 'Cannot add items to completed or cancelled orders'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            order.calculate_totals()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get order statistics"""
        stats = Order.objects.aggregate(
            total_orders=Count('id'),
            total_revenue=Sum('total'),
            pending_orders=Count('id', filter=Q(status='PENDING')),
            preparing_orders=Count('id', filter=Q(status='PREPARING')),
        )
        return Response(stats)


class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet for managing individual order items"""
    queryset = OrderItem.objects.select_related('order', 'menu_item').all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'menu_item']
