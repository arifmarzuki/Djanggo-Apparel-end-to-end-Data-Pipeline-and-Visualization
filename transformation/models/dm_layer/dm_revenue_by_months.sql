SELECT
    EXTRACT(MONTH from order_date) AS month,
    SUM(unit_sales) AS total_revenue
FROM
    {{ ref('fct_transactions') }}
GROUP BY
    month
ORDER BY
    month