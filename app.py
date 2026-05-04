import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("📊 E-commerce Sales Dashboard")

# MySQL Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akash@7830",  # <-- Yaha apna MySQL ka password daal de
        database="ecommerce"
    )

# 1. Month-wise Revenue
st.header("1. Month-wise Revenue")
query1 = """
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
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
st.bar_chart(df1.set_index('month'))

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
st.bar_chart(df3.set_index('name')['total_quantity_sold'])

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
st.bar_chart(df4.set_index('city'))
