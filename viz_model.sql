-- Data penjualan berdasarkan produk
SELECT
    p.product_id,
    p.product_name,
    pc.product_category_name,
    SUM(od.qty) AS Total_qty_Sold,
    SUM(od.unit_sales) AS Total_Sales
FROM
    products p
    JOIN order_details od ON p.product_id = od.product_id
    JOIN product_categories pc ON p.product_category_id = pc.product_category_id
GROUP BY
    p.product_id, p.product_name, pc.product_category_name
ORDER BY Total_Sales DESC
LIMIT 5;

-- Data penjualan berdasarkan provinsi
SELECT
    pr.province_id,
    pr.province_name,
    SUM(od.qty) AS Total_qty_Sold,
    SUM(od.unit_sales) AS Total_Sales
FROM
    orders o
    JOIN order_details od ON o.order_id = od.order_id
    JOIN provinces pr ON o.province_id = pr.province_id
GROUP BY
    pr.province_id, pr.province_name
ORDER BY Total_Sales DESC
LIMIT 5;

-- Data penjualan berdasarkan waktu (bulan)
SELECT
    DATE_TRUNC('month', o.order_date) AS Month,
    SUM(od.qty) AS Total_qty_Sold,
    SUM(od.unit_sales) AS Total_Sales
FROM
    orders o
    JOIN order_details od ON o.order_id = od.order_id
GROUP BY
    Month
ORDER BY
    Month;

-- Analisis Pelanggan:
-- Total belanja per pelanggan.
-- Jumlah pesanan per pelanggan.
-- Produk paling sering dibeli oleh pelanggan.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS Total_Orders,
    SUM(od.unit_sales) AS Total_Sales
FROM
    customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_details od ON o.order_id = od.order_id
GROUP BY
    c.customer_id, c.first_name, c.last_name
ORDER BY Total_Sales DESC
LIMIT 10;

-- Analisis Kategori Produk:
-- Total penjualan per kategori produk.
-- Jumlah produk terjual per kategori.
SELECT
    pc.product_category_id,
    pc.product_category_name,
    SUM(od.unit_sales) AS Total_Sales,
    COUNT(DISTINCT p.product_id) AS Total_Products_Sold
FROM
    product_categories pc
    JOIN products p ON pc.product_category_id = p.product_category_id
    JOIN order_details od ON p.product_id = od.product_id
GROUP BY
    pc.product_category_id, pc.product_category_name;

-- Analisis Waktu:
-- Jumlah pesanan dan penjualan bulanan
SELECT
    DATE_TRUNC('month', o.order_date) AS Month,
    COUNT(o.order_id) AS Total_Orders,
    SUM(od.unit_sales) AS Total_Sales
FROM
    orders o
    JOIN order_details od ON o.order_id = od.order_id
GROUP BY
    Month
ORDER BY
    Month DESC;

-- Analisis Kinerja Produk:
-- Produk terlaris berdasarkan jumlah terjual.
-- Produk dengan pendapatan tertinggi.
SELECT
    p.product_id,
    p.product_name,
    SUM(od.qty) AS Total_qty_Sold,
    SUM(od.unit_sales) AS Total_Sales
FROM
    products p
    JOIN order_details od ON p.product_id = od.product_id
GROUP BY
    p.product_id, p.product_name
ORDER BY
    Total_qty_Sold DESC;
