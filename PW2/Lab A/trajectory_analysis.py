"""
Bonus: 2D tracked trajectory - path and speed over time.
"""

import numpy as np
import matplotlib.pyplot as plt

# read time, x, y
data = np.loadtxt("trajectory.csv", delimiter=",", skiprows=1)
t = data[:, 0]
x = data[:, 1]
y = data[:, 2]

# differentiate each coordinate separately
vx = np.gradient(x, t)
vy = np.gradient(y, t)

# speed = sqrt(vx^2 + vy^2)
speed = np.sqrt(vx**2 + vy**2)

print(f"Mean speed: {speed.mean():.3f}")
print(f"Max speed: {speed.max():.3f}")

# two panels: path (x vs y) and speed over time
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot(x, y)
ax1.set_title("Path")
ax1.set_xlabel("x")
ax1.set_ylabel("y")

ax2.plot(t, speed)
ax2.set_title("Speed over time")
ax2.set_xlabel("time (s)")
ax2.set_ylabel("speed")

plt.tight_layout()
plt.savefig("trajectory.png")

