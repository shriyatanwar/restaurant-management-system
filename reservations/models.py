from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from customers.models import Customer
from datetime import datetime, timedelta


class Table(models.Model):
    """Restaurant tables"""
    table_number = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, blank=True, help_text="e.g., Window, Patio, Main Hall")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['table_number']

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class Reservation(models.Model):
    """Table reservations"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SEATED', 'Seated'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='reservations')
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['reservation_date', 'reservation_time']
        unique_together = ['table', 'reservation_date', 'reservation_time']

    def __str__(self):
        return f"{self.customer.name} - Table {self.table.table_number} on {self.reservation_date} at {self.reservation_time}"

    def clean(self):
        """Validate reservation"""
        # Check if table capacity is sufficient
        if self.number_of_guests > self.table.capacity:
            raise ValidationError(f"Table {self.table.table_number} can only accommodate {self.table.capacity} guests.")

        # Check for overlapping reservations (within 2 hours)
        if self.pk:  # Only check when updating
            reservation_datetime = datetime.combine(self.reservation_date, self.reservation_time)
            start_time = reservation_datetime - timedelta(hours=2)
            end_time = reservation_datetime + timedelta(hours=2)

            overlapping = Reservation.objects.filter(
                table=self.table,
                reservation_date=self.reservation_date,
                status__in=['PENDING', 'CONFIRMED', 'SEATED']
            ).exclude(pk=self.pk)

            for reservation in overlapping:
                existing_datetime = datetime.combine(reservation.reservation_date, reservation.reservation_time)
                if start_time <= existing_datetime <= end_time:
                    raise ValidationError(
                        f"Table {self.table.table_number} is already reserved at {reservation.reservation_time}. "
                        f"Please choose a different time or table."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
