"""
PW3 Session 1: load the heart data, look at distributions, check normality.
Source: Heart Disease (Cleveland), Kaggle / UCI.
"""
import io
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 1. Load the data.
# Every line of heart.csv is wrapped in quotation marks, which would make
# pandas read each line as ONE column. Strip the quotes first, then parse.
with open("heart.csv") as f:
    text = f.read().replace('"', "")
df = pd.read_csv(io.StringIO(text))

print("Shape:", df.shape)
print(df.head())

cols = ["age", "chol", "trestbps", "thalach"]
data = df[cols]
print(data.describe())

# 2. Histogram of each variable (4 panels)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, col in zip(axes.ravel(), cols):
    ax.hist(data[col], bins=20)
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel("how often")
plt.tight_layout()
plt.savefig("distributions.png")
plt.close()

# 3a. Q-Q plot of each variable (4 panels)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, col in zip(axes.ravel(), cols):
    stats.probplot(data[col], dist="norm", plot=ax)
    ax.set_title(f"Q-Q plot: {col}")
plt.tight_layout()
plt.savefig("qqplots.png")
plt.close()

# 3b. Shapiro-Wilk test (H0: the data is normal)
print("\nShapiro-Wilk normality test:")
for col in cols:
    W, p = stats.shapiro(data[col])
    verdict = "NOT normal" if p < 0.05 else "approximately normal"
    print(f"{col:10s} W = {W:.4f}, p = {p:.4g} -> {verdict}   (skewness = {data[col].skew():.2f})")
    