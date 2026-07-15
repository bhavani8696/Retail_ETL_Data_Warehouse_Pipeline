import pandas as pd
from pathlib import Path


def extract_data():
    # Project root
    project_root = Path(__file__).resolve().parents[2]

    # CSV Path
    csv_path = project_root / "data" / "raw" / "orders.csv"

    print("=" * 60)
    print("RETAIL ETL - EXTRACT STAGE")
    print("=" * 60)

    # Read CSV
    df = pd.read_csv(csv_path)

    print(f"\nDataset Loaded Successfully")

    print(f"\nRows       : {df.shape[0]}")
    print(f"Columns    : {df.shape[1]}")

    print("\nColumn Names:")
    for col in df.columns:
        print(f" - {col}")

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nFirst 5 Rows:")
    print(df.head())

    return df


if __name__ == "__main__":
    extract_data()