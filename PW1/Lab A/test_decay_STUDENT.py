"""
Tests for the decay simulation.

One complete test is given as a model. Add the two tests described in the
lab handout (a negative-rate test, and a test against the analytical law).
Run with:  pytest -v
"""

import numpy as np
import pytest
from decay import simulate, simulate_loop


def test_starts_at_N0():
    # at time zero, no atoms have decayed yet
    assert simulate(1000, 0.4)[0] == 1000

def test_rejects_negative_rate():
    with pytest.raises(ValueError):
        simulate(1000, -0.4)


def test_matches_law():
    N0, lam = 1000, 0.4
    t = 200 * 0.05  # steps * dt
    results = [simulate(N0, lam, seed=s)[-1] for s in range(300)]
    avg = np.mean(results)
    expected = N0 * np.exp(-lam * t)
    assert avg == pytest.approx(expected, rel=0.05)

