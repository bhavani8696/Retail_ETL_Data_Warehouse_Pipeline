import pandas as pd
from pathlib import Path
from sqlalchemy import text
from src.config.db_config import engine


def load_dimension_tables():

    print("=" * 60)
    print("LOADING DIMENSION TABLES")
    print("=" * 60)

    project_root = Path(__file__).resolve().parents[2]

    csv_path = project_root / "data" / "processed" / "clean_orders.csv"

    df = pd.read_csv(csv_path)

    # -------------------------
    # CUSTOMER DIMENSION
    # -------------------------

    customer_df = (
        df[["Customer_ID", "Customer_Name", "Segment"]]
        .drop_duplicates(subset=["Customer_ID"])
        .rename(columns={
            "Customer_ID": "customer_id",
            "Customer_Name": "customer_name",
            "Segment": "segment"
        })
    )

    customer_df.to_sql(
        "dim_customer",
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Customers Loaded : {len(customer_df)}")

    # -------------------------
    # PRODUCT DIMENSION
    # -------------------------

    product_df = (
        df[["Product_ID", "Product_Name", "Category", "Sub_Category"]]
        .drop_duplicates(subset=["Product_ID"])
        .rename(columns={
            "Product_ID": "product_id",
            "Product_Name": "product_name",
            "Category": "category",
            "Sub_Category": "sub_category"
        })
    )

    product_df.to_sql(
        "dim_product",
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Products Loaded : {len(product_df)}")

    # -------------------------
    # STORE DIMENSION
    # -------------------------

    store_df = (
        df[["City", "State", "Country", "Region", "Market"]]
        .drop_duplicates()
        .rename(columns={
            "City": "city",
            "State": "state",
            "Country": "country",
            "Region": "region",
            "Market": "market"
        })
    )

    store_df.to_sql(
        "dim_store",
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Stores Loaded : {len(store_df)}")

    # -------------------------
    # DATE DIMENSION
    # -------------------------

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])

    date_df = (
        df[["Order_Date", "Ship_Date", "Year", "weeknum"]]
        .drop_duplicates()
        .rename(columns={
            "Order_Date": "order_date",
            "Ship_Date": "ship_date",
            "Year": "year",
            "weeknum": "week_num"
        })
    )

    date_df.to_sql(
        "dim_date",
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Dates Loaded : {len(date_df)}")

    print("\n")
    print("=" * 60)
    print("ALL DIMENSION TABLES LOADED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    load_dimension_tables()