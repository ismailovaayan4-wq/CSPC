"""
PW3 Session 2: group comparison, correlation, and the confounder mystery.
"""
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ---------- load heart data (strip the quotes around each line) ----------
with open("heart.csv") as f:
    text = f.read().replace('"', "")
heart = pd.read_csv(io.StringIO(text))

# ================= 4. Is the effect real? =================
disease = heart.loc[heart["target"] == 1, "thalach"]
healthy = heart.loc[heart["target"] == 0, "thalach"]

print("=== Task 4: thalach, disease vs healthy ===")
print(f"disease: n = {len(disease)}, mean = {disease.mean():.2f}")
print(f"healthy: n = {len(healthy)}, mean = {healthy.mean():.2f}")

# thalach is not normal (Session 1) -> Mann-Whitney U, two-tailed
U, p_mw = stats.mannwhitneyu(disease, healthy, alternative="two-sided")
print(f"Mann-Whitney U = {U:.1f}, p = {p_mw:.3g}")

# cross-check with the t-test
t_stat, p_t = stats.ttest_ind(disease, healthy)
print(f"t-test (cross-check): t = {t_stat:.2f}, p = {p_t:.3g}")

# mean and standard error of the mean for each group
def mean_se(x):
    return x.mean(), x.std(ddof=1) / np.sqrt(len(x))

m_d, se_d = mean_se(disease)
m_h, se_h = mean_se(healthy)
print(f"disease: {m_d:.2f} +/- {se_d:.2f} (SE), 95% CI ~ [{m_d-2*se_d:.2f}, {m_d+2*se_d:.2f}]")
print(f"healthy: {m_h:.2f} +/- {se_h:.2f} (SE), 95% CI ~ [{m_h-2*se_h:.2f}, {m_h+2*se_h:.2f}]")

plt.figure(figsize=(5, 4))
plt.errorbar(["healthy", "disease"], [m_h, m_d], yerr=[2 * se_h, 2 * se_d],
             fmt="o", capsize=8, markersize=8)
plt.ylabel("mean thalach (max heart rate)")
plt.title("Group means with 95% CI (mean +/- 2 SE)")
plt.tight_layout()
plt.savefig("thalach_groups.png")
plt.close()

# ================= 5. Do two things move together? =================
print("\n=== Task 5: age vs thalach ===")
r, p_r = stats.pearsonr(heart["age"], heart["thalach"])
rho, p_rho = stats.spearmanr(heart["age"], heart["thalach"])
print(f"Pearson  r   = {r:.3f}, p = {p_r:.3g}")
print(f"Spearman rho = {rho:.3f}, p = {p_rho:.3g}")

plt.figure(figsize=(6, 4))
plt.scatter(heart["age"], heart["thalach"], s=15)
plt.xlabel("age")
plt.ylabel("thalach")
plt.title(f"age vs thalach (r = {r:.2f})")
plt.tight_layout()
plt.savefig("age_thalach.png")
plt.close()

# ================= 6. Chemical mystery: naive analysis =================
chem = pd.read_csv("chemicals_cancer.csv")
print("\n=== Task 6: naive analysis ===")
print("rows:", len(chem))
for col in ["benzene", "cadmium"]:
    r_c, p_c = stats.pearsonr(chem[col], chem["malignancy"])
    print(f"{col:8s} vs malignancy: r = {r_c:.3f}, p = {p_c:.3g}")

# ================= 7. Look again: control the confounder =================
print("\n=== Task 7: who drives the pollution index? ===")
for col in ["benzene", "cadmium", "malignancy"]:
    r_p, _ = stats.pearsonr(chem[col], chem["pollution_index"])
    print(f"{col:10s} vs pollution_index: r = {r_p:.3f}")

print("\nAssociation with malignancy inside narrow pollution_index bands:")
bands = [(0, 30), (30, 50), (50, 70), (70, 1000)]
for lo, hi in bands:
    sub = chem[(chem["pollution_index"] > lo) & (chem["pollution_index"] <= hi)]
    if len(sub) < 10:
        continue
    rb, _ = stats.pearsonr(sub["benzene"], sub["malignancy"])
    rc, _ = stats.pearsonr(sub["cadmium"], sub["malignancy"])
    print(f"pollution in ({lo}, {hi}]: n = {len(sub):4d} | benzene r = {rb:6.3f} | cadmium r = {rc:6.3f}")

# the single band the lab suggests
sub = chem[(chem["pollution_index"] > 40) & (chem["pollution_index"] < 60)]
rb, _ = stats.pearsonr(sub["benzene"], sub["malignancy"])
rc, _ = stats.pearsonr(sub["cadmium"], sub["malignancy"])
print(f"\nBand 40-60: n = {len(sub)} | benzene r = {rb:.3f} | cadmium r = {rc:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, col in zip(axes, ["benzene", "cadmium"]):
    ax.scatter(chem[col], chem["malignancy"], s=6, alpha=0.4, label="all patients")
    ax.scatter(sub[col], sub["malignancy"], s=8, color="red", label="pollution 40-60")
    ax.set_xlabel(col)
    ax.set_ylabel("malignancy")
    ax.legend()
plt.tight_layout()
plt.savefig("chemicals.png")
plt.close()

# ================= Bonus: entropy of a categorical column =================
print("\n=== Bonus: entropy of target ===")
p = heart["target"].value_counts(normalize=True)
print(p)
H = -(p * np.log2(p)).sum()
print(f"Entropy of target = {H:.3f} bits (maximum for 2 categories = 1 bit)")