USE ecommerce;

INSERT INTO customers VALUES
(1, 'Rahul Sharma', 'rahul@gmail.com', 'Delhi', '2024-01-15'),
(2, 'Priya Singh', 'priya@gmail.com', 'Mumbai', '2024-02-20'),
(3, 'Amit Kumar', 'amit@gmail.com', 'Hisar', '2024-03-10'),
(4, 'Sneha Patel', 'sneha@gmail.com', 'Ahmedabad', '2024-01-05'),
(5, 'Vikash Yadav', 'vikash@gmail.com', 'Lucknow', '2024-04-01');

INSERT INTO products VALUES
(101, 'iPhone 15', 'Electronics', 79900.00),
(102, 'Samsung TV', 'Electronics', 45000.00),
(103, 'Nike Shoes', 'Fashion', 7999.00),
(104, 'Levis Jeans', 'Fashion', 3999.00),
(105, 'Pressure Cooker', 'Home', 2499.00);

INSERT INTO orders VALUES
(1001, 1, '2024-05-01', 79900.00, 'delivered'),
(1002, 2, '2024-05-02', 52999.00, 'delivered'),
(1003, 3, '2024-05-03', 7999.00, 'shipped'),
(1004, 1, '2024-05-10', 3999.00, 'delivered'),
(1005, 4, '2024-05-15', 2499.00, 'cancelled'),
(1006, 5, '2024-06-01', 45000.00, 'delivered');

INSERT INTO order_items VALUES
(1, 1001, 101, 1, 79900.00),
(2, 1002, 102, 1, 45000.00),
(3, 1002, 103, 1, 7999.00),
(4, 1003, 103, 1, 7999.00),
(5, 1004, 104, 1, 3999.00),
(6, 1005, 105, 1, 2499.00),
(7, 1006, 102, 1, 45000.00);