"""
Warmup: three routes to a minimum.
"""

import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
# f(x) = (x - 3)^2 + 1, one global minimum at x = 3

def f(x):
    return (x - 3) ** 2 + 1

def f_prime(x):
    return 2 * (x - 3)

def f_double_prime(x):
    return 2

x0 = 0.0

# (1) gradient descent by hand
x = x0
learning_rate = 0.1
for _ in range(100):
    x = x - learning_rate * f_prime(x)
print(f"[2A] Gradient descent: x = {x:.4f}")

# (2) Newton's method on f'(x) = 0
x_newton = newton(f_prime, x0, fprime=f_double_prime)
print(f"[2A] Newton's method:  x = {x_newton:.4f}")

# (3) SLSQP
res = minimize(f, x0, method="SLSQP")
print(f"[2A] SLSQP:            x = {res.x[0]:.4f}")

print()

# ---------- 2B: harder landscape ----------
# g(x) = x^4 - 3x^2 + x + 5

def g(x):
    return x ** 4 - 3 * x ** 2 + x + 5

def g_prime(x):
    return 4 * x ** 3 - 6 * x + 1

def g_double_prime(x):
    return 12 * x ** 2 - 6

for start in [0.0, 2.0]:
    print(f"--- starting from x0 = {start} ---")

    # (1) gradient descent by hand
    x = start
    for _ in range(1000):
        x = x - 0.01 * g_prime(x)
    print(f"[2B] Gradient descent: x = {x:.4f}, g(x) = {g(x):.4f}")

    # (2) Newton's method on g'(x) = 0
    x_newton = newton(g_prime, start, fprime=g_double_prime)
    curvature = g_double_prime(x_newton)
    kind = "minimum" if curvature > 0 else "maximum"
    print(f"[2B] Newton's method:  x = {x_newton:.4f}, g''(x) = {curvature:.4f} -> {kind}")

    # (3) SLSQP
    res = minimize(g, start, method="SLSQP")
    print(f"[2B] SLSQP:            x = {res.x[0]:.4f}, g(x) = {res.fun:.4f}")
    print()
