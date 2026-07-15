from src.extract.extract_data import extract_data
from src.validate.validate_data import validate_data
from src.transform.clean_data import clean_data
from src.load.load_dimension_tables import load_dimension_tables
from src.load.load_fact_table import load_fact_table
import time


def main():

    start = time.time()

    print("=" * 70)
    print(" RETAIL ETL DATA WAREHOUSE PIPELINE ")
    print("=" * 70)

    print("\n[1/5] Extract Stage")
    extract_data()

    print("\n[2/5] Validation Stage")
    validate_data()

    print("\n[3/5] Cleaning Stage")
    clean_data()

    print("\n[4/5] Loading Dimension Tables")
    load_dimension_tables()

    print("\n[5/5] Loading Fact Table")
    load_fact_table()

    end = time.time()

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print(f"Execution Time : {round(end-start,2)} Seconds")
    print("=" * 70)


if __name__ == "__main__":
    main()