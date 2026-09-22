# Mock database for customer details, order history, and addresses
MOCK_CUSTOMERS = {
    "CUST-1001": {
        "name": "Sarah Ahmed",
        "email": "sarah.ahmed@example.com",
        "phone": "+92 300 1234567",
        "address": "House 45, Street 12, F-7/2, Islamabad, Pakistan",
        "orders": [
            {
                "order_id": "ORD-9921",
                "item": "Wireless Noise-Canceling Headphones",
                "price": "$150.00",
                "status": "In Transit",
                "estimated_delivery": "2026-09-25",
            },
            {
                "order_id": "ORD-8810",
                "item": "Mechanical Keyboard",
                "price": "$85.00",
                "status": "Delivered",
                "estimated_delivery": "2026-09-10",
            },
        ],
    },
    "CUST-1002": {
        "name": "Ali Raza",
        "email": "ali.raza@example.com",
        "phone": "+92 321 7654321",
        "address": "Apartment 4B, Gulberg III, Lahore, Pakistan",
        "orders": [
            {
                "order_id": "ORD-7743",
                "item": "Ergonomic Office Chair",
                "price": "$210.00",
                "status": "Processing",
                "estimated_delivery": "2026-09-28",
            }
        ],
    },
}


def get_customer_info(customer_id: str) -> dict | None:
    """Fetch customer profile and orders by Customer ID."""
    return MOCK_CUSTOMERS.get(customer_id.strip().upper())
