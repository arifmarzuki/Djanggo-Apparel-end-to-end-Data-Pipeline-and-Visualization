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
    p.product_name,
    c.city_names,
    count(ft.product_id) as product_count
from
    fct_transaction ft
join
    products p on p.product_id = ft.product_id
join
    cities c on c.city_id = ft.city_id
group by
    p.product_id, c.city_id, p.product_name, c.city_names
