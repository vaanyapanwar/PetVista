-- PetVista Database Setup
-- Run this once to create the database and tables

CREATE DATABASE IF NOT EXISTS petvista;
USE petvista;

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    quantity INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    total_price DECIMAL(10,2),
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Sample data (optional)
INSERT IGNORE INTO products VALUES
  (1, 'Royal Canin Adult Dog Food', 'Food', 1299.00, 45),
  (2, 'Whiskas Tuna Cat Food', 'Food', 349.00, 80),
  (3, 'Pet Grooming Brush', 'Grooming', 499.00, 30),
  (4, 'Rope Tug Toy', 'Toys', 199.00, 60),
  (5, 'Tick & Flea Collar', 'Medicine', 249.00, 8),
  (6, 'Adjustable Harness (M)', 'Accessories', 699.00, 15);
