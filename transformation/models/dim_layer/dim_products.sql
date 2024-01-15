select
    p.product_id
    , p.product_name
    , p.size
    , p.price
    , pc.product_category_id
    , pc.product_category_name
from 
    products p
left join
    product_categories as pc
    on
        pc.product_category_id = p.product_category_id