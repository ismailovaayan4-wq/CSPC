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