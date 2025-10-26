import pandas as pd
import numpy as np

df = pd.DataFrame({
    "date": pd.date_range("2025-10-01", periods=8, freq="D"),
    "store": ["A","A","B","B","A","B","A","B"],
    "units": [5,7,3,4,8,6,2,9],
    "price": [10,10,11,11,10,12,10,12]
})
df["revenue"] = df["units"] * df["price"]
daily = df.groupby("date", as_index=False).agg(total_units=("units","sum"), total_revenue=("revenue","sum"))
by_store = df.pivot_table(index="store", values=["units","revenue"], aggfunc="sum")
top_day = daily.sort_values("total_revenue", ascending=False).head(1)
print(df.head(3))
print(daily.tail(3))
print(by_store)
print(top_day)
