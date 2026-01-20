from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    total_orders = serializers.ReadOnlyField()
    total_spent = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'address', 'date_of_birth',
            'loyalty_points', 'is_vip', 'notes', 'total_orders', 'total_spent',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['loyalty_points', 'is_vip', 'created_at', 'updated_at']


class CustomerDetailSerializer(CustomerSerializer):
    """Detailed customer info with order history"""
    recent_orders = serializers.SerializerMethodField()
    recent_reservations = serializers.SerializerMethodField()

    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields + ['recent_orders', 'recent_reservations']

    def get_recent_orders(self, obj):
        from orders.serializers import OrderSerializer
        recent = obj.orders.all()[:5]
        return OrderSerializer(recent, many=True).data

    def get_recent_reservations(self, obj):
        from reservations.serializers import ReservationSerializer
        recent = obj.reservations.all()[:5]
        return ReservationSerializer(recent, many=True).data
