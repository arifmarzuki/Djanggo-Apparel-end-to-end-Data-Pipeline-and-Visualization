SELECT
    gender
    , SUM(unit_sales) as Total_Sales
from
    {{ ref('fct_transactions') }}
GROUP BY
    gender