{{ config(schema='MART', materialized='table') }}

with base as (
  select * from {{ ref('stg_customers') }}
)
select
  customer_id,
  signup_date,
  country,
  segment
from base
