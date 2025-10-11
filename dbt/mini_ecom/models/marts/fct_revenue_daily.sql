{{ config(schema='MART', materialized='table') }}

with f as (select * from {{ ref('fct_orders') }})
select
  order_date,
  sum(order_value) as revenue,
  count(distinct order_id) as orders,
  case when count(distinct order_id)=0 then null
       else sum(order_value)/count(distinct order_id) end as aov
from f
group by 1
order by 1
