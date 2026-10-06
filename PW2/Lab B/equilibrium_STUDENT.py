"""
PW2 Lab B Part 4 -- chemical equilibrium.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0

# TODO 1: write k_imbalance(x) = (2x)^2/((a-x)(b-x)) - K.
#         It equals zero exactly at equilibrium.
def k_imbalance(x):
    return (2 * x) ** 2 / ((a - x) * (b - x)) - K

# TODO 2 (method 1): use scipy.optimize.newton to find the root of k_imbalance
#         (start x0=0.5). This is root-finding.
x_newton = newton(k_imbalance, x0=0.5)
print(f"Newton:   x = {x_newton:.4f}")

# TODO 3 (method 2): use scipy.optimize.minimize to minimise k_imbalance(x)**2
#         (method "SLSQP", bounds [(0, 0.999)], x0=[0.5]). Print both answers
#         and confirm they agree.
res = minimize(lambda x: k_imbalance(x[0]) ** 2, x0=[0.5], method="SLSQP", bounds=[(0, 0.999)])
x_slsqp = res.x[0]
print(f"SLSQP:    x = {x_slsqp:.4f}")
print(f"Agree? {np.isclose(x_newton, x_slsqp, atol=1e-3)}")

# TODO 4: report the equilibrium amounts (H2, I2, HI), and plot how the three
#         amounts change with the extent x, marking the equilibrium. Save
#         equilibrium.png.
x_eq = x_newton
nH2 = a - x_eq
nI2 = b - x_eq
nHI = 2 * x_eq
print(f"Equilibrium amounts: H2 = {nH2:.4f}, I2 = {nI2:.4f}, HI = {nHI:.4f}")

x_range = np.linspace(0, 0.99, 200)
plt.plot(x_range, a - x_range, label="H2")
plt.plot(x_range, b - x_range, label="I2")
plt.plot(x_range, 2 * x_range, label="HI")
plt.axvline(x_eq, color="black", linestyle="--", label=f"equilibrium x={x_eq:.3f}")
plt.xlabel("extent x")
plt.ylabel("amount (mol)")
plt.legend()
plt.savefig("equilibrium.png")