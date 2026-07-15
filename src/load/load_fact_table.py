import pandas as pd
from pathlib import Path
from sqlalchemy import text
from src.config.db_config import engine


def load_fact_table():

    print("=" * 60)
    print("LOADING FACT TABLE")
    print("=" * 60)

    project_root = Path(__file__).resolve().parents[2]

    csv_path = project_root / "data" / "processed" / "clean_orders.csv"

    df = pd.read_csv(csv_path)

    with engine.connect() as conn:

        # Customer Dimension
        customer = pd.read_sql(
            "SELECT customer_key, customer_id FROM dim_customer",
            conn
        )

        # Product Dimension
        product = pd.read_sql(
            "SELECT product_key, product_id FROM dim_product",
            conn
        )

        # Store Dimension
        store = pd.read_sql(
            "SELECT store_key, city, state, country, region, market FROM dim_store",
            conn
        )

        # Date Dimension
        date = pd.read_sql(
            "SELECT date_key, order_date, ship_date FROM dim_date",
            conn
        )

    print("Dimension tables loaded successfully.")

    # -----------------------------
    # Customer Mapping
    # -----------------------------
    fact = df.merge(
        customer,
        left_on="Customer_ID",
        right_on="customer_id",
        how="left"
    )

    # -----------------------------
    # Product Mapping
    # -----------------------------
    fact = fact.merge(
        product,
        left_on="Product_ID",
        right_on="product_id",
        how="left"
    )

    # -----------------------------
    # Convert Dates
    # -----------------------------
    fact["Order_Date"] = pd.to_datetime(fact["Order_Date"])
    fact["Ship_Date"] = pd.to_datetime(fact["Ship_Date"])

    date["order_date"] = pd.to_datetime(date["order_date"])
    date["ship_date"] = pd.to_datetime(date["ship_date"])

    # -----------------------------
    # Date Mapping
    # -----------------------------
    fact = fact.merge(
        date,
        left_on=["Order_Date", "Ship_Date"],
        right_on=["order_date", "ship_date"],
        how="left"
    )

    # -----------------------------
    # Store Mapping
    # -----------------------------
    fact = fact.merge(
        store,
        left_on=[
            "City",
            "State",
            "Country",
            "Region",
            "Market"
        ],
        right_on=[
            "city",
            "state",
            "country",
            "region",
            "market"
        ],
        how="left"
    )

    # -----------------------------
    # Final Fact Table
    # -----------------------------
    fact_sales = fact[
        [
            "Order_ID",
            "customer_key",
            "product_key",
            "store_key",
            "date_key",
            "Sales",
            "Profit",
            "Quantity",
            "Discount",
            "Shipping_Cost"
        ]
    ]

    fact_sales.columns = [
        "order_id",
        "customer_key",
        "product_key",
        "store_key",
        "date_key",
        "sales",
        "profit",
        "quantity",
        "discount",
        "shipping_cost"
    ]

    fact_sales.to_sql(
        "fact_sales",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Fact Records Loaded : {len(fact_sales)}")

    print("=" * 60)
    print("FACT TABLE LOADED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    load_fact_table()