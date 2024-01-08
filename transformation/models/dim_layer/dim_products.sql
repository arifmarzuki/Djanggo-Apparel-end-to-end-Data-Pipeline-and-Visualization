select  
    p.*,
    pc.product_category_name 
from
    products p
left join  product_categories pc on pc.product_category_id=p.product_category_id