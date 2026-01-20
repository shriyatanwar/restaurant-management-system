from rest_framework import serializers
from .models import Order, OrderItem
from menu.serializers import MenuItemSerializer
from customers.serializers import CustomerSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'menu_item', 'menu_item_name', 'quantity',
            'unit_price', 'total_price', 'special_instructions', 'created_at'
        ]
        read_only_fields = ['unit_price', 'total_price', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'status', 'table_number',
            'notes', 'subtotal', 'tax', 'discount', 'total',
            'items_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['subtotal', 'tax', 'total', 'created_at', 'updated_at']

    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(OrderSerializer):
    """Detailed order serializer with all items"""
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ['items']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders with items"""
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'table_number', 'notes', 'discount', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        # Calculate totals
        order.calculate_totals()
        return order
