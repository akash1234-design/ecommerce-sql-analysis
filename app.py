import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")

st.title("📊 E-Commerce Sales Analysis Dashboard")
st.markdown("**MySQL + Streamlit | Project by Akash**")

# MySQL Connection - Yaha apna password daal
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="Akash@7830",  # <-- Apna MySQL password
        database="ecommerce_db"
    )

# Query run karne ka function
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Sidebar filters
st.sidebar.header("Filters")
analysis = st.sidebar.selectbox("Choose Analysis", [
    "Month-wise Revenue", 
    "Top 3 Customers", 
    "Best Selling Products",
    "Month-on-Month Growth",
    "City-wise Revenue"
])

# 1. Month-wise Revenue
if analysis == "Month-wise Revenue":
    st.subheader("📈 Month-wise Total Revenue")
    query = """
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        ROUND(SUM(total_amount), 2) AS total_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY month ORDER BY month;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)
    
    fig = px.bar(df, x='month', y='total_revenue', title='Revenue Trend')
    st.plotly_chart(fig, use_container_width=True)

# 2. Top 3 Customers
elif analysis == "Top 3 Customers":
    st.subheader("👑 Top 3 Customers by Spending")
    query = """
    SELECT 
        c.name,
        c.city,
        ROUND(SUM(o.total_amount), 2) AS total_spent,
        RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS customer_rank
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id
    LIMIT 3;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)
    
    fig = px.pie(df, values='total_spent', names='name', title='Top Customer Share')
    st.plotly_chart(fig, use_container_width=True)

# 3. Best Selling Products
elif analysis == "Best Selling Products":
    st.subheader("🔥 Best Selling Products by Quantity")
    query = """
    SELECT 
        p.name,
        p.category,
        SUM(oi.quantity) AS total_quantity_sold,
        ROUND(SUM(oi.quantity * oi.price), 2) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.product_id
    ORDER BY total_quantity_sold DESC;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# 4. Month-on-Month Growth
elif analysis == "Month-on-Month Growth":
    st.subheader("📊 Month-on-Month Revenue Growth")
    query = """
    WITH monthly_sales AS (
        SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
               SUM(total_amount) AS monthly_revenue
        FROM orders WHERE status = 'completed' GROUP BY month
    )
    SELECT month, monthly_revenue,
           LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month_revenue,
           ROUND((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) 
           / LAG(monthly_revenue) OVER (ORDER BY month) * 100, 2) AS growth_percent
    FROM monthly_sales ORDER BY month;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# 5. City-wise Revenue
elif analysis == "City-wise Revenue":
    st.subheader("🏙️ Revenue by City")
    query = """
    SELECT 
        c.city,
        ROUND(SUM(o.total_amount), 2) AS city_revenue,
        ROUND(SUM(o.total_amount) * 100.0 / SUM(SUM(o.total_amount)) OVER (), 2) AS percentage
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.city ORDER BY city_revenue DESC;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)
    
    fig = px.bar(df, x='city', y='city_revenue', title='City-wise Revenue')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**GitHub:** [github.com/akash1234-design/ecommerce-sql-analysis](https://github.com/akash1234-design/ecommerce-sql-analysis)")
