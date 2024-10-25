# ShelfLife - Inventory & Sales Management System

ShelfLife is a comprehensive inventory management solution designed for small-scale manufacturers and retailers. Our mission is to simplify inventory tracking and empower businesses with the tools they need to succeed.

## Features

- Real-time inventory tracking
- Sales and transaction management
- Product categorization
- Low stock alerts
- Daily and monthly reports
- User-friendly interface

## Tech Stack

- Backend: Flask, SQLAlchemy
- Frontend: Bootstrap 5, JavaScript
- Database: SQLite 
- Additional: Flask-Marshmallow, Flask-CORS

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update variables as needed
   ```
   DATABASE_URL=sqlite:///inventory.db
   SECRET_KEY=your-secret-key
   ```
5. Run the application:
   ```bash
   python run.py
   ```
