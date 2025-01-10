-- Use the `ref` function to select from other models

select *
from "dbt_demo"."public"."my_first_dbt_model"
where id = 1