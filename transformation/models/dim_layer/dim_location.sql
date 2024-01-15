select
    c.city_id
    , c.city_names
    , p.province_id
    , p.province_names
from
    provinces p
left join
    cities as c
    on
        c.province_id = p.province_id