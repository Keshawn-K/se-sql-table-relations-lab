# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return first and last names and job titles for all employees in Boston
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees e
    INNER JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Are there any offices that have zero employees?
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
""", conn)

# STEP 3
# Return employees with city and state of office (if they have one), ordered by first name then last name
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Return customers with no orders and their sales rep employee number
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5
# Return customer contacts with payment info, sorted by amount (descending)
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.paymentDate, p.amount
    FROM customers c
    INNER JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Return top 4 employees with highest average credit limit from their customers
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) as numCustomers
    FROM employees e
    INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY COUNT(c.customerNumber) DESC
""", conn)

# STEP 7
# Return product name with order count and total units sold
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(DISTINCT o.orderNumber) as numorders, SUM(od.quantityOrdered) as totalunits
    FROM products p
    INNER JOIN orderdetails od ON p.productCode = od.productCode
    INNER JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Return product name/code with distinct customer count who ordered each product
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) as numpurchasers
    FROM products p
    INNER JOIN orderdetails od ON p.productCode = od.productCode
    INNER JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Return count of customers per office
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) as n_customers
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode
""", conn)

# STEP 10
# Return employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    FROM employees e
    INNER JOIN offices o ON e.officeCode = o.officeCode
    INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    INNER JOIN orders ord ON c.customerNumber = ord.customerNumber
    INNER JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT p.productCode
        FROM products p
        INNER JOIN orderdetails od2 ON p.productCode = od2.productCode
        INNER JOIN orders o2 ON od2.orderNumber = o2.orderNumber
        GROUP BY p.productCode
        HAVING COUNT(DISTINCT o2.customerNumber) < 20
    )
    GROUP BY e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    ORDER BY e.lastName
""", conn)

conn.close()