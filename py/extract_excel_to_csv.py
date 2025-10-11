# extract_excel_to_csv.py
import pandas as pd
from pathlib import Path
import re

# ====== CONFIG ======
# Put your actual file paths here (absolute or relative)
EXCEL_CUSTOMERS = r"../data/Adventure Works Customers Data.xlsx"
EXCEL_FULL      = r"../data/Adventure Works Full Data.xlsx"

# Output folder for CSVs
OUT_DIR = Path("../data_csv")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Helpers
def snake(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s.strip())
    s = re.sub(r"_+", "_", s).strip("_")
    return s.lower()

def read_first_matching_sheet(xlsx_path: str, candidates: list[str]) -> pd.DataFrame:
    xls = pd.ExcelFile(xlsx_path)
    sheets = [s.lower() for s in xls.sheet_names]
    # Try exact/contains match
    for cand in candidates:
        for s in xls.sheet_names:
            if cand.lower() == s.lower() or cand.lower() in s.lower():
                df = pd.read_excel(xlsx_path, sheet_name=s)
                df.columns = [snake(c) for c in df.columns]
                return df
    # If nothing matched, print available
    print(f"[WARN] No candidate sheet found in {xlsx_path}. Available: {xls.sheet_names}")
    return pd.DataFrame()

def safe_write_csv(df: pd.DataFrame, name: str):
    if df.empty:
        print(f"[SKIP] {name}.csv (empty dataframe)")
        return
    out = OUT_DIR / f"{name}.csv"
    df.to_csv(out, index=False)
    print(f"[OK] Wrote {out.resolve()}  rows={len(df)}")

def main():
    # --- Likely mappings for AdventureWorks-style files ---
    customers_df = read_first_matching_sheet(EXCEL_CUSTOMERS, ["Customers", "Customer", "Customer_Details"])
    products_df  = read_first_matching_sheet(EXCEL_FULL,      ["Products", "Product", "Product_Details"])
    orders_df    = read_first_matching_sheet(EXCEL_FULL,      ["Sales", "Orders", "FactInternetSales", "Order_Header"])
    items_df     = read_first_matching_sheet(EXCEL_FULL,      ["Order_Details", "Order Items", "Sales_Detail", "Sales_Orders_Detail"])

    # Minimal column normalization for downstream RAW tables (best-effort)
    # Customers expected: id, signup_date, country, segment
    if not customers_df.empty:
        rename_map = {}
        for c in customers_df.columns:
            if c in ("customerid","id","customer_key"): rename_map[c]="id"
            if c in ("countryregion","country_region","country"): rename_map[c]="country"
            if c in ("segment","cust_category","customer_segment"): rename_map[c]="segment"
            if c in ("signup_date","first_order_date","firstpurchase","first_purchase_date"): rename_map[c]="signup_date"
        customers_df = customers_df.rename(columns=rename_map)

    # Products expected: id, category, unit_price, is_active
    if not products_df.empty:
        rename_map = {}
        for c in products_df.columns:
            if c in ("productid","id","product_key"): rename_map[c]="id"
            if c in ("category","subcategory","product_category"): rename_map[c]="category"
            if c in ("listprice","unitprice","price"): rename_map[c]="unit_price"
            if c in ("status","active","is_active","isactive"): rename_map[c]="is_active"
        products_df = products_df.rename(columns=rename_map)

    # Orders expected: id, customer_id, order_ts, status
    if not orders_df.empty:
        rename_map = {}
        for c in orders_df.columns:
            if c in ("salesorderid","orderid","id"): rename_map[c]="id"
            if c in ("customerid","fk_customer","customer_key"): rename_map[c]="customer_id"
            if c in ("orderdate","order_date","orderdatetime","order_ts","date"): rename_map[c]="order_ts"
            if c in ("status","orderstatus","state"): rename_map[c]="status"
        orders_df = orders_df.rename(columns=rename_map)

    # Items expected: order_id, product_id, qty, unit_price_at_sale
    if not items_df.empty:
        rename_map = {}
        for c in items_df.columns:
            if c in ("salesorderid","orderid"): rename_map[c]="order_id"
            if c in ("productid","product_key","id"): rename_map[c]="product_id"
            if c in ("orderqty","quantity","qty"): rename_map[c]="qty"
            if c in ("unitprice","line_total","price"): rename_map[c]="unit_price_at_sale"
        items_df = items_df.rename(columns=rename_map)

    # Write CSVs
    safe_write_csv(customers_df, "customers")
    safe_write_csv(products_df,  "products")
    safe_write_csv(orders_df,    "orders")
    safe_write_csv(items_df,     "order_items")

if __name__ == "__main__":
    main()
