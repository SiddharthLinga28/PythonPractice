import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

path = Path("dementia_dataset (2).xls")
if path.suffix.lower()==".csv":
    df = pd.read_csv(path)
elif path.suffix.lower()==".xlsx":
    df = pd.read_excel(path, engine="openpyxl")
elif path.suffix.lower()==".xls":
    df = pd.read_excel(path, engine="xlrd")
else:
    raise ValueError("Unsupported file type")

label_map = {"Nondemented":0,"NonDemented":0,"NONDEMENTED":0,"Demented":1,"Converted":1}
df = df.copy()
df["target"] = df["Group"].map(label_map)
df = df.dropna(subset=["target"])
y = df["target"].astype(int)

num_cols = df.select_dtypes(include=["number"]).columns.tolist()
cat_cols = [c for c in ["M/F","Hand"] if c in df.columns]
num_cols = [c for c in num_cols if c!="target"]

X = df[num_cols + cat_cols]

num_pipe = Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())])
cat_pipe = Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))])
pre = ColumnTransformer([("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)])

clf = Pipeline([("pre", pre), ("lr", LogisticRegression(max_iter=2000, class_weight="balanced"))])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
print(round(accuracy_score(y_test, pred),3))
print(classification_report(y_test, pred, digits=3))
