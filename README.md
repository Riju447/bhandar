# Smart Inventory Management System

A Django-based inventory management system with modular apps for accounts, dashboard, products, categories, brands, suppliers, purchases, sales, inventory, reports, notifications, and settings.

## Features
- Authentication and user management
- Dashboard with summary cards
- Product CRUD and inventory tracking
- Admin-ready Django models for purchases, sales, suppliers, and settings

## Run locally
1. Create and activate a virtual environment if desired.
2. Install dependencies: `pip install Django reportlab openpyxl pillow`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`

## Notes
- The base UI uses Bootstrap via MDBootstrap-style markup plus simple custom CSS.
- Media uploads are served from the `media/` directory during development.
