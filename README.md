# 🛒 Mini E-Commerce Modern Data Stack

> **End-to-end ELT data pipeline** using **Azure Blob Storage**, **Snowflake**, **dbt Core**, and **Power BI** — designed to demonstrate a complete modern data stack workflow for e-commerce analytics.

---

## 🚀 Project Overview

This project simulates an **e-commerce analytics pipeline** built using modern data engineering tools and principles.

It covers:
- **Extraction & Ingestion** from Excel (AdventureWorks dataset)
- **Landing Zone Storage** in Azure Blob
- **Loading** into Snowflake using `COPY INTO`
- **Transformations & Modeling** with dbt Core
- **Visualization** in Power BI
- (Next) **Orchestration** with Apache Airflow

The goal is to show how to build a **scalable, modular, and production-ready data pipeline**.

---

## 🧠 Architecture Overview


Excel → (Python) → CSV
         |
         v
   Azure Blob “landing”  (container: landing)
         |
         v
 Snowflake External Stage ──> COPY INTO ──> RAW_LZ tables
                                   |
                                   v
                           dbt STAGING (views, PUBLIC_STG)
                                   |
                                   v
                           dbt MARTS (tables, PUBLIC_MART)
                                   |
                                   v
                              Power BI / SQL


## ⚙️ Tools & Technologies

| Layer | Tool | Purpose |
|-------|------|----------|
| **Data Source** | Excel (AdventureWorks) | Source data for e-commerce domain |
| **Extraction** | Python (pandas) | Convert Excel to CSV |
| **Landing Zone** | Azure Blob Storage | Store raw CSV files |
| **Warehouse** | Snowflake | Centralized storage and compute |
| **ELT Orchestration (Transform)** | dbt Core | Build, test, and document data models |
| **Visualization** | Power BI | Dashboard and KPI visualization |
| **(Next)** | Apache Airflow | Automation and scheduling of pipeline |


---

## 🧱 Data Pipeline Layers

| Layer | Description | Examples |
|-------|--------------|-----------|
| **Landing (Azure)** | Raw CSV files stored in Azure Blob Storage | `customers.csv`, `orders.csv` |
| **Raw (Snowflake)** | Loaded CSVs using `COPY INTO`, minimal transformations | `CUSTOMERS_RAW`, `ORDERS_RAW` |
| **Staging (dbt)** | Cleaned and standardized data (type casting, renaming, normalization) | `STG_CUSTOMERS`, `STG_ORDERS` |
| **Mart (dbt)** | Analytics-ready tables and facts for BI | `DIM_CUSTOMERS`, `FCT_ORDERS`, `FCT_REVENUE_DAILY` |


         ┌───────────┐
         │ Customers  │────┐
         └───────────┘    │
                          ▼
                    ┌────────────┐
                    │ Orders     │
                    └────────────┘
                          │
                          ▼
                    ┌────────────┐
                    │ OrderItems │───┐
                    └────────────┘   │
                                     ▼
                                ┌────────────┐
                                │ Products   │
                                └────────────┘
➡ dbt Models Built

stg_customers.sql

stg_orders.sql

stg_products.sql

stg_order_items.sql

dim_customers.sql

fct_orders.sql

fct_revenue_daily.sql
🧰 Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/<your_username>/mini-ecom-modern-data-stack.git
cd mini-ecom-modern-data-stack

2️⃣ Environment Setup

Python ≥ 3.10

dbt Core (Snowflake adapter)

Install dbt:

pip install dbt-snowflake

3️⃣ Configure dbt Profile

Edit ~/.dbt/profiles.yml (Windows: %USERPROFILE%\.dbt\profiles.yml)

mini_ecom:
  outputs:
    dev:
      type: snowflake
      account: <ACCOUNT_NAME>
      user: <USERNAME>
      password: <PASSWORD>
      role: ANALYST
      database: ANALYTICS_DEV
      warehouse: WH_ANALYTICS_XS
      schema: PUBLIC
  target: dev

4️⃣ Run Models
dbt debug
dbt run
dbt test

5️⃣ Connect to Power BI

Connect Power BI to ANALYTICS_DEV.PUBLIC_MART schema using the Snowflake connector.

📊 Example Analytics
Metric	Description
Total Revenue	Sum of completed order item sales
Daily Revenue Trend	Time-series view from fct_revenue_daily
Customer Segments	Dimensional breakdown from dim_customers
Order Count by Status	Derived from normalized order statuses
🧠 Key Learnings

ELT pattern: Extract & Load first, then Transform in-warehouse.

dbt modularity: ref() and source() manage model dependencies.

Data governance: Separate layers (RAW → STG → MART) for clarity and auditability.

Testing: Data quality enforced via dbt tests (unique, not_null).

Reproducibility: The entire pipeline can be re-run from raw CSVs.

Scalability: Architecture ready for Airflow orchestration.

🔄 Next Steps

 Add Apache Airflow DAG for full automation

 Deploy dbt to dbt Cloud / GitHub Actions CI/CD

 Add Snapshots for slowly changing dimensions

 Extend Power BI dashboards (Revenue, Customer Segments)

📦 Repository Structure
mini-ecom-modern-data-stack/
│
├── dbt/
│   └── mini_ecom/
│       ├── models/
│       │   ├── staging/
│       │   ├── marts/
│       │   └── snapshots/
│       ├── macros/
│       └── dbt_project.yml
│
├── python_scripts/
│   ├── extract_excel_to_csv.py
│
├── airflow_dag/               # (coming soon)
│   └── mini_ecom_dag.py
│
└── README.md

🧩 Future Enhancements

Add incremental models in dbt for large data volumes

Implement data quality alerts in Airflow

Add dbt documentation site using dbt docs generate

Integrate with GitHub Actions CI/CD
