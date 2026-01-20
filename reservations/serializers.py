from rest_framework import serializers
from .models import Table, Reservation
from customers.serializers import CustomerSerializer


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'capacity', 'is_available', 'location', 'created_at']
        read_only_fields = ['created_at']


class ReservationSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    table_number = serializers.IntegerField(source='table.table_number', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'customer', 'customer_name', 'table', 'table_number',
            'reservation_date', 'reservation_time', 'number_of_guests',
            'status', 'special_requests', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Custom validation for reservations"""
        table = data.get('table')
        number_of_guests = data.get('number_of_guests')

        if table and number_of_guests:
            if number_of_guests > table.capacity:
                raise serializers.ValidationError(
                    f"Table {table.table_number} can only accommodate {table.capacity} guests."
                )

        return data


class ReservationDetailSerializer(ReservationSerializer):
    """Detailed reservation with customer and table info"""
    customer = CustomerSerializer(read_only=True)
    table = TableSerializer(read_only=True)

    class Meta(ReservationSerializer.Meta):
        fields = ReservationSerializer.Meta.fields
