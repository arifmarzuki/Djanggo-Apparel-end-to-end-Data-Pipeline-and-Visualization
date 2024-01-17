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