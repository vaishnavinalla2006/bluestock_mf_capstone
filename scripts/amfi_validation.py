import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")

fund_master = pd.read_csv(
    RAW_PATH / "01_fund_master.csv"
)

nav_history = pd.read_csv(
    RAW_PATH / "02_nav_history.csv"
)

master_codes = set(
    fund_master["amfi_code"]
)

nav_codes = set(
    nav_history["amfi_code"]
)

missing_codes = (
    master_codes - nav_codes
)

print("\n==============================")
print("AMFI CODE VALIDATION")
print("==============================")

print(
    f"\nCodes in fund master: "
    f"{len(master_codes)}"
)

print(
    f"Codes in nav history: "
    f"{len(nav_codes)}"
)

print(
    f"Missing codes: "
    f"{len(missing_codes)}"
)

if len(missing_codes) > 0:

    print("\nMissing Codes:")
    print(missing_codes)

else:

    print(
        "\nAll AMFI codes validated "
        "successfully."
    )

