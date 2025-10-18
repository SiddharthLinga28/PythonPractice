import numpy as np

rng = np.random.default_rng(0)
x = rng.normal(50, 10, size=12)
y = rng.normal(52, 11, size=12)

xz = (x - x.mean()) / x.std(ddof=1)
yz = (y - y.mean()) / y.std(ddof=1)
corr = (xz * yz).mean()

d = np.linalg.norm(x - y)

mask = x > np.median(x)
high_x_mean = x[mask].mean()

print(round(corr,3))
print(round(d,3))
print(round(high_x_mean,3))
