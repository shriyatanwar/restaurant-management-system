from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from inventory.models import MenuItemIngredient, StockTransaction


@receiver(post_save, sender=OrderItem)
def update_inventory_on_order(sender, instance, created, **kwargs):
    """Automatically deduct inventory when an order item is created"""
    if created and instance.order.status in ['PENDING', 'PREPARING']:
        # Get all ingredients for this menu item
        ingredients = MenuItemIngredient.objects.filter(menu_item=instance.menu_item)

        for menu_ingredient in ingredients:
            # Calculate total quantity needed
            quantity_needed = menu_ingredient.quantity_required * instance.quantity

            # Deduct from inventory
            ingredient = menu_ingredient.ingredient
            ingredient.current_stock -= quantity_needed
            ingredient.save()

            # Create stock transaction record
            StockTransaction.objects.create(
                ingredient=ingredient,
                transaction_type='USED',
                quantity=-quantity_needed,
                notes=f"Used in Order #{instance.order.id} for {instance.quantity}x {instance.menu_item.name}"
            )
