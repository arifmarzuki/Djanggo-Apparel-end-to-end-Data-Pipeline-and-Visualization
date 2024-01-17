SELECT
    CONCAT(product_name, '-', product_category_name, '-', size) AS product
    , SUM(qty) AS Total_qty_Sold
FROM
    {{ ref('fct_transactions') }}
GROUP BY
    product
ORDER BY Total_qty_Sold DESC
LIMIT 5