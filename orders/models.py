from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from menu.models import MenuItem
from customers.models import Customer


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PREPARING', 'Preparing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    table_number = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    notes = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} - {self.status}"

    def calculate_totals(self):
        """Calculate order totals"""
        items = self.items.all()
        if items:
            self.subtotal = sum(item.total_price for item in items)
        else:
            self.subtotal = Decimal('0.00')

        self.tax = Decimal(str(self.subtotal)) * Decimal('0.10')  # 10% tax
        self.total = Decimal(str(self.subtotal)) + Decimal(str(self.tax)) - Decimal(str(self.discount))
        self.save()


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Auto-calculate total price"""
        self.unit_price = Decimal(str(self.menu_item.price))
        self.total_price = self.unit_price * Decimal(str(self.quantity))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
