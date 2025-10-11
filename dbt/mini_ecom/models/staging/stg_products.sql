{{ config(schema='STG', materialized='view') }}

select
  id as product_id,
  category,
  try_to_decimal(unit_price, 10, 2) as unit_price,
  try_to_boolean(is_active) as is_active
from {{ source('raw_lz','products_raw') }}

