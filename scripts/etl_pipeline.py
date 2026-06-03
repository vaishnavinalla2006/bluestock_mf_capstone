
import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import create_engine
import logging

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================================
# PATHS
# ==========================================

RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")
DB_PATH = "sqlite:///data/db/bluestock_mf.db"

PROCESSED_PATH.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# SQLITE ENGINE
# ==========================================

engine = create_engine(DB_PATH)

# ==========================================
# CLEAN FUND MASTER
# ==========================================

def clean_fund_master():

    logging.info("Cleaning fund master")

    df = pd.read_csv(
        RAW_PATH / "01_fund_master.csv"
    )

    df = df.drop_duplicates()

    df["launch_date"] = pd.to_datetime(
        df["launch_date"],
        errors="coerce"
    )

    df.to_csv(
        PROCESSED_PATH /
        "clean_fund_master.csv",
        index=False
    )

    return df

# ==========================================
# CLEAN NAV HISTORY
# ==========================================

def clean_nav_history():

    logging.info("Cleaning nav history")

    df = pd.read_csv(
        RAW_PATH / "02_nav_history.csv"
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(subset=["date"])

    df = df.sort_values(
        by=["amfi_code", "date"]
    )

    df = df.drop_duplicates()

    df = df[df["nav"] > 0]

    cleaned_frames = []

    for code in df["amfi_code"].unique():

        temp = df[
            df["amfi_code"] == code
        ].copy()

        temp = temp.set_index("date")

        full_dates = pd.date_range(
            start=temp.index.min(),
            end=temp.index.max(),
            freq="D"
        )

        temp = temp.reindex(full_dates)

        temp["amfi_code"] = code

        temp["nav"] = temp["nav"].ffill()

        temp = temp.reset_index()

        temp = temp.rename(
            columns={"index": "date"}
        )

        cleaned_frames.append(temp)

    final_df = pd.concat(cleaned_frames)

    final_df.to_csv(
        PROCESSED_PATH /
        "clean_nav_history.csv",
        index=False
    )

    return final_df

# ==========================================
# CLEAN TRANSACTIONS
# ==========================================

def clean_transactions():

    logging.info(
        "Cleaning investor transactions"
    )

    df = pd.read_csv(
        RAW_PATH /
        "08_investor_transactions.csv"
    )

    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["transaction_type"] = (
        df["transaction_type"]
        .replace({
            "LUMPSUM": "LUMPSUM",
            "SIP": "SIP",
            "REDEMPTION": "REDEMPTION"
        })
    )

    df = df[
        df["amount_inr"] > 0
    ]

    df["transaction_date"] = (
        pd.to_datetime(
            df["transaction_date"],
            errors="coerce"
        )
    )

    df = df.dropna(
        subset=["transaction_date"]
    )

    valid_kyc = [
        "Verified",
        "Pending"
    ]

    df = df[
        df["kyc_status"]
        .isin(valid_kyc)
    ]

    df.to_csv(
        PROCESSED_PATH /
        "clean_transactions.csv",
        index=False
    )

    return df

# ==========================================
# CLEAN PERFORMANCE
# ==========================================

def clean_performance():

    logging.info(
        "Cleaning scheme performance"
    )

    df = pd.read_csv(
        RAW_PATH /
        "07_scheme_performance.csv"
    )

    numeric_cols = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct"
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    anomalies = df[
        (df["expense_ratio_pct"] < 0.1)
        |
        (df["expense_ratio_pct"] > 2.5)
    ]

    print("\nExpense Ratio Anomalies:")
    print(anomalies.shape[0])

    df = df[
        (df["expense_ratio_pct"] >= 0.1)
        &
        (df["expense_ratio_pct"] <= 2.5)
    ]

    df.to_csv(
        PROCESSED_PATH /
        "clean_performance.csv",
        index=False
    )

    return df

# ==========================================
# LOAD TO SQLITE
# ==========================================

def load_to_sqlite(dataframes):

    logging.info(
        "Loading into SQLite"
    )

    for table_name, df in dataframes.items():

        df.to_sql(
            table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

        logging.info(
            f"{table_name} loaded "
            f"with {len(df)} rows"
        )

# ==========================================
# MAIN PIPELINE
# ==========================================

def main():

    fund_df = clean_fund_master()

    nav_df = clean_nav_history()

    txn_df = clean_transactions()

    perf_df = clean_performance()

    dataframes = {

        "dim_fund": fund_df,

        "fact_nav": nav_df,

        "fact_transactions": txn_df,

        "fact_performance": perf_df
    }

    load_to_sqlite(dataframes)

    logging.info(
        "ETL PIPELINE COMPLETED"
    )

if __name__ == "__main__":
    main()

