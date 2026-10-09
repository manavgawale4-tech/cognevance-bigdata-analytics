CREATE DATABASE IF NOT EXISTS ecommerce_analytics;

USE ecommerce_analytics;

SELECT DATABASE();

USE ecommerce_analytics;

-- 1. Total orders
SELECT COUNT(*) AS total_orders
FROM olist_orders_dataset;

-- 2. Total customers
SELECT COUNT(*) AS total_customers
FROM olist_customers_dataset;

-- 3. Order status distribution
SELECT order_status, COUNT(*) AS total_orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY total_orders DESC;

-- 4. Payment type distribution
SELECT payment_type, COUNT(*) AS total_payments
FROM olist_order_payments_dataset
GROUP BY payment_type
ORDER BY total_payments DESC;

-- 5. Top 10 product categories by number of products
SELECT product_category_name, COUNT(*) AS total_products
FROM olist_products_dataset
GROUP BY product_category_name
ORDER BY total_products DESC
LIMIT 10;

-- 6. Count unique customers
SELECT COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM olist_customers_dataset;

-- 7. Total product revenue
SELECT ROUND(SUM(price), 2) AS total_product_revenue
FROM olist_order_items_dataset;

-- 8. Revenue by product category
SELECT
    p.product_category_name,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM olist_order_items_dataset oi
JOIN olist_products_dataset p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;

-- 9. Monthly revenue trend
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    ROUND(SUM(oi.price), 2) AS monthly_revenue
FROM olist_orders_dataset o
JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY month;

-- 10. Delivery performance analysis
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS avg_delivery_days
FROM olist_orders_dataset
WHERE order_status = 'delivered'
GROUP BY order_status;

-- 11. Payment method revenue analysis
SELECT
    payment_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS average_payment_value
FROM olist_order_payments_dataset
GROUP BY payment_type
ORDER BY total_payment_value DESC;

-- 12. Top 10 states by customer count
SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;

-- 13. Check missing delivery dates
SELECT
    COUNT(*) AS missing_delivery_dates
FROM olist_orders_dataset
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NULL;