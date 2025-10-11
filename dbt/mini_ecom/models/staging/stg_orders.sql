{{ config(schema='PUBLIC_STG', materialized='view') }}

-- Normalize many possible status values to a single 'completed'
-- AdventureWorks codes: 1=In process, 2=Approved, 3=Backordered, 4=Rejected, 5=Shipped, 6=Canceled
select
  id as order_id,
  customer_id,
  order_ts,
  case
    -- numeric codes often seen in AW exports
    when status in ('5') then 'completed'   -- Shipped
    -- common text variants
    when lower(status) in (
      'completed','complete','closed','shipped','delivered','fulfilled','success'
    ) then 'completed'
    -- everything else
    when status is null or trim(status) = '' then 'unknown'
    else lower(status)
  end as status
from {{ source('raw_lz','orders_raw') }}
