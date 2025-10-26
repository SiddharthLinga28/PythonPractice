import pandas as pd
import numpy as np
import time

n = 2_000_000
rng = np.random.default_rng(0)
df = pd.DataFrame({
    "a": rng.integers(0, 1000, size=n),
    "b": rng.random(n),
    "c": rng.choice(["x","y","z"], size=n, p=[0.6,0.3,0.1])
})

t0 = time.perf_counter()
df["ab"] = df["a"] * df["b"]
m = df["ab"].mean()
t1 = time.perf_counter()

df["c"] = df["c"].astype("category")
t2 = time.perf_counter()
g = df.groupby("c", observed=True)["ab"].sum()
t3 = time.perf_counter()

A = df[["a","b"]].to_numpy(dtype=float)
t4 = time.perf_counter()
z = (A - A.mean(0)) / A.std(0, ddof=1)
t5 = time.perf_counter()

print(round(t1-t0,4))
print(round(t3-t2,4))
print(z.shape, round(t5-t4,4))
print(g.to_dict())
print(round(m,6))
