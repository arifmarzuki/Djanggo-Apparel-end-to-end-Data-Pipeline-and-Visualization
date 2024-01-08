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