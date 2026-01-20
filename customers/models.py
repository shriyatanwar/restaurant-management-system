from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Customer(models.Model):
    """Restaurant customers"""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    loyalty_points = models.IntegerField(default=0)
    is_vip = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Special preferences, allergies, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def total_orders(self):
        """Get total number of orders"""
        return self.orders.count()

    @property
    def total_spent(self):
        """Calculate total amount spent by customer"""
        return sum(order.total for order in self.orders.filter(status='COMPLETED'))

    def add_loyalty_points(self, amount):
        """Add loyalty points based on order amount (1 point per ₹100)"""
        points = int(amount / 100)
        self.loyalty_points += points

        # Automatically upgrade to VIP after 100 points
        if self.loyalty_points >= 100 and not self.is_vip:
            self.is_vip = True

        self.save()
