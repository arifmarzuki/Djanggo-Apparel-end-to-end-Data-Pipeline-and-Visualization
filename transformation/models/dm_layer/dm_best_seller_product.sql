SELECT
    product_name,
    product_category_name,
    size,
    SUM(qty) AS Total_qty_Sold
FROM
    {{ ref('fct_transactions') }}
GROUP BY
    product_name, product_category_name
ORDER BY Total_qty_Sold DESC
LIMIT 5