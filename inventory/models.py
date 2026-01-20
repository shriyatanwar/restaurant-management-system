from django.db import models
from django.core.validators import MinValueValidator
from menu.models import MenuItem


class Ingredient(models.Model):
    """Inventory ingredients"""
    UNIT_CHOICES = [
        ('KG', 'Kilograms'),
        ('G', 'Grams'),
        ('L', 'Liters'),
        ('ML', 'Milliliters'),
        ('PCS', 'Pieces'),
        ('PKG', 'Packages'),
    ]

    name = models.CharField(max_length=200, unique=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    supplier = models.CharField(max_length=200, blank=True)
    last_restocked = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"

    @property
    def is_low_stock(self):
        """Check if stock is below minimum threshold"""
        if self.current_stock is None or self.minimum_stock is None:
            return False
        return self.current_stock <= self.minimum_stock


class MenuItemIngredient(models.Model):
    """Links menu items with their ingredients and quantities"""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='menu_items')
    quantity_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Quantity required per menu item"
    )

    class Meta:
        unique_together = ['menu_item', 'ingredient']

    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity_required} {self.ingredient.unit} of {self.ingredient.name}"


class StockTransaction(models.Model):
    """Track stock changes (additions/deductions)"""
    TRANSACTION_TYPES = [
        ('PURCHASE', 'Purchase'),
        ('USED', 'Used in Order'),
        ('WASTE', 'Waste/Spoilage'),
        ('ADJUSTMENT', 'Manual Adjustment'),
    ]

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, default='admin')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.quantity} {self.ingredient.unit} of {self.ingredient.name}"
