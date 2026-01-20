# API Documentation - Restaurant Management System

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
All endpoints require admin authentication. Use Django session authentication by logging in to the admin panel first.

## Response Format
All responses are in JSON format.

### Success Response
```json
{
  "id": 1,
  "name": "Example",
  "created_at": "2026-01-19T10:00:00Z"
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

---

## Menu Management API

### Categories

#### List Categories
```http
GET /api/menu/categories/
```

Query Parameters:
- `is_active` - Filter by active status (true/false)
- `search` - Search in name and description
- `ordering` - Sort by: name, created_at

Response:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Appetizers",
      "description": "Starters and small plates",
      "is_active": true,
      "items_count": 8,
      "created_at": "2026-01-19T10:00:00Z",
      "updated_at": "2026-01-19T10:00:00Z"
    }
  ]
}
```

#### Create Category
```http
POST /api/menu/categories/
Content-Type: application/json

{
  "name": "Desserts",
  "description": "Sweet treats and pastries",
  "is_active": true
}
```

#### Get Category Items
```http
GET /api/menu/categories/{id}/items/
```

Returns all available menu items in this category.

### Menu Items

#### List Menu Items
```http
GET /api/menu/items/
```

Query Parameters:
- `category` - Filter by category ID
- `is_available` - Filter by availability
- `is_vegetarian` - Filter vegetarian items
- `is_vegan` - Filter vegan items
- `search` - Search in name and description
- `ordering` - Sort by: name, price, created_at

#### Create Menu Item
```http
POST /api/menu/items/
Content-Type: multipart/form-data

{
  "name": "Margherita Pizza",
  "description": "Classic pizza with tomato, mozzarella, and basil",
  "category": 1,
  "price": "12.99",
  "image": <file>,
  "is_available": true,
  "is_vegetarian": true,
  "is_vegan": false,
  "preparation_time": 15
}
```

#### Get Menu Item Details
```http
GET /api/menu/items/{id}/
```

Response includes ingredient information:
```json
{
  "id": 1,
  "name": "Margherita Pizza",
  "description": "Classic pizza",
  "category": 1,
  "category_name": "Main Course",
  "price": "12.99",
  "image": "/media/menu_items/pizza.jpg",
  "is_available": true,
  "is_vegetarian": true,
  "is_vegan": false,
  "preparation_time": 15,
  "ingredients": [
    {
      "id": 1,
      "ingredient": 1,
      "ingredient_name": "Pizza Dough",
      "quantity_required": "0.30",
      "unit": "KG"
    }
  ],
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T10:00:00Z"
}
```

#### Get Available Items Only
```http
GET /api/menu/items/available/
```

#### Toggle Item Availability
```http
POST /api/menu/items/{id}/toggle_availability/
```

---

## Order Management API

### Orders

#### List Orders
```http
GET /api/orders/
```

Query Parameters:
- `status` - Filter by status (PENDING, PREPARING, COMPLETED, CANCELLED)
- `customer` - Filter by customer ID
- `table_number` - Filter by table
- `search` - Search customer name/email
- `ordering` - Sort by: created_at, total, status

#### Create Order
```http
POST /api/orders/
Content-Type: application/json

{
  "customer": 1,
  "table_number": 5,
  "notes": "Extra cheese on pizza",
  "discount": 5.00,
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
}
```

Response:
```json
{
  "id": 15,
  "customer": 1,
  "customer_name": "John Doe",
  "status": "PENDING",
  "table_number": 5,
  "notes": "Extra cheese on pizza",
  "subtotal": "38.97",
  "tax": "3.90",
  "discount": "5.00",
  "total": "37.87",
  "items_count": 2,
  "created_at": "2026-01-19T12:30:00Z",
  "updated_at": "2026-01-19T12:30:00Z"
}
```

#### Get Order Details
```http
GET /api/orders/{id}/
```

Returns full order with all items and customer details.

#### Update Order Status
```http
POST /api/orders/{id}/update_status/
Content-Type: application/json

{
  "status": "PREPARING"
}
```

Valid statuses: PENDING, PREPARING, COMPLETED, CANCELLED

#### Add Item to Order
```http
POST /api/orders/{id}/add_item/
Content-Type: application/json

{
  "menu_item": 5,
  "quantity": 1,
  "special_instructions": "No onions"
}
```

#### Get Order Statistics
```http
GET /api/orders/statistics/
```

Response:
```json
{
  "total_orders": 150,
  "total_revenue": "15234.50",
  "pending_orders": 8,
  "preparing_orders": 12
}
```

---

## Inventory Management API

### Ingredients

#### List Ingredients
```http
GET /api/inventory/ingredients/
```

Query Parameters:
- `unit` - Filter by unit type
- `search` - Search name and supplier
- `ordering` - Sort by: name, current_stock, minimum_stock

Response:
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "name": "Pizza Dough",
      "unit": "KG",
      "current_stock": "15.50",
      "minimum_stock": "10.00",
      "cost_per_unit": "2.50",
      "supplier": "Bakery Supplies Co.",
      "stock_status": "OK",
      "is_low_stock": false,
      "last_restocked": "2026-01-18T08:00:00Z",
      "created_at": "2026-01-10T10:00:00Z",
      "updated_at": "2026-01-18T08:00:00Z"
    }
  ]
}
```

#### Get Low Stock Items
```http
GET /api/inventory/ingredients/low_stock/
```

Returns ingredients where current_stock <= minimum_stock

#### Restock Ingredient
```http
POST /api/inventory/ingredients/{id}/restock/
Content-Type: application/json

{
  "quantity": 20.00,
  "notes": "Weekly delivery from supplier"
}
```

### Stock Transactions

#### List Transactions
```http
GET /api/inventory/transactions/
```

Query Parameters:
- `ingredient` - Filter by ingredient ID
- `transaction_type` - Filter by type (PURCHASE, USED, WASTE, ADJUSTMENT)
- `ordering` - Sort by: created_at

#### Create Manual Transaction
```http
POST /api/inventory/transactions/
Content-Type: application/json

{
  "ingredient": 1,
  "transaction_type": "ADJUSTMENT",
  "quantity": 5.00,
  "notes": "Stock correction after inventory check",
  "created_by": "admin"
}
```

Transaction Types:
- `PURCHASE` - Adds to stock
- `ADJUSTMENT` - Adds to stock (manual correction)
- `USED` - Deducts from stock (automatic on orders)
- `WASTE` - Deducts from stock (spoilage)

---

## Reservation Management API

### Tables

#### List Tables
```http
GET /api/reservations/tables/
```

Query Parameters:
- `is_available` - Filter by availability
- `capacity` - Filter by capacity
- `ordering` - Sort by: table_number, capacity

#### Check Available Tables
```http
GET /api/reservations/tables/available/?date=2026-01-25&time=19:00
```

Returns tables not reserved at the specified date and time.

#### Create Table
```http
POST /api/reservations/tables/
Content-Type: application/json

{
  "table_number": 10,
  "capacity": 4,
  "is_available": true,
  "location": "Window seat"
}
```

### Reservations

#### List Reservations
```http
GET /api/reservations/
```

Query Parameters:
- `status` - Filter by status
- `customer` - Filter by customer ID
- `table` - Filter by table ID
- `reservation_date` - Filter by date (YYYY-MM-DD)
- `search` - Search customer name/email
- `ordering` - Sort by: reservation_date, reservation_time, created_at

#### Create Reservation
```http
POST /api/reservations/
Content-Type: application/json

{
  "customer": 1,
  "table": 3,
  "reservation_date": "2026-01-25",
  "reservation_time": "19:00",
  "number_of_guests": 4,
  "special_requests": "Window seat if possible, birthday celebration"
}
```

Validations:
- Guest count must not exceed table capacity
- Prevents overlapping reservations (2-hour buffer)

#### Update Reservation Status
```http
POST /api/reservations/{id}/update_status/
Content-Type: application/json

{
  "status": "CONFIRMED"
}
```

Valid statuses: PENDING, CONFIRMED, SEATED, COMPLETED, CANCELLED, NO_SHOW

#### Get Today's Reservations
```http
GET /api/reservations/today/
```

#### Get Upcoming Reservations
```http
GET /api/reservations/upcoming/
```

Returns confirmed and pending reservations from today onwards.

---

## Customer Management API

### Customers

#### List Customers
```http
GET /api/customers/
```

Query Parameters:
- `is_vip` - Filter VIP customers
- `search` - Search name, email, phone
- `ordering` - Sort by: name, created_at, loyalty_points

Response:
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "address": "123 Main St",
      "date_of_birth": "1990-05-15",
      "loyalty_points": 125,
      "is_vip": true,
      "notes": "Allergic to peanuts",
      "total_orders": 15,
      "total_spent": "1250.00",
      "created_at": "2025-12-01T10:00:00Z",
      "updated_at": "2026-01-19T12:00:00Z"
    }
  ]
}
```

#### Create Customer
```http
POST /api/customers/
Content-Type: application/json

{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1987654321",
  "address": "456 Oak Ave",
  "date_of_birth": "1985-08-20",
  "notes": "Prefers vegetarian options"
}
```

#### Get Customer Details
```http
GET /api/customers/{id}/
```

Returns customer with recent orders and reservations.

#### Get VIP Customers
```http
GET /api/customers/vip/
```

#### Get Customer Order History
```http
GET /api/customers/{id}/order_history/
```

#### Get Customer Reservation History
```http
GET /api/customers/{id}/reservation_history/
```

#### Add Loyalty Points
```http
POST /api/customers/{id}/add_loyalty_points/
Content-Type: application/json

{
  "points": 50
}
```

Note: Points are automatically added when orders are completed (1 point per $10).

---

## Filtering and Pagination

### Pagination
All list endpoints support pagination:
```http
GET /api/menu/items/?page=2
```

Default page size: 20 items

### Search
Use the `search` parameter:
```http
GET /api/menu/items/?search=pizza
```

### Ordering
Use the `ordering` parameter:
```http
GET /api/orders/?ordering=-created_at
```

Prefix with `-` for descending order.

### Multiple Filters
Combine filters:
```http
GET /api/menu/items/?category=1&is_vegetarian=true&ordering=price
```

---

## Error Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - No permission
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

No rate limiting is currently implemented. Consider adding it for production.

## Webhooks

Not currently supported. Can be added for order notifications.
