with fct_transaction as (
select
    o.*,
    od.order_detail_id ,
    od.product_id ,
    od.qty ,
    od.item_price ,
    od.unit_sales 
from
    orders o
join
    order_details od on o.order_id = od.order_id
)
select
    DATE_TRUNC('month', ft.order_date) as month,
    SUM(ft.qty * ft.item_price) as total_revenue
from
    fct_transaction ft
group by
    month