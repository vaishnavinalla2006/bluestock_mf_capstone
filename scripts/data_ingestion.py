import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")

csv_files = list(RAW_PATH.glob("*.csv"))

print("\n====================================")
print(f"FOUND {len(csv_files)} CSV FILES")
print("====================================\n")

for file in csv_files:

    print("=" * 70)
    print(f"DATASET: {file.name}")
    print("=" * 70)

    try:

        df = pd.read_csv(file)

        print("\nSHAPE:")
        print(df.shape)

        print("\nCOLUMN NAMES:")
        print(df.columns.tolist())

        print("\nDATA TYPES:")
        print(df.dtypes)

        print("\nFIRST 5 ROWS:")
        print(df.head())

        print("\nMISSING VALUES:")
        print(df.isnull().sum())

        print("\nDUPLICATES:")
        print(df.duplicated().sum())

        # Special exploration for fund master

        if file.name == "01_fund_master.csv":

            print("\nUNIQUE FUND HOUSES:")
            print(df["fund_house"].unique())

            print("\nUNIQUE CATEGORIES:")
            print(df["category"].unique())

            print("\nUNIQUE SUB-CATEGORIES:")
            print(df["sub_category"].unique())

            print("\nUNIQUE RISK CATEGORIES:")
            print(df["risk_category"].unique())

        print("\n")

    except Exception as e:

        print(f"ERROR LOADING {file.name}")
        print(e)
