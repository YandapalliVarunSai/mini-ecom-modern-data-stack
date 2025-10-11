{{ config(schema='STG', materialized='view') }}

select
  id as customer_id,
  try_to_date(signup_date) as signup_date,
  country,
  lower(segment) as segment
from {{ source('raw_lz','customers_raw') }}
