import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

path = Path("dementia_dataset (2).xls")
if path.suffix.lower()==".csv":
    raw = pd.read_csv(path)
elif path.suffix.lower()==".xlsx":
    raw = pd.read_excel(path, engine="openpyxl")
elif path.suffix.lower()==".xls":
    raw = pd.read_excel(path, engine="xlrd")
else:
    raise ValueError("Unsupported file type")

df = raw.copy()
df.columns = [c.strip() for c in df.columns]

label_map = {"Nondemented":0,"NonDemented":0,"NONDEMENTED":0,"Demented":1,"Converted":1}
df["target"] = df["Group"].map(label_map)
num = df.select_dtypes(include=["number"]).copy()
if "target" in num.columns:
    num = num.drop(columns=["target"])

summary = num.describe().T
missing = df.isna().sum().sort_values(ascending=False)
group_counts = df["Group"].value_counts(dropna=False) if "Group" in df.columns else pd.Series(dtype=int)

num_cols = num.columns.tolist()
X = df[num_cols]
y = df["target"]
mask = y.notna()
X = X.loc[mask]
y = y.loc[mask].astype(int)

pipe = Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()), ("clf", LogisticRegression(max_iter=2000, class_weight="balanced"))])
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
pipe.fit(Xtr, ytr)
pred = pipe.predict(Xte)
report = classification_report(yte, pred, digits=3, output_dict=True)
report_df = pd.DataFrame(report).T

outdir = Path("pandas_project_outputs")
outdir.mkdir(exist_ok=True)
summary.to_csv(outdir / "numeric_summary.csv")
missing.to_csv(outdir / "missing_counts.csv")
group_counts.to_csv(outdir / "group_counts.csv")
report_df.to_csv(outdir / "model_report.csv")
cleaned = X.copy()
cleaned["target"] = y
cleaned.to_csv(outdir / "cleaned_dataset.csv", index=False)

print(outdir.resolve())
print(summary.shape, missing.shape, group_counts.shape, report_df.shape)
