# Project: Inventory Management REST API

Build a complete inventory management REST API using Python and FastAPI.

---

## Autonomous Operation

**Execute this task completely without user interaction:**

1. **Proceed autonomously** - Make reasonable decisions without asking
2. **Implement all requirements** - Complete every feature listed below
3. **Write working code** - All endpoints must return valid responses
4. **Include tests** - Aim for 80%+ coverage
5. **Handle errors gracefully** - Proper HTTP status codes and messages

**Prioritized execution order:**
1. Project structure and database setup
2. Product CRUD operations
3. Category CRUD with hierarchy
4. Stock IN/OUT operations
5. Low stock alerts endpoint
6. Reports (valuation, movement, top products)
7. Authentication (API key)
8. Tests

---

## Requirements

### Core Features

1. **Product Management**
   - CRUD operations for products (name, SKU, price, quantity, category)
   - SKU must be unique and validated (format: XXX-NNNN)
   - Price validation (positive, max 2 decimal places)
   - Quantity cannot be negative

2. **Category Management**
   - CRUD for categories (name, description, parent_category_id for hierarchy)
   - Categories can be nested (max 3 levels)
   - Cannot delete category with products

3. **Stock Operations**
   - Record stock IN (purchase/return) and OUT (sale/damage)
   - Each transaction: product_id, quantity, type, timestamp, notes
   - Automatic quantity updates on products table
   - Transaction history with filtering by date range, product, type

4. **Low Stock Alerts**
   - Each product has reorder_level field
   - Endpoint to get all products below reorder level
   - Include current quantity and how much below threshold

5. **Reports**
   - Inventory valuation: total value per category and overall
   - Stock movement summary: daily/weekly/monthly totals
   - Top selling products (by quantity moved OUT)

### Technical Requirements

- FastAPI with async SQLAlchemy
- SQLite database with migrations (Alembic)
- Pydantic models with validation
- Proper error handling with custom exceptions
- API documentation via OpenAPI
- Pagination on list endpoints
- Basic auth with API key header
- Tests with pytest (aim for 80%+ coverage)

### Project Structure

```
inventory_api/
├── src/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── database.py       # DB connection
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routers/          # API routes
│   ├── services/         # Business logic
│   └── exceptions.py     # Custom exceptions
├── tests/
├── alembic/
└── pyproject.toml
```

### API Endpoints

```
GET/POST           /products
GET/PUT/DELETE     /products/{id}
GET                /products/low-stock
GET/POST           /categories
GET/PUT/DELETE     /categories/{id}
POST               /stock/in
POST               /stock/out
GET                /stock/transactions
GET                /reports/valuation
GET                /reports/movement
GET                /reports/top-products
```

---

## Success Criteria

| Priority | Requirement | Validation |
|----------|-------------|------------|
| P0 | All CRUD endpoints functional | HTTP 200/201 responses |
| P0 | Proper HTTP status codes | 201 create, 404 not found, 400 validation |
| P0 | Input validation with meaningful errors | Invalid SKU/price rejected |
| P1 | Stock operations update quantities | Product quantity changes |
| P1 | No N+1 query problems | Check query count |
| P2 | Reports return accurate data | Sum/count calculations correct |
| P2 | 80%+ test coverage | pytest-cov report |

**Deliverables:** Working REST API, database migrations, test suite, OpenAPI docs.
