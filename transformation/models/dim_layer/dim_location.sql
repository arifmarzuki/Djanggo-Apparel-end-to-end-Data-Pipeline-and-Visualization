select
    c.*,
    p.province_names
from
    cities c
left join provinces p on c.province_id=p.province_id