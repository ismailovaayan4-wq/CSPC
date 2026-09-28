"""
Motion from tracking data: position -> velocity -> acceleration, then integrate back.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# Part 2a: read the data
data = np.loadtxt("freefall.csv", delimiter=",", skiprows=1)
t = data[:, 0]
y = data[:, 1]

# Part 2b: differentiate twice
v = np.gradient(y, t)   # velocity from position
a = np.gradient(v, t)   # acceleration from velocity

# Part 2c + Part 3: mean and standard deviation of acceleration
print(f"Mean acceleration: {a.mean():.3f} m/s^2")
print(f"Std of acceleration: {a.std():.3f} m/s^2")

# Part 4: integrate back
v_rec = cumulative_trapezoid(a, t, initial=0) + v[0]
y_rec = cumulative_trapezoid(v_rec, t, initial=0) + y[0]
print(f"Largest position difference: {np.max(np.abs(y_rec - y)):.3f} m")

# Part 5: three stacked panels sharing the time axis
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 8))

ax1.plot(t, y)
ax1.set_ylabel("position (m)")

ax2.plot(t, v)
ax2.set_ylabel("velocity (m/s)")

ax3.plot(t, a)
ax3.axhline(-9.81, linestyle="--", color="red", label="-9.81")
ax3.set_ylabel("acceleration (m/s²)")
ax3.set_xlabel("time (s)")
ax3.legend()

plt.tight_layout()
plt.savefig("motion.png")