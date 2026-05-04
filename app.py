import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("📊 E-commerce Sales Dashboard")

# SQLite Connection - File based DB
def get_connection():
    return sqlite3.connect('ecommerce.db')

# Database + Data create kar de agar nahi hai
conn = get_connection()
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS customers
               (customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT, signup_date TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS products
               (product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT, price REAL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS orders
               (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS order_items
               (order_item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER, price REAL)''')

# Check karo data hai ya nahi
cursor.execute("SELECT COUNT(*) FROM customers")
if cursor.fetchone()[0] == 0:
    # Data insert kar do
    cursor.execute("INSERT INTO customers VALUES (1,'Amit Sharma','amit@gmail.com','Delhi','2023-01-15'),(2,'Priya Singh','priya@gmail.com','Mumbai','2023-02-20'),(3,'Rahul Verma','rahul@gmail.com','Bangalore','2023-03-10'),(4,'Sneha Patel','sneha@gmail.com','Delhi','2023-04-05'),(5,'Vikas Kumar','vikas@gmail.com','Pune','2023-05-12')")
    cursor.execute("INSERT INTO products VALUES (1,'iPhone 14','Electronics',79999),(2,'Samsung TV','Electronics',45000),(3,'Nike Shoes','Fashion',5999),(4,'Levis Jeans','Fashion',2499),(5,'Coffee Mug','Home',399)")
    cursor.execute("INSERT INTO orders VALUES (1,1,'2023-06-01','completed'),(2,2,'2023-06-05','completed'),(3,3,'2023-07-10','completed'),(4,1,'2023-07-15','completed'),(5,4,'2023-08-01','completed'),(6,5,'2023-08-10','completed'),(7,2,'2023-09-05','completed'),(8,3,'2023-09-12','completed'),(9,1,'2023-10-01','completed'),(10,4,'2023-10-15','completed')")
    cursor.execute("INSERT INTO order_items VALUES (1,1,1,1,79999),(2,1,5,2,399),(3,2,2,1,45000),(4,3,3,1,5999),(5,4,1,1,79999),(6,5,4,2,2499),(7,6,3,2,5999),(8,7,2,1,45000),(9,8,4,1,2499),(10,9,5,3,399),(11,10,1,1,79999)")
    conn.commit()
conn.close()

# 1. Month-wise Revenue
st.header("1. Month-wise Revenue")
query1 = """
SELECT
    strftime('%Y-%m', o.order_date) AS month,
    ROUND(SUM(oi.quantity * oi.price), 2) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY month
ORDER BY month;
"""
conn = get_connection()
df1 = pd.read_sql(query1, conn)
conn.close()
st.dataframe(df1, use_container_width=True)
fig1 = px.bar(df1, x='month', y='total_revenue', title='Monthly Revenue Trend')
st.plotly_chart(fig1, use_container_width=True)

# 2. Top 3 Customers
st.header("2. Top 3 Customers by Revenue")
query2 = """
SELECT
    c.name,
    ROUND(SUM(oi.quantity * oi.price), 2) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 3;
"""
conn = get_connection()
df2 = pd.read_sql(query2, conn)
conn.close()
st.dataframe(df2, use_container_width=True)

# 3. Best Selling Products
st.header("3. Best Selling Products")
query3 = """
SELECT
    p.product_name as name,
    p.category,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.quantity * oi.price), 2) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_quantity_sold DESC;
"""
conn = get_connection()
df3 = pd.read_sql(query3, conn)
conn.close()
st.dataframe(df3, use_container_width=True)
fig3 = px.bar(df3, x='name', y='total_quantity_sold', color='category', title='Products Sold by Category')
st.plotly_chart(fig3, use_container_width=True)

# 4. City-wise Revenue
st.header("4. City-wise Revenue")
query4 = """
SELECT
    c.city,
    ROUND(SUM(oi.quantity * oi.price), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.city
ORDER BY total_revenue DESC;
"""
conn = get_connection()
df4 = pd.read_sql(query4, conn)
conn.close()
st.dataframe(df4, use_container_width=True)
fig4 = px.pie(df4, names='city', values='total_revenue', title='Revenue by City')
st.plotly_chart(fig4, use_container_width=True)
