"""
PW4 Session A: concrete strength (regression + classification).
Data: UCI Concrete Compressive Strength (Yeh, 1998).
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

os.makedirs("results", exist_ok=True)

# ---------- A2. Clean and look ----------
df = pd.read_csv("data/concrete.csv")
print("shape before cleaning:", df.shape)
print("duplicate rows:", df.duplicated().sum())
print("missing values per column:\n", df.isna().sum())

df = df.drop_duplicates().reset_index(drop=True)
print("shape after cleaning:", df.shape)

X = df.drop(columns="strength")
y = df["strength"]

print(df.describe().T)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(df["cement"], df["strength"], s=8)
axes[0].set_xlabel("cement (kg/m3)")
axes[0].set_ylabel("strength (MPa)")
axes[1].scatter(df["age"], df["strength"], s=8)
axes[1].set_xlabel("age (days)")
axes[1].set_ylabel("strength (MPa)")
plt.tight_layout()
plt.savefig("results/A_scatter.png")
plt.close()

# ---------- A3. Split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("train:", X_train.shape, " test:", X_test.shape)

# ---------- A4. Linear regression ----------
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def adj_r2(r2, n, p):
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)

lin = LinearRegression()
lin.fit(X_train, y_train)

print("\nLinear regression: intercept =", round(lin.intercept_, 4))
for name, c in zip(X.columns, lin.coef_):
    print(f"  {name:13s} {c:+.5f}")

pred_train = lin.predict(X_train)
pred_test = lin.predict(X_test)
n, p = X_train.shape

lin_table = pd.DataFrame([{
    "model": "linear",
    "train_RMSE": np.sqrt(mean_squared_error(y_train, pred_train)),
    "test_RMSE": np.sqrt(mean_squared_error(y_test, pred_test)),
    "test_MAE": mean_absolute_error(y_test, pred_test),
    "train_R2": r2_score(y_train, pred_train),
    "train_adjR2": adj_r2(r2_score(y_train, pred_train), n, p),
    "test_R2": r2_score(y_test, pred_test),
}])
print(lin_table.round(3).to_string(index=False))

# residuals of the test set against age (log x-axis)
resid = y_test - pred_test
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(X_test["age"], resid, s=10)
ax.axhline(0, color="red")
ax.set_xscale("log")
ax.set_xlabel("age (days, log scale)")
ax.set_ylabel("residual = true - predicted (MPa)")
plt.tight_layout()
plt.savefig("results/A_residuals_linear.png")
plt.close()

# ---------- A5. Polynomial regression ----------
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline

rows = []
for d in [1, 2, 3, 4]:
    poly = make_pipeline(PolynomialFeatures(degree=d, include_bias=False),
                         StandardScaler(),
                         LinearRegression())
    poly.fit(X_train, y_train)
    p_d = poly[0].n_output_features_
    ptr = poly.predict(X_train)
    pte = poly.predict(X_test)
    r2_tr = r2_score(y_train, ptr)
    rows.append({
        "degree": d,
        "p": p_d,
        "train_RMSE": np.sqrt(mean_squared_error(y_train, ptr)),
        "test_RMSE": np.sqrt(mean_squared_error(y_test, pte)),
        "train_R2": r2_tr,
        "train_adjR2": adj_r2(r2_tr, len(X_train), p_d),
        "test_R2": r2_score(y_test, pte),
    })

poly_table = pd.DataFrame(rows)
print("\nPolynomial regression:")
print(poly_table.round(3).to_string(index=False))
poly_table.to_csv("results/A_poly.csv", index=False)

# ---------- A6. Classification: KNN and decision tree ----------
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text

K_CHOSEN = 7        # placeholder: change after looking at the K sweep
DEPTH_CHOSEN = 5   # placeholder: change after looking at the depth sweep

y_class = (df["strength"] >= 40).astype(int)   # 1 = reaches 40 MPa
print("\nclass proportions:\n", y_class.value_counts(normalize=True).round(3))

Xc_train, Xc_test, c_train, c_test = train_test_split(
    X, y_class, test_size=0.2, random_state=42, stratify=y_class)

# --- KNN: sweep K (with scaler) ---
rows = []
for K in [1, 3, 5, 7, 15, 25, 51, 101]:
    knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K))
    knn.fit(Xc_train, c_train)
    rows.append({"K": K,
                 "train_acc": knn.score(Xc_train, c_train),
                 "test_acc": knn.score(Xc_test, c_test)})
knn_table = pd.DataFrame(rows)
print("\nKNN sweep:\n", knn_table.round(3).to_string(index=False))
knn_table.to_csv("results/A_knn_sweep.csv", index=False)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(knn_table["K"], knn_table["train_acc"], "o-", label="train")
ax.plot(knn_table["K"], knn_table["test_acc"], "o-", label="test")
ax.set_xscale("log")
ax.set_xlabel("K (log scale)")
ax.set_ylabel("accuracy")
ax.legend()
plt.tight_layout()
plt.savefig("results/A_knn_sweep.png")
plt.close()

# --- KNN at chosen K: with vs without scaler ---
with_sc = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K_CHOSEN))
no_sc = KNeighborsClassifier(n_neighbors=K_CHOSEN)
with_sc.fit(Xc_train, c_train)
no_sc.fit(Xc_train, c_train)
print(f"\nK = {K_CHOSEN}: test accuracy with scaler = {with_sc.score(Xc_test, c_test):.3f}, "
      f"without scaler = {no_sc.score(Xc_test, c_test):.3f}")

# --- KNN at chosen K: five different splits ---
accs = []
for rs in range(5):
    Xa, Xb, ca, cb = train_test_split(X, y_class, test_size=0.2,
                                      random_state=rs, stratify=y_class)
    m = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K_CHOSEN))
    m.fit(Xa, ca)
    accs.append(m.score(Xb, cb))
print("five test accuracies:", np.round(accs, 3),
      f"| mean = {np.mean(accs):.3f}, std = {np.std(accs):.3f}")

# --- Decision tree: sweep max_depth ---
rows = []
for d in [1, 2, 3, 4, 5, 6, 8, None]:
    tree = DecisionTreeClassifier(criterion="entropy", max_depth=d,
                                  min_samples_leaf=1, random_state=0)
    tree.fit(Xc_train, c_train)
    rows.append({"max_depth": "None" if d is None else d,
                 "leaves": tree.get_n_leaves(),
                 "train_acc": tree.score(Xc_train, c_train),
                 "test_acc": tree.score(Xc_test, c_test)})
tree_table = pd.DataFrame(rows)
print("\nTree sweep:\n", tree_table.round(3).to_string(index=False))
tree_table.to_csv("results/A_tree_sweep.csv", index=False)

fig, ax = plt.subplots(figsize=(6, 4))
xs = range(len(tree_table))
ax.plot(xs, tree_table["train_acc"], "o-", label="train")
ax.plot(xs, tree_table["test_acc"], "o-", label="test")
ax.set_xticks(list(xs))
ax.set_xticklabels(tree_table["max_depth"].astype(str))
ax.set_xlabel("max_depth")
ax.set_ylabel("accuracy")
ax.legend()
plt.tight_layout()
plt.savefig("results/A_tree_sweep.png")
plt.close()

# --- top two levels of the tree at chosen depth ---
tree_final = DecisionTreeClassifier(criterion="entropy", max_depth=DEPTH_CHOSEN,
                                    min_samples_leaf=1, random_state=0)
tree_final.fit(Xc_train, c_train)
print(f"\nTree with max_depth = {DEPTH_CHOSEN}: top two levels")
print(export_text(tree_final, feature_names=list(X.columns), max_depth=2))

# ---------- A7. The metrics that matter ----------
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score, f1_score)

knn_final = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K_CHOSEN))
knn_final.fit(Xc_train, c_train)

def metrics_row(name, model):
    pred = model.predict(Xc_test)
    tn, fp, fn, tp = confusion_matrix(c_test, pred).ravel()
    return {"model": name, "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "accuracy": accuracy_score(c_test, pred),
            "precision": precision_score(c_test, pred),
            "recall": recall_score(c_test, pred),
            "F1": f1_score(c_test, pred)}

metrics = pd.DataFrame([metrics_row(f"KNN (K={K_CHOSEN})", knn_final),
                        metrics_row(f"Tree (depth={DEPTH_CHOSEN})", tree_final)])
print("\nA7 metrics:")
print(metrics.round(3).to_string(index=False))
metrics.to_csv("results/A_metrics.csv", index=False)

# thresholds for the KNN probability of class 1
proba = knn_final.predict_proba(Xc_test)[:, 1]
rows = []
for t in [0.3, 0.5, 0.7, 0.9]:
    pred = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(c_test, pred).ravel()
    rows.append({"threshold": t, "TP": tp, "FP": fp, "FN": fn, "TN": tn,
                 "precision": precision_score(c_test, pred, zero_division=0),
                 "recall": recall_score(c_test, pred)})
thr = pd.DataFrame(rows)
print("\nKNN thresholds:")
print(thr.round(3).to_string(index=False))
thr.to_csv("results/A_thresholds.csv", index=False)

# ---------- A8. Feature importance ----------
from sklearn.inspection import permutation_importance

# (1) raw and standardised coefficients (regression)
raw_coef = pd.Series(lin.coef_, index=X.columns)
std_pipe = make_pipeline(StandardScaler(), LinearRegression())
std_pipe.fit(X_train, y_train)
std_coef = pd.Series(std_pipe[-1].coef_, index=X.columns)

# (2) tree importances (classification tree at chosen depth)
tree_imp = pd.Series(tree_final.feature_importances_, index=X.columns)

# (3) permutation importances (F1 score, KNN and tree)
pi_knn = permutation_importance(knn_final, Xc_test, c_test, scoring="f1",
                                n_repeats=20, random_state=0)
pi_tree = permutation_importance(tree_final, Xc_test, c_test, scoring="f1",
                                 n_repeats=20, random_state=0)

imp = pd.DataFrame({
    "raw_coef": raw_coef,
    "std_coef": std_coef,
    "tree_importance": tree_imp,
    "perm_knn": pd.Series(pi_knn.importances_mean, index=X.columns),
    "perm_tree": pd.Series(pi_tree.importances_mean, index=X.columns),
})
print("\nA8 importance table:")
print(imp.round(4).to_string())
print("\nrank by |raw coef|:", list(raw_coef.abs().sort_values(ascending=False).index))
print("rank by |std coef|:", list(std_coef.abs().sort_values(ascending=False).index))
imp.to_csv("results/A_importance.csv")

# bar chart for three of the measures
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
std_coef.abs().sort_values().plot.barh(ax=axes[0], title="|standardised coef| (MPa per std)")
tree_imp.sort_values().plot.barh(ax=axes[1], title="tree feature importance")
imp["perm_knn"].sort_values().plot.barh(ax=axes[2], title="permutation importance (KNN, F1)")
plt.tight_layout()
plt.savefig("results/A_importance.png")
plt.close()

# ---------- Bonus: let physics choose the features ----------
def physics_features(Xs, use_wb):
    Z = Xs.copy()
    Z["age"] = np.log(Z["age"])                       # strength grows ~ log(age)
    if use_wb:                                        # Abrams' law: water/binder
        Z["water"] = Z["water"] / (Z["cement"] + Z["slag"] + Z["ash"])
        Z = Z.rename(columns={"water": "w_b"})
    return Z

bonus_rows = []
for label, use_wb in [("log(age)", False), ("log(age) + w/b", True)]:
    Ztr, Zte = physics_features(X_train, use_wb), physics_features(X_test, use_wb)
    m = LinearRegression().fit(Ztr, y_train)
    bonus_rows.append({"features": label, "p": Ztr.shape[1],
                       "test_RMSE": np.sqrt(mean_squared_error(y_test, m.predict(Zte))),
                       "test_R2": r2_score(y_test, m.predict(Zte))})
bonus = pd.DataFrame(bonus_rows)
print("\nBonus (physics features, plain LinearRegression):")
print(bonus.round(3).to_string(index=False))
bonus.to_csv("results/A_bonus.csv", index=False)