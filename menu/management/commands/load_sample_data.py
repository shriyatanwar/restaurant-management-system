from django.core.management.base import BaseCommand
from menu.models import Category, MenuItem
from customers.models import Customer
from reservations.models import Table
from inventory.models import Ingredient, MenuItemIngredient


class Command(BaseCommand):
    help = 'Loads sample data for testing and demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))

        # Create categories
        self.stdout.write('Creating categories...')
        appetizers, _ = Category.objects.get_or_create(
            name="Appetizers",
            defaults={"description": "Starters and small plates"}
        )
        mains, _ = Category.objects.get_or_create(
            name="Main Course",
            defaults={"description": "Main dishes"}
        )
        desserts, _ = Category.objects.get_or_create(
            name="Desserts",
            defaults={"description": "Sweet treats and pastries"}
        )
        beverages, _ = Category.objects.get_or_create(
            name="Beverages",
            defaults={"description": "Drinks and refreshments"}
        )

        # Create ingredients
        self.stdout.write('Creating ingredients...')
        chicken, _ = Ingredient.objects.get_or_create(
            name="Chicken Breast",
            defaults={
                "unit": "KG",
                "current_stock": 25.0,
                "minimum_stock": 10.0,
                "cost_per_unit": 8.50,
                "supplier": "Fresh Meats Co."
            }
        )

        lettuce, _ = Ingredient.objects.get_or_create(
            name="Lettuce",
            defaults={
                "unit": "KG",
                "current_stock": 15.0,
                "minimum_stock": 5.0,
                "cost_per_unit": 2.50,
                "supplier": "Green Farms"
            }
        )

        tomatoes, _ = Ingredient.objects.get_or_create(
            name="Tomatoes",
            defaults={
                "unit": "KG",
                "current_stock": 20.0,
                "minimum_stock": 8.0,
                "cost_per_unit": 3.00,
                "supplier": "Green Farms"
            }
        )

        cheese, _ = Ingredient.objects.get_or_create(
            name="Mozzarella Cheese",
            defaults={
                "unit": "KG",
                "current_stock": 10.0,
                "minimum_stock": 5.0,
                "cost_per_unit": 12.00,
                "supplier": "Dairy Products Ltd."
            }
        )

        flour, _ = Ingredient.objects.get_or_create(
            name="Flour",
            defaults={
                "unit": "KG",
                "current_stock": 50.0,
                "minimum_stock": 20.0,
                "cost_per_unit": 1.50,
                "supplier": "Bakery Supplies Co."
            }
        )

        # Create menu items (Indian cuisine)
        self.stdout.write('Creating menu items...')

        # Appetizers
        samosa, created = MenuItem.objects.get_or_create(
            name="Vegetable Samosa",
            defaults={
                "description": "Crispy pastry filled with spiced potatoes and peas",
                "category": appetizers,
                "price": 60,
                "is_available": True,
                "is_vegetarian": True,
                "is_vegan": True,
                "preparation_time": 15
            }
        )

        MenuItem.objects.get_or_create(
            name="Paneer Tikka",
            defaults={
                "description": "Cottage cheese marinated in spices and grilled in tandoor",
                "category": appetizers,
                "price": 180,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 20
            }
        )

        # Main Course
        butter_chicken, created = MenuItem.objects.get_or_create(
            name="Butter Chicken",
            defaults={
                "description": "Tender chicken in rich tomato-based creamy gravy",
                "category": mains,
                "price": 320,
                "is_available": True,
                "preparation_time": 25
            }
        )
        if created:
            MenuItemIngredient.objects.create(
                menu_item=butter_chicken,
                ingredient=chicken,
                quantity_required=0.25
            )
            MenuItemIngredient.objects.create(
                menu_item=butter_chicken,
                ingredient=tomatoes,
                quantity_required=0.10
            )

        MenuItem.objects.get_or_create(
            name="Palak Paneer",
            defaults={
                "description": "Fresh cottage cheese in smooth spinach gravy",
                "category": mains,
                "price": 260,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 20
            }
        )

        MenuItem.objects.get_or_create(
            name="Biryani (Chicken)",
            defaults={
                "description": "Fragrant basmati rice cooked with tender chicken and aromatic spices",
                "category": mains,
                "price": 280,
                "is_available": True,
                "preparation_time": 30
            }
        )

        MenuItem.objects.get_or_create(
            name="Dal Tadka",
            defaults={
                "description": "Yellow lentils tempered with ghee, cumin, and spices",
                "category": mains,
                "price": 180,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 25
            }
        )

        MenuItem.objects.get_or_create(
            name="Naan (Plain)",
            defaults={
                "description": "Traditional Indian flatbread baked in tandoor",
                "category": mains,
                "price": 40,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 10
            }
        )

        # Desserts
        MenuItem.objects.get_or_create(
            name="Gulab Jamun",
            defaults={
                "description": "Soft milk dumplings soaked in rose-flavored sugar syrup",
                "category": desserts,
                "price": 80,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 5
            }
        )

        MenuItem.objects.get_or_create(
            name="Rasmalai",
            defaults={
                "description": "Soft cottage cheese patties in sweetened creamy milk with cardamom",
                "category": desserts,
                "price": 100,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 5
            }
        )

        MenuItem.objects.get_or_create(
            name="Kulfi",
            defaults={
                "description": "Traditional Indian ice cream with pistachios and cardamom",
                "category": desserts,
                "price": 90,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 5
            }
        )

        # Beverages
        MenuItem.objects.get_or_create(
            name="Masala Chai",
            defaults={
                "description": "Indian spiced tea with milk and aromatic spices",
                "category": beverages,
                "price": 40,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 5
            }
        )

        MenuItem.objects.get_or_create(
            name="Mango Lassi",
            defaults={
                "description": "Sweet yogurt drink blended with fresh mango pulp",
                "category": beverages,
                "price": 80,
                "is_available": True,
                "is_vegetarian": True,
                "preparation_time": 5
            }
        )

        MenuItem.objects.get_or_create(
            name="Fresh Lime Soda",
            defaults={
                "description": "Refreshing lime juice with soda and a hint of mint",
                "category": beverages,
                "price": 60,
                "is_available": True,
                "is_vegetarian": True,
                "is_vegan": True,
                "preparation_time": 3
            }
        )

        # Create tables
        self.stdout.write('Creating tables...')
        for i in range(1, 11):
            Table.objects.get_or_create(
                table_number=i,
                defaults={
                    "capacity": 4 if i <= 8 else 6,
                    "is_available": True,
                    "location": "Main Hall" if i <= 5 else "Patio"
                }
            )

        # Create sample customers
        self.stdout.write('Creating customers...')
        Customer.objects.get_or_create(
            email="rahul.sharma@example.com",
            defaults={
                "name": "Rahul Sharma",
                "phone": "+919876543210",
                "address": "123 MG Road, Mumbai, Maharashtra 400001"
            }
        )

        Customer.objects.get_or_create(
            email="priya.patel@example.com",
            defaults={
                "name": "Priya Patel",
                "phone": "+919123456789",
                "address": "456 Brigade Road, Bangalore, Karnataka 560001"
            }
        )

        Customer.objects.get_or_create(
            email="amit.verma@example.com",
            defaults={
                "name": "Amit Verma",
                "phone": "+919988776655",
                "address": "789 Connaught Place, New Delhi 110001",
                "loyalty_points": 150,
                "is_vip": True
            }
        )

        Customer.objects.get_or_create(
            email="sneha.reddy@example.com",
            defaults={
                "name": "Sneha Reddy",
                "phone": "+918877665544",
                "address": "321 Park Street, Kolkata, West Bengal 700016"
            }
        )

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('Summary:'))
        self.stdout.write(f'  - Categories: {Category.objects.count()}')
        self.stdout.write(f'  - Menu Items: {MenuItem.objects.count()}')
        self.stdout.write(f'  - Ingredients: {Ingredient.objects.count()}')
        self.stdout.write(f'  - Tables: {Table.objects.count()}')
        self.stdout.write(f'  - Customers: {Customer.objects.count()}')
