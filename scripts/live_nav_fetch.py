
import requests
import pandas as pd
from pathlib import Path

OUTPUT_PATH = Path("data/raw")

schemes = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for scheme_name, scheme_code in schemes.items():

    print(f"\nFetching {scheme_name}")

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        meta = data.get("meta", {})
        nav_data = data.get("data", [])

        df = pd.DataFrame(nav_data)

        output_file = (
            OUTPUT_PATH /
            f"{scheme_name}_live_nav.csv"
        )

        df.to_csv(
            output_file,
            index=False
        )

        print(f"Saved -> {output_file}")

        print(
            f"Scheme Name: "
            f"{meta.get('scheme_name')}"
        )

    else:

        print(
            f"FAILED FOR {scheme_name}"
        )

