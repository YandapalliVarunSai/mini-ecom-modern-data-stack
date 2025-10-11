{{ config(schema='MART', materialized='table') }}

with o as (
  select * from {{ ref('stg_orders') }} where status = 'completed'
),
i as (
  select * from {{ ref('stg_order_items') }}
)
select
  o.order_id,
  o.customer_id,
  o.order_ts::date as order_date,
  sum(i.qty * i.unit_price_at_sale) as order_value,
  count(*) as line_items
from o
join i using(order_id)
group by 1,2,3
