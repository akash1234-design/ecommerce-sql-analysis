# E-Commerce Sales Analysis using MySQL

## 📊 Project Overview
Designed and queried a relational database for an e-commerce platform to derive business insights on revenue, customers, and products. This project demonstrates SQL skills in data modeling, complex joins, CTEs, and window functions.

## 🛠️ Tech Stack
- **Database:** MySQL 8.0
- **Tools:** MySQL Workbench
- **Concepts:** Database Design, Foreign Keys, JOINs, GROUP BY, CTE, Window Functions

## 🗂️ Database Schema
The database consists of 4 relational tables with proper constraints:

**1. customers** - Stores customer information
**2. products** - Product catalog with categories and pricing  
**3. orders** - Order header with customer reference and status
**4. order_items** - Line items for each order with product reference

**ER Diagram:** `customers` 1:N `orders` 1:N `order_items` N:1 `products`

## 📈 Key Business Questions Solved

| Query | Business Question | SQL Concept Used |
| --- | --- | --- |
| 1 | Month-over-Month Revenue Trend | GROUP BY, DATE_FORMAT |
| 2 | Top 3 High-Value Customers | JOIN, ORDER BY, LIMIT |
| 3 | Best Selling Products by Quantity | JOIN 3 Tables, SUM |
| 4 | Best Selling Products by Revenue | Aggregate Functions |
| 5 | Customer Ranking by Spending | Window Function RANK() |
| 6 | Category-wise Revenue Contribution % | Window Function OVER() |
| 7 | Sales Performance by Price Range | CASE WHEN, GROUP BY |
| 8 | MoM Growth Percentage | CTE, LAG() Window Function |

## 💡 Key Insights from Analysis
1. **Revenue:** May 2024 generated ₹1,36,898 from 3 delivered orders vs ₹45,000 in June
2. **Top Customer:** Rahul Sharma from Delhi contributed ₹83,899 with 2 orders - 61% of total revenue
3. **Top Category:** Electronics drove 84% of revenue share
4. **Star Product:** iPhone 15 generated highest revenue ₹79,900 despite only 1 unit sold
5. **Price Range:** Products above ₹50K contributed maximum revenue

## 🚀 How to Run This Project

**Step 1: Create Database & Tables**
```sql
Run 01_schema.sql