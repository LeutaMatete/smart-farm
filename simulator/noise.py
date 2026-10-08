"""Sensor imperfections for the farm simulator.

Every function takes an explicit random generator, so results are reproducible:
the same seed always gives the same data.
"""
import random  # noqa: F401  (callers pass in random.Random(seed))


class TwoStateMarkov:
    """A chain that flips between OFF and ON.

    Each step: if OFF, switch ON with probability p_enter;
               if ON, switch OFF with probability p_exit.
    Long-run fraction of time ON = p_enter / (p_enter + p_exit).
    Mean length of an ON period = 1 / p_exit steps.
    """

    def __init__(self, p_enter, p_exit, rng):
        self.p_enter = p_enter
        self.p_exit = p_exit
        self.rng = rng
        self.on = False

    def step(self):
        if self.on:
            if self.rng.random() < self.p_exit:
                self.on = False
        else:
            if self.rng.random() < self.p_enter:
                self.on = True
        return self.on


def gaussian_noise(value, sigma, rng):
    return value + rng.gauss(0.0, sigma)


def maybe_spike(value, p, rng, low=10.0, high=30.0):
    """With probability p, add a spike of random size and sign."""
    if rng.random() < p:
        sign = 1 if rng.random() < 0.5 else -1
        return value + sign * rng.uniform(low, high)
    return value


def clamp(value, lo, hi):
    return max(lo, min(hi, value))