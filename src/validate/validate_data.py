import pandas as pd
from pathlib import Path


def validate_data():

    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "raw" / "orders.csv"

    df = pd.read_csv(csv_path)

    print("=" * 60)
    print("RETAIL ETL - DATA VALIDATION")
    print("=" * 60)

    print(f"\nTotal Rows : {len(df)}")
    print(f"Total Columns : {len(df.columns)}")

    # Missing Values
    print("\nMissing Values")
    print("-" * 40)
    print(df.isnull().sum())

    # Duplicate Rows
    duplicates = df.duplicated().sum()
    print("\nDuplicate Records :", duplicates)

    # Negative Sales
    negative_sales = (df["Sales"] < 0).sum()
    print("Negative Sales :", negative_sales)

    # Negative Profit
    negative_profit = (df["Profit"] < 0).sum()
    print("Negative Profit :", negative_profit)

    # Invalid Discount
    invalid_discount = ((df["Discount"] < 0) | (df["Discount"] > 1)).sum()
    print("Invalid Discount :", invalid_discount)

    # Invalid Quantity
    invalid_quantity = (df["Quantity"] <= 0).sum()
    print("Invalid Quantity :", invalid_quantity)

    # Invalid Dates
    df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")
    invalid_dates = df["Order.Date"].isnull().sum()

    print("Invalid Dates :", invalid_dates)

    # Data Quality Score
    total_checks = (
        duplicates
        + negative_sales
        + invalid_discount
        + invalid_quantity
        + invalid_dates
    )

    score = ((len(df) - total_checks) / len(df)) * 100

    print("\n" + "=" * 60)
    print(f"DATA QUALITY SCORE : {score:.2f}%")
    print("=" * 60)


if __name__ == "__main__":
    validate_data()