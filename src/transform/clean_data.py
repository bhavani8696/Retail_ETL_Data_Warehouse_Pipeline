import pandas as pd
from pathlib import Path

def clean_data():

    project_root = Path(__file__).resolve().parents[2]

    input_file = project_root / "data" / "raw" / "orders.csv"
    output_file = project_root / "data" / "processed" / "clean_orders.csv"

    print("=" * 60)
    print("RETAIL ETL - DATA CLEANING")
    print("=" * 60)

    df = pd.read_csv(input_file)

    print(f"\nOriginal Rows : {len(df)}")

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove unwanted column
    if "记录数" in df.columns:
        df.drop(columns=["记录数"], inplace=True)

    # Convert dates
    df["Order.Date"] = pd.to_datetime(df["Order.Date"])
    df["Ship.Date"] = pd.to_datetime(df["Ship.Date"])

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )

    # Save cleaned data
    df.to_csv(output_file, index=False)

    print(f"Rows After Cleaning : {len(df)}")
    print(f"Columns After Cleaning : {len(df.columns)}")

    print("\nCleaned dataset saved successfully.")
    print(output_file)


if __name__ == "__main__":
    clean_data()