USE ecommerce;

-- Q1: Month-wise Revenue
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(order_id) AS total_orders, SUM(total_amount) AS total_revenue
FROM orders WHERE status = 'delivered' GROUP BY month ORDER BY month;

-- Q2: Top 3 Customers
SELECT c.name, c.city, COUNT(o.order_id) AS total_orders, SUM(o.total_amount) AS total_spent
FROM customers c JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'delivered' GROUP BY c.customer_id, c.name, c.city ORDER BY total_spent DESC LIMIT 3;

-- Q3: Best Selling by Quantity
SELECT p.product_name, p.category, SUM(oi.quantity) AS units_sold, SUM(oi.quantity * oi.price) AS revenue_from_product
FROM order_items oi JOIN products p ON oi.product_id = p.product_id JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'delivered' GROUP BY p.product_id, p.product_name, p.category ORDER BY units_sold DESC;

-- Q4: Best Selling by Revenue
SELECT p.product_name, p.category, SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items oi JOIN products p ON oi.product_id = p.product_id JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'delivered' GROUP BY p.product_id, p.product_name, p.category ORDER BY total_revenue DESC;

-- Q5: Customer Ranking using Window Function
SELECT c.name, SUM(o.total_amount) AS total_spent, RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS spending_rank
FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'delivered' GROUP BY c.customer_id, c.name;

-- Q6: Category Revenue %
SELECT p.category, SUM(oi.quantity * oi.price) AS category_revenue,
ROUND(SUM(oi.quantity * oi.price) * 100.0 / SUM(SUM(oi.quantity * oi.price)) OVER (), 2) AS revenue_percent
FROM order_items oi JOIN products p ON oi.product_id = p.product_id JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'delivered' GROUP BY p.category ORDER BY category_revenue DESC;

-- Q7: Price Range Analysis
SELECT CASE WHEN p.price < 5000 THEN 'Under 5K' WHEN p.price BETWEEN 5000 AND 20000 THEN '5K-20K'
WHEN p.price BETWEEN 20000 AND 50000 THEN '20K-50K' ELSE 'Above 50K' END AS price_range,
COUNT(DISTINCT oi.order_id) AS total_orders, SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items oi JOIN products p ON oi.product_id = p.product_id JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'delivered' GROUP BY price_range ORDER BY total_revenue DESC;

-- Q8: MoM Growth using CTE + LAG
WITH monthly_sales AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue
    FROM orders WHERE status = 'delivered' GROUP BY month
)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100, 2) AS growth_percent
FROM monthly_sales;