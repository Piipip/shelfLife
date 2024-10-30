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

## Usage

1. **Start the Application**
   ```bash
   python3 app.py
   ```
   Access the application at `http://localhost:5000`

2. **API Endpoints**

   Products:
   - GET `/api/products/` - List all products
   - POST `/api/products/` - Create new product
   - PUT `/api/products/<id>` - Update product
   - DELETE `/api/products/<id>` - Delete product

   Sales:
   - GET `/api/sales/` - List all sales
   - POST `/api/sales/` - Record new sale

   Reports:
   - GET `/api/reports/daily` - Get daily report
   - GET `/api/reports/monthly` - Get monthly report

3. **Frontend Routes**
   - `/` - Landing page
   - `/dashboard` - Main dashboard
   - `/products` - Product management
   - `/sales` - Sales operations
   - `/reports` - Reports and analytics

## Development

- Run in debug mode: `python3 app.py`
- Application will auto-reload on code changes
- SQLite database file is created in the root directory

## Error Handling

The application includes comprehensive error handling:
- Input validation
- Database constraints
- Stock level verification
- Transaction rollbacks
- User-friendly error messages

## Security Features

- CORS protection
- SQL injection prevention through SQLAlchemy
- Environment variable management
- Input sanitization
- Transaction integrity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Created by [Piipip](https://github.com/Piipip)  
Follow me on Twitter: [@philipkorans](https://twitter.com/philipkorans)
