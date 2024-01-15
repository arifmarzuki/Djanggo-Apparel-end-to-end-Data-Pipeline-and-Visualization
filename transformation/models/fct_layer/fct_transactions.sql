select
    od.order_id
    , od.order_detail_id
    , o.customer_id
    , od.product_id
    , dl.city_id
    , dl.province_id
    , dp.product_category_id
    , o.order_date
    , CONCAT(dc.first_name,' ', dc.last_name) AS name
    , dc.gender
    , dl.city_names
    , dl.province_names
    , dp.product_name
    , dp.product_category_name
    , dp.size
    , dp.price
    , od.qty
    , od.item_price
    , od.unit_sales 
from
    order_details od
join
    orders as o
    on
        od.order_id = o.order_id
join
    {{ ref('dim_customers')}} as dc
    on
        dc.customer_id = o.customer_id
join
    {{ ref('dim_location')}} as dl
    on
        o.city_id = dl.city_id
join
    {{ ref('dim_products')}} as dp
    on
        od.product_id = dp.product_id