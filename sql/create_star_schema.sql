-- ============================================
-- Retail ETL & Data Warehouse Pipeline
-- Star Schema Design
-- ============================================

CREATE DATABASE IF NOT EXISTS retail_dw;

USE retail_dw;

-- ==========================
-- Customer Dimension
-- ==========================

CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE,
    customer_name VARCHAR(150),
    segment VARCHAR(50)
);

-- ==========================
-- Product Dimension
-- ==========================

CREATE TABLE dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE,
    product_name VARCHAR(255),
    category VARCHAR(100),
    sub_category VARCHAR(100)
);

-- ==========================
-- Store Dimension
-- ==========================

CREATE TABLE dim_store (
    store_key INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(100),
    market VARCHAR(100)
);

-- ==========================
-- Date Dimension
-- ==========================

CREATE TABLE dim_date (
    date_key INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE,
    ship_date DATE,
    year INT,
    week_num INT
);

-- ==========================
-- Sales Fact Table
-- ==========================

CREATE TABLE fact_sales (

    sales_key INT AUTO_INCREMENT PRIMARY KEY,

    order_id VARCHAR(50),

    customer_key INT,

    product_key INT,

    store_key INT,

    date_key INT,

    sales DECIMAL(12,2),

    profit DECIMAL(12,2),

    quantity INT,

    discount DECIMAL(5,2),

    shipping_cost DECIMAL(10,2),

    FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    FOREIGN KEY (product_key)
        REFERENCES dim_product(product_key),

    FOREIGN KEY (store_key)
        REFERENCES dim_store(store_key),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)

);