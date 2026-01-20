from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ingredient, MenuItemIngredient, StockTransaction
from .serializers import (
    IngredientSerializer,
    MenuItemIngredientSerializer,
    StockTransactionSerializer
)


class IngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory ingredients.
    Supports CRUD operations and stock monitoring.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unit']
    search_fields = ['name', 'supplier']
    ordering_fields = ['name', 'current_stock', 'minimum_stock']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get ingredients with low stock"""
        low_stock_items = [item for item in self.queryset if item.is_low_stock]
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restock(self, request, pk=None):
        """Add stock to an ingredient"""
        ingredient = self.get_object()
        quantity = request.data.get('quantity')

        if not quantity or float(quantity) <= 0:
            return Response(
                {'error': 'Invalid quantity'},
                status=400
            )

        # Create stock transaction
        from django.utils import timezone
        StockTransaction.objects.create(
            ingredient=ingredient,
            transaction_type='PURCHASE',
            quantity=float(quantity),
            notes=request.data.get('notes', ''),
            created_by=request.user.username if request.user.is_authenticated else 'admin'
        )

        ingredient.current_stock += float(quantity)
        ingredient.last_restocked = timezone.now()
        ingredient.save()

        serializer = self.get_serializer(ingredient)
        return Response(serializer.data)


class MenuItemIngredientViewSet(viewsets.ModelViewSet):
    """ViewSet for managing menu item ingredients"""
    queryset = MenuItemIngredient.objects.select_related('menu_item', 'ingredient').all()
    serializer_class = MenuItemIngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['menu_item', 'ingredient']


class StockTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and creating stock transactions"""
    queryset = StockTransaction.objects.select_related('ingredient').all()
    serializer_class = StockTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ingredient', 'transaction_type']
    ordering_fields = ['created_at']
    http_method_names = ['get', 'post', 'head', 'options']  # No update or delete
