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