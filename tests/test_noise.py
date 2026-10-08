import random
import statistics

from simulator.noise import TwoStateMarkov, clamp, gaussian_noise, maybe_spike


def draws(seed):
    rng = random.Random(seed)
    return [gaussian_noise(50.0, 1.0, rng) for _ in range(10)]


def test_same_seed_gives_same_values():
    assert draws(42) == draws(42)


def test_different_seed_gives_different_values():
    assert draws(1) != draws(2)


def test_gaussian_noise_has_requested_mean_and_sigma():
    rng = random.Random(0)
    xs = [gaussian_noise(50.0, 0.8, rng) for _ in range(20000)]
    assert abs(statistics.mean(xs) - 50.0) < 0.05
    assert abs(statistics.stdev(xs) - 0.8) < 0.03


def test_spike_frequency_matches_probability():
    rng = random.Random(0)
    values = [maybe_spike(50.0, 0.01, rng) for _ in range(50000)]
    spikes = sum(1 for v in values if v != 50.0)
    assert 400 < spikes < 600  # expected 500


def test_markov_long_run_fraction():
    chain = TwoStateMarkov(0.01, 0.3, random.Random(0))
    n = 200000
    on_steps = sum(1 for _ in range(n) if chain.step())
    expected = 0.01 / (0.01 + 0.3)
    assert abs(on_steps / n - expected) < 0.004


def test_markov_bursts_have_expected_length():
    chain = TwoStateMarkov(0.01, 0.3, random.Random(0))
    lengths, current = [], 0
    for _ in range(200000):
        if chain.step():
            current += 1
        elif current:
            lengths.append(current)
            current = 0
    assert abs(statistics.mean(lengths) - 1 / 0.3) < 0.3


def test_clamp():
    assert clamp(150, 0, 100) == 100
    assert clamp(-5, 0, 100) == 0
    assert clamp(42, 0, 100) == 42