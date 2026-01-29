from typing import List, Dict, Any
from app.db import get_db_connection

conn = get_db_connection()

def get_customers_by_credit_limit_range():
    """Return customers with credit limits outside the normal range."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT customerName, creditLimit
    FROM customers
    WHERE creditLimit < 10000 OR creditLimit > 100000
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_orders_with_null_comments():
    """Return orders that have null comments."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT orderNumber, comments
    FROM orders 
    WHERE comments IS NULL
    ORDER BY orderDate ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_first_5_customers():
    """Return the first 5 customers."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT customerName, contactLastName, contactFirstName
    FROM customers
    order by contactLastName
    LIMIT 5
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_payments_total_and_average():
    """Return total and average payment amounts."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT SUM(amount) as total_amount, AVG(amount) as avg_payments, MIN(amount) as min_payments, MAX(amount) as max_payments
    FROM payments
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_employees_with_office_phone():
    """Return employees with their office phone numbers."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT e.firstName, e.lastName, o.phone
    FROM employees e
    INNER JOIN offices o
    ON o.officeCode = e.officeCode
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_customers_with_shipping_dates():
    """Return customers with their order shipping dates."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT c.customerName, o.shippedDate
    FROM customers c
    LEFT JOIN orders o
    ON o.customerNumber = c.customerNumber
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_customer_quantity_per_order():
    """Return customer name and quantity for each order."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT c.customerName, SUM(od.quantityOrdered)
    FROM customers c
    JOIN orders o
    ON o.customerNumber = c.customerNumber
    JOIN orderdetails od
    ON od.orderNumber = o.orderNumber
    GROUP BY c.customerName
    ORDER BY c.customerName ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_customers_payments_by_lastname_pattern(pattern: str = "son"):
    """Return customers and payments for last names matching pattern."""
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT c.customerName AS customer_name, e.firstName AS Salesperson_name, SUM(p.amount) AS total_payments
    FROM customers c
    JOIN payments p
    ON p.customerNumber = c.customerNumber
    LEFT JOIN employees e
    ON e.employeeNumber = c.salesRepEmployeeNumber
    WHERE c.contactFirstName LIKE '%ly%' OR c.contactFirstName LIKE '%Mu%'
    GROUP BY c.customerName, e.firstName
    ORDER BY total_payments DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows
