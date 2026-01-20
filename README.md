# Restaurant Management System

A comprehensive Admin-Based Restaurant Management System built with Django and Django REST Framework to help restaurant owners efficiently manage their operations.

## Features

### 1. Admin Authentication
- Secure admin login via Django Admin Panel
- Permission-based access control
- Session-based authentication for API endpoints

### 2. Menu Management
- Add, update, and delete food items
- Categorize menu items (Appetizers, Main Course, Desserts, Beverages, etc.)
- Control item availability and pricing
- Mark dietary preferences (Vegetarian, Vegan)
- Track preparation time

### 3. Order Management
- Create and manage customer orders
- Track order status: Pending → Preparing → Completed / Cancelled
- Automatic billing calculation with tax
- Apply discounts
- View complete order history
- Order statistics and analytics

### 4. Inventory Management
- Track stock levels of ingredients
- Automatically update inventory when orders are placed
- Low-stock alerts
- Stock transaction history
- Link ingredients to menu items
- Manual stock adjustments

### 5. Table Reservation System
- Book tables with date and time
- Prevent double bookings with validation
- Manage reservation status
- Check table availability
- Track guest count and special requests

### 6. Customer Management
- Store customer details
- Track order history per customer
- Loyalty points system (1 point per $10 spent)
- Automatic VIP upgrade at 100 points
- Customer analytics (total orders, total spent)

## Technical Stack

- **Backend Framework**: Django 4.2+
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL / MySQL / SQLite
- **Additional Libraries**:
  - django-cors-headers (CORS support)
  - django-filter (Advanced filtering)
  - Pillow (Image handling)
  - python-decouple (Environment management)

## Project Structure

```
restaurant_management/
├── manage.py
├── requirements.txt
├── .env.example
├── restaurant/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── menu/                    # Menu management app
│   ├── models.py           # Category, MenuItem
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── orders/                  # Order management app
│   ├── models.py           # Order, OrderItem
│   ├── views.py
│   ├── serializers.py
│   ├── signals.py          # Auto inventory updates
│   └── admin.py
├── inventory/               # Inventory management app
│   ├── models.py           # Ingredient, StockTransaction
│   ├── views.py
│   └── admin.py
├── reservations/            # Reservation system app
│   ├── models.py           # Table, Reservation
│   ├── views.py
│   └── admin.py
└── customers/               # Customer management app
    ├── models.py           # Customer
    ├── views.py
    └── admin.py
```

## Installation & Setup

### 1. Clone or Setup Project

```bash
cd D:\projects\restaurant_management
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
copy .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For PostgreSQL:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# For MySQL:
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=restaurant_db
# DB_USER=root
# DB_PASSWORD=your-password
# DB_HOST=localhost
# DB_PORT=3306

# For SQLite (default - no config needed):
# Just leave DB_ENGINE empty or remove database config from .env
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

## API Endpoints

### Menu Management

#### Categories
- `GET /api/menu/categories/` - List all categories
- `POST /api/menu/categories/` - Create new category
- `GET /api/menu/categories/{id}/` - Get category details
- `PUT /api/menu/categories/{id}/` - Update category
- `DELETE /api/menu/categories/{id}/` - Delete category
- `GET /api/menu/categories/{id}/items/` - Get items in category

#### Menu Items
- `GET /api/menu/items/` - List all menu items
- `POST /api/menu/items/` - Create new menu item
- `GET /api/menu/items/{id}/` - Get item details (with ingredients)
- `PUT /api/menu/items/{id}/` - Update menu item
- `DELETE /api/menu/items/{id}/` - Delete menu item
- `GET /api/menu/items/available/` - List only available items
- `POST /api/menu/items/{id}/toggle_availability/` - Toggle item availability

### Order Management

- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details (with items)
- `PUT /api/orders/{id}/` - Update order
- `POST /api/orders/{id}/update_status/` - Update order status
- `POST /api/orders/{id}/add_item/` - Add item to existing order
- `GET /api/orders/statistics/` - Get order statistics

### Inventory Management

#### Ingredients
- `GET /api/inventory/ingredients/` - List all ingredients
- `POST /api/inventory/ingredients/` - Create new ingredient
- `GET /api/inventory/ingredients/{id}/` - Get ingredient details
- `PUT /api/inventory/ingredients/{id}/` - Update ingredient
- `DELETE /api/inventory/ingredients/{id}/` - Delete ingredient
- `GET /api/inventory/ingredients/low_stock/` - Get low stock items
- `POST /api/inventory/ingredients/{id}/restock/` - Add stock

#### Stock Transactions
- `GET /api/inventory/transactions/` - List all transactions
- `POST /api/inventory/transactions/` - Create transaction (manual adjustment)
- `GET /api/inventory/transactions/{id}/` - Get transaction details

### Reservation Management

#### Tables
- `GET /api/reservations/tables/` - List all tables
- `POST /api/reservations/tables/` - Create new table
- `GET /api/reservations/tables/{id}/` - Get table details
- `PUT /api/reservations/tables/{id}/` - Update table
- `DELETE /api/reservations/tables/{id}/` - Delete table
- `GET /api/reservations/tables/available/?date=YYYY-MM-DD&time=HH:MM` - Check available tables

#### Reservations
- `GET /api/reservations/` - List all reservations
- `POST /api/reservations/` - Create new reservation
- `GET /api/reservations/{id}/` - Get reservation details
- `PUT /api/reservations/{id}/` - Update reservation
- `DELETE /api/reservations/{id}/` - Delete reservation
- `POST /api/reservations/{id}/update_status/` - Update reservation status
- `GET /api/reservations/today/` - Get today's reservations
- `GET /api/reservations/upcoming/` - Get upcoming reservations

### Customer Management

- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details (with order/reservation history)
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer
- `GET /api/customers/vip/` - List VIP customers
- `GET /api/customers/{id}/order_history/` - Get customer's orders
- `GET /api/customers/{id}/reservation_history/` - Get customer's reservations
- `POST /api/customers/{id}/add_loyalty_points/` - Manually add loyalty points

## Usage Examples

### Creating a Menu Item

```bash
curl -X POST http://127.0.0.1:8000/api/menu/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Margherita Pizza",
    "description": "Classic pizza with tomato sauce, mozzarella, and basil",
    "category": 1,
    "price": "12.99",
    "is_available": true,
    "is_vegetarian": true,
    "preparation_time": 15
  }'
```

### Creating an Order

```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer": 1,
    "table_number": 5,
    "notes": "Extra cheese",
    "discount": 0,
    "items": [
      {
        "menu_item": 1,
        "quantity": 2,
        "special_instructions": "Well done"
      },
      {
        "menu_item": 3,
        "quantity": 1
      }
    ]
  }'
```

### Making a Reservation

```bash
curl -X POST http://127.0.0.1:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer": 1,
    "table": 3,
    "reservation_date": "2026-01-25",
    "reservation_time": "19:00",
    "number_of_guests": 4,
    "special_requests": "Window seat preferred"
  }'
```

## Business Logic

### Automatic Inventory Updates
When an order is created, the system automatically:
1. Checks ingredient requirements for each menu item
2. Deducts required quantities from inventory
3. Creates stock transaction records
4. Triggers low-stock alerts if needed

### Loyalty Points System
- Customers earn 1 loyalty point for every $10 spent
- Automatic VIP upgrade at 100 points
- VIP status can provide special benefits (customizable)

### Reservation Validation
- Prevents double bookings at the same time
- Validates table capacity vs. guest count
- Checks for overlapping reservations (2-hour buffer)

### Order Billing
- Automatic subtotal calculation
- 10% tax applied
- Discounts supported
- Final total computed automatically

## Django Admin Panel

Access the admin panel at http://127.0.0.1:8000/admin/

Features:
- Rich admin interfaces for all models
- Inline editing for order items
- Stock status badges
- VIP customer badges
- Advanced filtering and search
- Bulk actions

## Database Models

### Menu App
- **Category**: Menu categories
- **MenuItem**: Food items with pricing and details

### Orders App
- **Order**: Customer orders with billing
- **OrderItem**: Individual items in orders

### Inventory App
- **Ingredient**: Stock items with quantities
- **MenuItemIngredient**: Links menu items to ingredients
- **StockTransaction**: Inventory change log

### Reservations App
- **Table**: Restaurant tables
- **Reservation**: Table bookings

### Customers App
- **Customer**: Customer information and loyalty

## Security Features

- Admin-only API access (IsAdminUser permission)
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection
- Password validation
- Session-based authentication

## Testing

Run tests with:

```bash
python manage.py test
```

## Production Deployment

### 1. Security Settings

Update `.env` for production:
```env
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Collect Static Files

```bash
python manage.py collectstatic
```

### 3. Use Production Database

Configure PostgreSQL or MySQL in `.env`

### 4. Use Production Server

Use Gunicorn or uWSGI instead of Django's development server:

```bash
pip install gunicorn
gunicorn restaurant.wsgi:application
```

## Contributing

This is a production-ready backend system demonstrating:
- Django best practices
- RESTful API design
- Database modeling
- Business logic implementation
- Admin interface customization

## License

This project is provided as-is for educational and production use.

## Support

For issues or questions:
1. Check the Django documentation: https://docs.djangoproject.com/
2. Review Django REST Framework docs: https://www.django-rest-framework.org/
3. Check model validations and business logic in the code
