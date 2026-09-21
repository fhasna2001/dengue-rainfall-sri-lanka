import pandas as pd

df = pd.read_csv("data/processed/dengue_weekly_by_district_raw.csv")
colombo = df[df["district"] == "Colombo"]
colombo = colombo.drop_duplicates(subset=["year", "week"]).sort_values(["year", "week"])
print(colombo[["year", "week", "cases"]].to_string(index=False))