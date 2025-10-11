{{ config(schema='STG', materialized='view') }}

select
  order_id,
  product_id,
  try_to_number(qty) as qty,
  try_to_decimal(unit_price_at_sale, 10, 2) as unit_price_at_sale
from {{ source('raw_lz','order_items_raw') }}
