-- Best seller produk
SELECT
    product_name,
    product_category_name,
    size,
    SUM(qty) AS Total_qty_Sold
FROM
    {{ ref('fct_transactions') }}
GROUP BY
    product_name, product_category_name
ORDER BY Total_Sales DESC
LIMIT 5;

-- Data penjualan berdasarkan provinsi
SELECT
    province_names,
    product_name,
    SUM(qty) AS total_quantity,
    SUM(unit_sales) AS total_sales
FROM
    {{ ref('fct_transactions') }}
GROUP BY
    province_names,
    product_name
ORDER BY
    province_names

-- Data penjualan berdasarkan waktu (bulan)
SELECT
    EXTRACT(MONTH FROM CAST(order_date AS TIMESTAMP)) AS Month,
    SUM(qty) AS Total_qty_Sold,
    SUM(unit_sales) AS Total_Sales
FROM
    {{ ref('fct_transactions')}}
GROUP BY
    Month
ORDER BY
    Month

-- Analisis Pelanggan: top 5 pelanggan yang paling banyak menghabiskan uang
SELECT
    name,
    SUM(unit_sales) AS Total_Sales
FROM
    {{ ref('fct_transactions')}}
GROUP BY
    name
ORDER BY 
    Total_Sales DESC
LIMIT 5

-- revenue penjualan tiap bulan dalam setahun
SELECT
    EXTRACT(MONTH FROM CAST(order_date AS TIMESTAMP)) AS month,
    SUM(unit_sales) AS total_revenue
FROM
    {{ ref('fct_transactions') }}
GROUP BY
    month
ORDER BY
    month
    
-- perbandingan pembelian produk berdasarkan gender
SELECT
    gender
    , SUM(unit_sales) as Total_Sales
from
    {{ ref('fct_transactions') }}
GROUP BY
    gender
