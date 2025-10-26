import pandas as pd
import numpy as np
from pathlib import Path

path = Path("dementia_dataset (2).xls")
if path.suffix.lower()==".csv":
    df = pd.read_csv(path)
elif path.suffix.lower()==".xlsx":
    df = pd.read_excel(path, engine="openpyxl")
elif path.suffix.lower()==".xls":
    df = pd.read_excel(path, engine="xlrd")
else:
    raise ValueError("Unsupported file type")

df.columns = [c.strip() for c in df.columns]
num = df.select_dtypes(include=["number"])
missing = df.isna().sum().sort_values(ascending=False)
grp = df["Group"].value_counts(dropna=False) if "Group" in df.columns else pd.Series(dtype=int)
desc = num.describe().T
valid = num.dropna()
corr = valid.corr(method="pearson") if not valid.empty else pd.DataFrame()
print(df.shape)
print(grp)
print(missing.head(10))
print(desc[["mean","std","min","50%","max"]].round(3).head(10))
print(corr.round(3).head(10))
