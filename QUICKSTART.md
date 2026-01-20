# Quick Start Guide

Get the Restaurant Management System up and running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

For SQLite (default - no configuration needed):
```bash
# Skip this step, it will use SQLite by default
```

For PostgreSQL or MySQL:
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your database credentials
notepad .env
```

### 3. Setup Database

```bash
# Create database tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

Enter your admin credentials when prompted:
- Username: admin
- Email: admin@example.com
- Password: (choose a secure password)

### 4. Run Server

```bash
python manage.py runserver
```

## Access the Application

### Admin Panel
```
http://127.0.0.1:8000/admin/
```
Login with the superuser credentials you created.

### API Endpoints
```
http://127.0.0.1:8000/api/
```

## First Steps in Admin Panel

1. **Add Categories**: Go to Menu → Categories
   - Create categories like: Appetizers, Main Course, Desserts, Beverages

2. **Add Menu Items**: Go to Menu → Menu Items
   - Add food items with prices and details

3. **Add Tables**: Go to Reservations → Tables
   - Create tables with numbers and capacity

4. **Add Ingredients**: Go to Inventory → Ingredients
   - Add ingredients with stock levels

5. **Add Customers**: Go to Customers → Customers
   - Add customer information

## Testing the API

### Using Browser (DRF Browsable API)

Navigate to any endpoint in your browser:
- http://127.0.0.1:8000/api/menu/items/
- http://127.0.0.1:8000/api/orders/
- http://127.0.0.1:8000/api/customers/

You can interact with the API directly through the browsable interface.

### Using curl

Create a menu item:
```bash
curl -X POST http://127.0.0.1:8000/api/menu/items/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Burger\",\"description\":\"Classic beef burger\",\"category\":1,\"price\":\"9.99\",\"is_available\":true,\"preparation_time\":10}"
```

Create a customer:
```bash
curl -X POST http://127.0.0.1:8000/api/customers/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"phone\":\"+1234567890\"}"
```

Create an order:
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d "{\"customer\":1,\"table_number\":5,\"items\":[{\"menu_item\":1,\"quantity\":2}]}"
```

## Sample Data Setup

Load sample data to quickly test the system:

```bash
python manage.py load_sample_data
```

This will create:
- 4 menu categories (Appetizers, Main Course, Desserts, Beverages)
- 7 menu items with prices and details
- 5 ingredients with stock levels
- 10 tables (numbered 1-10)
- 3 sample customers (including 1 VIP)
- Links between menu items and their ingredients

## Common Commands

### Database Management
```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (WARNING: deletes all data)
python manage.py flush
```

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword admin
```

### Development
```bash
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

## API Authentication

All API endpoints require admin authentication. To authenticate:

1. **Via Browser**: Login to admin panel first, then access API endpoints
2. **Via curl**: Use session authentication or add token authentication

## Next Steps

1. Read the full [README.md](README.md) for detailed features
2. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference
3. Review [DEPLOYMENT.md](DEPLOYMENT.md) when ready for production

## Troubleshooting

### Port already in use
```bash
# Run on different port
python manage.py runserver 8080
```

### Database errors
```bash
# Delete database and start fresh
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Permission errors on Windows
Run Command Prompt or PowerShell as Administrator.

## Need Help?

- Check the error messages carefully
- Review the [README.md](README.md) documentation
- Ensure all dependencies are installed
- Verify Python version is 3.8 or higher

---

**You're all set!** Start managing your restaurant efficiently. 🍽️
