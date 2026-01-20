from rest_framework import serializers
from .models import Ingredient, MenuItemIngredient, StockTransaction


class IngredientSerializer(serializers.ModelSerializer):
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = [
            'id', 'name', 'unit', 'current_stock', 'minimum_stock',
            'cost_per_unit', 'supplier', 'stock_status', 'is_low_stock',
            'last_restocked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_low_stock', 'created_at', 'updated_at']

    def get_stock_status(self, obj):
        if obj.is_low_stock:
            return "LOW"
        return "OK"


class MenuItemIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    unit = serializers.CharField(source='ingredient.unit', read_only=True)

    class Meta:
        model = MenuItemIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'quantity_required', 'unit']


class StockTransactionSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = StockTransaction
        fields = [
            'id', 'ingredient', 'ingredient_name', 'transaction_type',
            'quantity', 'notes', 'created_by', 'created_at'
        ]
        read_only_fields = ['created_at']

    def create(self, validated_data):
        transaction = StockTransaction.objects.create(**validated_data)

        # Update ingredient stock based on transaction type
        ingredient = transaction.ingredient
        if transaction.transaction_type in ['PURCHASE', 'ADJUSTMENT']:
            ingredient.current_stock += abs(transaction.quantity)
            if transaction.transaction_type == 'PURCHASE':
                from django.utils import timezone
                ingredient.last_restocked = timezone.now()
        else:  # USED or WASTE
            ingredient.current_stock -= abs(transaction.quantity)

        ingredient.save()
        return transaction
