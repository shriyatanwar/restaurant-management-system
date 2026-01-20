from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer, MenuItemDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing menu categories.
    Supports CRUD operations and filtering.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all menu items in this category"""
        category = self.get_object()
        items = category.items.filter(is_available=True)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing menu items.
    Supports CRUD operations, filtering, and searching.
    """
    queryset = MenuItem.objects.select_related('category').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available', 'is_vegetarian', 'is_vegan']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MenuItemDetailSerializer
        return MenuItemSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get only available menu items"""
        items = self.queryset.filter(is_available=True)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """Toggle item availability"""
        item = self.get_object()
        item.is_available = not item.is_available
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)
