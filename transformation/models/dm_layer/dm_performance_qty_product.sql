SELECT
    EXTRACT(MONTH FROM CAST(order_date AS TIMESTAMP)) AS month,
    SUM(qty) AS Total_qty_Sold,
    SUM(unit_sales) AS Total_Sales
FROM
    {{ ref('fct_transactions')}}
GROUP BY
    month
ORDER BY
    month