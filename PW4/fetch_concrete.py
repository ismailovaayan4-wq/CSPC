"""
A1: download the UCI Concrete Compressive Strength dataset (Yeh, 1998) once
and save it to data/concrete.csv, so the rest of the lab works offline.
"""
import os
from ucimlrepo import fetch_ucirepo

concrete = fetch_ucirepo(id=165)          # 165 = UCI id of this dataset
X = concrete.data.features                # inputs (DataFrame)
y = concrete.data.targets                 # output (DataFrame with ONE column)

print(concrete.metadata)
print(concrete.variables)

# rename by position, in the order shown in concrete.variables
X = X.copy()
X.columns = ["cement", "slag", "ash", "water", "superplastic",
             "coarse_agg", "fine_agg", "age"]
y = y.iloc[:, 0].rename("strength")       # DataFrame -> 1-D Series

os.makedirs("data", exist_ok=True)
X.assign(strength=y).to_csv("data/concrete.csv", index=False)
print("saved data/concrete.csv", X.shape)