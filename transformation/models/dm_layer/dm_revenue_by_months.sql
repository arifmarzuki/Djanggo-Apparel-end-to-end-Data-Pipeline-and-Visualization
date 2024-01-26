SELECT
    EXTRACT(MONTH FROM CAST(order_date AS TIMESTAMP)) AS month, --extract mengambil bulannya saja, date trunc di ambil di awal tanggal bulan tsb
    SUM(unit_sales) AS total_revenue
FROM
    {{ ref('fct_transactions') }}
GROUP BY
    month
ORDER BY
    month