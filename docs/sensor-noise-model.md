# Sensor Noise Model v0.1

Real sensors are imperfect. The simulator adds four kinds of imperfection so
that validation, anomaly detection and alerts are tested against messy data.
All numbers are our own assumptions, chosen to be plausible. They are not
measurements of a specific sensor.

| Effect            | Model                                   | Parameters                             |
|-------------------|-----------------------------------------|----------------------------------------|
| Measurement noise | Gaussian added to the true value        | moisture sigma 0.8 points, temp 0.3 C  |
| Spikes            | Bernoulli event, uniform size, random sign | p = 0.002 per reading, size 10 to 30 |
| Lost messages     | Two-state Markov chain (good/bad)       | p_enter 0.01, p_exit 0.3               |
| Stuck sensor      | Two-state Markov chain (working/stuck)  | p_enter 0.00005, p_exit 1/288          |

Readings are every 10 minutes, so 144 per day.

## Why these distributions
(write this yourself)

## Derived numbers (do these by hand, then compare with the tests)
1. Long-run fraction of messages lost = p_enter / (p_enter + p_exit)
2. Mean length of a loss burst = 1 / p_exit readings. How many minutes is that?
3. Fraction of time a sensor is stuck, and expected stuck events per node per year.