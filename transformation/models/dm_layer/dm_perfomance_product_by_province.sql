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