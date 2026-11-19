# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc 



---

## PW1 - Lab A: Reproducible Foundations

**What I built:**
- A CSPC repository with Git version control, a conda environment, a radioactive decay
  simulation, and automated tests comparing a pure-Python loop to a vectorised NumPy version.

**Speed comparison (loop vs NumPy):**
- loop : 1.6680 s
- numpy : 0.0002 s
- speed-up: 7344.8x faster

**Tests:** all passing? yes

**Conclusion:**
- The NumPy vectorised version was dramatically faster than the pure-Python loop because it
  processes all atoms in the sample at once instead of looping over each one individually in
  Python. All three tests pass, confirming the simulation starts at N0, correctly rejects a
  negative decay rate, and matches the analytical exponential decay law on average.



---

## PW1 - Lab B: Data, Plotting, and Automation

**What the data showed:**
- The observed counts started at 5000 and decayed rapidly over time, following a clear
  downward curve typical of exponential decay.

**Did it match the analytical law?**
- Yes, the observed data closely follows the analytical curve N0 * exp(-LAMBDA * t); the two
  panels show the same overall shape and scale, with the small deviations expected from real
  (noisy) measurements.

**Snakemake pipeline:**
- The Snakefile defines one rule that rebuilds figure.png from decay_observed.csv by running
  plot_STUDENT.py, and only reruns when the input files are newer than the output.





---

## PW2 - Lab A: Motion from Tracking Data

**Mean acceleration measured:**
- -8.58 m/s^2 (std 28.7 m/s^2), close to the expected -9.81 m/s^2 of free fall. The
  mean is slightly off because the finite-difference derivative is least accurate at the
  endpoints, where noise affects it most.

**Why the acceleration is noisy:**
- A derivative compares neighbouring measurements, so the small random errors in position
  get magnified each time we differentiate. Acceleration needed two derivatives, so the
  noise grew much larger than in the position data.

**What integrating back showed:**
- Integrating the noisy acceleration twice recovered the position to within 0.785 m of the
  original, because integration is a sum and random noise partly cancels out. Integration
  suppresses noise, the opposite of differentiation.



**Bonus - 2D trajectory:**
- Differentiating x and y separately with np.gradient gave a mean speed of about
  23.7 and a maximum speed of about 38.7. The speed curve shows small fluctuations
  caused by measurement noise, but only one derivative was needed, so it is much
  cleaner than the acceleration in the free-fall data.



---

## PW2 - Lab B: Optimization in Chemistry

**Part 2 - Three routes to a minimum:**
- On the easy convex function f(x), all three methods (gradient descent, Newton, SLSQP)
  agreed and found x = 3, the single global minimum.
- On the harder landscape g(x), the methods did not always agree. Starting from x0=0,
  Newton's method converged to x = 0.17, which turned out to be a maximum (g''(x) < 0),
  while gradient descent and SLSQP both found the minimum near x = -1.30. Starting from
  x0=2, Newton correctly found a minimum at x = 1.13 (g''(x) > 0), but SLSQP converged to
  the other minimum near x = -1.30 instead. This shows that on a complicated landscape,
  the starting point strongly affects which stationary point each method finds, and Newton's
  method needs the curvature check to confirm whether it landed on a minimum or a maximum.


**Part 3 - Kinetics fit:**
- Fitted rate constant k = 0.2618, close to the expected ~0.25. The fitted curve
  passes closely through the noisy measured concentration data.

**Part 4 - Chemical equilibrium:**
- Both Newton's method and SLSQP converged to the same extent, x = 0.6638.
  Equilibrium amounts: H2 = 0.3362 mol, I2 = 0.3362 mol, HI = 1.3277 mol.

**Part 5 (bonus) - Titration equivalence point:**
- The pH curve's slope peaks at V = 50.00 mL, which is the equivalence point,
  matching the steep jump visible in the pH curve.






---

## PW3 - Data, Distributions, Testing, and Causation

Dataset: Heart Disease (Cleveland), Kaggle / UCI, 303 patients.

### Session 1 - Distributions and normality

**Shapes:**
- age: roughly bell-shaped, centred around 55-60, slightly bumpy.
- chol: skewed to the right with a long tail and one extreme value near 564.
- trestbps: skewed to the right, bumpy because blood pressure is recorded in round numbers.
- thalach: skewed to the left, most patients near 160 with a tail of low values.

**Normality verdicts (Q-Q plot + Shapiro-Wilk):**
- age: approximately normal. Shapiro rejects it (p = 0.006), but with n = 303 the test is very
  sensitive, while the Q-Q points follow the line closely and the skewness is small (-0.21).
- chol: not normal. p = 6e-09, skewness 1.14, and the Q-Q plot bends sharply away at the top.
- trestbps: not normal. p = 2e-06, skewness 0.71, Q-Q plot bends upward at the top.
- thalach: not normal (mildly). p = 7e-05, skewness -0.54, Q-Q tails leave the line.
  Because of this, a non-parametric test will be used in Session 2.


### Session 2 - Conclusions

**Heart rate comparison (thalach, disease vs healthy):**
- Because thalach is not normal (Session 1), I used the Mann-Whitney U test (two-tailed) and
  cross-checked with a t-test. Mann-Whitney: p = 1.9e-13; t-test: p = 3.5e-14.
- Healthy patients: mean 158.4 +/- 1.5 (SE), disease patients: mean 139.3 +/- 1.9 (SE).
  The 95% intervals ([155.4, 161.4] and [135.4, 143.1]) do not overlap, which agrees with the
  test. Conclusion: reject H0, the groups truly differ, healthy patients reach about 19 bpm
  higher maximum heart rate.

**Age vs thalach:**
- Pearson r = -0.39, Spearman rho = -0.39 (p ~ 1e-12): older patients tend to reach a lower
  maximum heart rate. The relationship is moderate (age explains about 15% of the variance).

**Chemical mystery:**
- Naive analysis: cadmium vs malignancy r = 0.88, benzene vs malignancy r = 0.39. Taken at
  face value, cadmium looks like the cause.
- Third variable: pollution_index is almost identical to cadmium (r = 0.98) and is also
  strongly linked to malignancy (r = 0.90), while it is unrelated to benzene (r = 0.05).
- After holding pollution_index roughly fixed (narrow bands), cadmium's association drops to
  about 0.3 while benzene's association rises to about 0.7. So benzene is the real cause and
  cadmium only looked guilty because it tracks pollution (a confounder). The cadmium value
  does not reach exactly zero because the bands are still wide enough for pollution to vary.

**Bonus - entropy of target:**
- Proportions 54.1% / 45.9%, entropy = 0.995 bits (maximum 1 bit): the column is almost
  perfectly balanced, so the category is hard to guess.



---

## PW4 - Machine Learning

### Session A - Concrete strength

Dataset: UCI Concrete Compressive Strength, I-C. Yeh (1998), "Modeling of strength of
high-performance concrete using artificial neural networks", Cement and Concrete Research
28(12). 1030 laboratory tests, 8 inputs, 1 output, no missing values.

**Variables and units:**
- cement, slag (blast furnace slag), ash (fly ash), water, superplastic (superplasticizer),
  coarse_agg, fine_agg: kg per m3 of concrete.
- age: days (1 to 365).
- strength (target): compressive strength in MPa.


**Cleaning (A2):**
- 25 duplicate rows found and removed (1030 -> 1005 rows); no missing values.
- A row appearing twice is a problem for a train/test split: the same row can land in both
  parts, so the model is tested on an example it has already seen, and the test score looks
  better than it really is (data leakage).
- Largest numerical scales: coarse_agg (~974) and fine_agg (~773), then water and cement;
  superplastic (~6) is far smaller. Scaling will matter later.
- strength vs cement: positive trend but very scattered, cement alone does not determine strength.
- strength vs age: grows quickly in the first weeks then flattens (curved, not a straight line).



**Linear regression (A4):**
strength = -23.39 + 0.1167 cement + 0.0981 slag + 0.0846 ash - 0.1314 water
+ 0.3315 superplastic + 0.0155 coarse_agg + 0.0207 fine_agg + 0.1106 age
(MPa per kg/m3 for ingredients, MPa per day for age; intercept in MPa)

| model | train RMSE | test RMSE | test MAE | train R2 | train adj R2 | test R2 |
|---|---|---|---|---|---|---|
| linear | 10.00 | 11.19 | 8.90 | 0.61 | 0.606 | 0.58 |

Residuals vs age (log axis): the residuals are negative at 3-7 days, positive at 28-100
days and negative again at 180-365 days, an arch shape. A systematic pattern means the
model is missing structure: here the effect of age is curved (strong early growth that
flattens), but a linear model forces a straight line. Train and test errors are close, so
this is underfitting, not overfitting.


**Polynomial regression (A5):**

| degree | p | train RMSE | test RMSE | train R2 | train adj R2 | test R2 |
|---|---|---|---|---|---|---|
| 1 | 8 | 10.00 | 11.19 | 0.610 | 0.606 | 0.580 |
| 2 | 44 | 6.99 | 8.31 | 0.809 | 0.798 | 0.769 |
| 3 | 164 | 4.40 | 5.95 | 0.925 | 0.905 | 0.881 |
| 4 | 494 | 2.33 | 39.41 | 0.979 | 0.945 | -4.206 |

I would choose degree 3: it has the lowest test error (RMSE 5.95, R2 0.88), and going
from degree 1 to 3 keeps improving the test score. At degree 4 there are 494 features for
only 804 training rows, so the model memorises the training data: train RMSE drops to 2.33
while test RMSE explodes to 39.4 (negative test R2). Adjusted R2 does not protect against
this: it is computed on training data and gives degree 4 the highest value (0.945), so only
the score on unseen data reveals the overfitting. (Note: choosing the degree with the test
set slightly reuses it; cross-validation would be the cleaner way.)


**Classification (A6):** target = strength >= 40 MPa (35.8% class 1, 64.2% class 0; always
guessing "no" would give 64.2% accuracy).

| K | train acc | test acc |
|---|---|---|
| 1 | 0.998 | 0.831 |
| 3 | 0.934 | 0.801 |
| 5 | 0.907 | 0.816 |
| 7 | 0.893 | 0.836 |
| 15 | 0.848 | 0.826 |
| 25 | 0.841 | 0.806 |
| 51 | 0.805 | 0.781 |
| 101 | 0.757 | 0.736 |

I chose K = 7 (best test accuracy, much smaller train-test gap than K = 1). With the
scaler the test accuracy is 0.836, without it 0.821. Over five splits (random_state 0-4)
the test accuracy was 0.801, 0.851, 0.821, 0.836, 0.806 (mean 0.823, std 0.019), so the
scaler difference (0.015) and the differences between K = 1, 7 and 15 are within noise;
only large differences (e.g. K = 101 vs K = 7, about 0.10) are meaningful.

| max_depth | leaves | train acc | test acc |
|---|---|---|---|
| 1 | 2 | 0.755 | 0.701 |
| 2 | 4 | 0.755 | 0.701 |
| 3 | 8 | 0.840 | 0.796 |
| 4 | 16 | 0.869 | 0.826 |
| 5 | 26 | 0.889 | 0.846 |
| 6 | 38 | 0.930 | 0.841 |
| 8 | 61 | 0.973 | 0.856 |
| None | 80 | 0.998 | 0.881 |

The train-test gap stays near 0.04-0.05 up to depth 5 and doubles from depth 6. I chose
depth 5 (26 leaves): the last depth before the gap grows, still readable. The unlimited tree
has the best test accuracy (0.881) but 80 leaves cannot be read, so we lose


**Metrics (A7):**

| model | TP | FP | FN | TN | accuracy | precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|
| KNN (K=7) | 54 | 15 | 18 | 114 | 0.836 | 0.783 | 0.750 | 0.766 |
| Tree (depth=5) | 58 | 17 | 14 | 112 | 0.846 | 0.773 | 0.806 | 0.789 |

The dangerous mistake is a false positive (the model says the mix reaches 40 MPa but it
does not): weak concrete could be used in a structure. It is controlled by precision
= TP/(TP+FP). A false negative only wastes good concrete and is controlled by recall.

KNN at different thresholds on the predicted probability of class 1:

| threshold | TP | FP | FN | TN | precision | recall |
|---|---|---|---|---|---|---|
| 0.3 | 61 | 23 | 11 | 106 | 0.726 | 0.847 |
| 0.5 | 54 | 15 | 18 | 114 | 0.783 | 0.750 |
| 0.7 | 39 | 11 | 33 | 118 | 0.780 | 0.542 |
| 0.9 | 18 | 1 | 54 | 128 | 0.947 | 0.250 |

I choose threshold 0.9: only 1 false positive and precision 0.947, which matters most
when weak concrete is dangerous. The price is recall 0.25: three quarters of the mixes
that really reach 40 MPa are rejected, so many good mixes need extra testing.


**Feature importance (A8):**

| | raw coef | std coef | tree | perm KNN | perm tree |
|---|---|---|---|---|---|
| cement | 0.117 | 12.12 | 0.253 | 0.165 | 0.170 |
| slag | 0.098 | 8.44 | 0.036 | 0.055 | 0.009 |
| ash | 0.085 | 5.44 | 0.037 | 0.016 | 0.000 |
| water | -0.131 | -2.83 | 0.095 | 0.068 | 0.012 |
| superplastic | 0.332 | 1.97 | 0.164 | 0.066 | 0.188 |
| coarse_agg | 0.016 | 1.20 | 0.011 | 0.038 | 0.002 |
| fine_agg | 0.021 | 1.67 | 0.091 | 0.081 | 0.072 |
| age | 0.111 | 6.89 | 0.313 | 0.176 | 0.165 |

Raw coefficients have different units (per kg/m3, per day) and depend on each variable's
scale: superplastic ranks first by raw coefficient only because it varies over a small
range. The standardised coefficient is the raw one times the standard deviation of the
input (MPa per standard deviation), which makes inputs comparable; superplastic then falls
to sixth place. The methods agree that cement and age are among the three most important
inputs. They disagree on slag (high only in the linear model) and superplastic (first only
for the permutation importance of one tree). The linear model underestimates age because
its effect is curved. This is consistent with age being key, but water appears only
mid-ranked because the engineers' water-to-cement


**Bonus - physics-chosen features (plain LinearRegression):**

| features | p | test RMSE | test R2 |
|---|---|---|---|
| raw inputs | 8 | 11.19 | 0.580 |
| log(age) | 8 | 7.65 | 0.804 |
| log(age) + w/b | 8 | 7.60 | 0.806 |
| polynomial degree 2 | 44 | 8.31 | 0.769 |
| polynomial degree 3 | 164 | 5.95 | 0.881 |

Replacing age by log(age) alone raised the linear model's test R2 from 0.58 to 0.80 with
the same 8 features, better than the 44-feature degree-2 polynomial. Replacing water by the
water-to-binder ratio added almost nothing (0.806). Domain knowledge (strength grows with
the logarithm of age) gave more than blind flexibility per added feature; degree 3 is still
better (0.88) but uses 164 features and degree 4 showed how flexibility can overfit.