# Soil Moisture Model v0.1

A single "bucket" model of the root zone.
State: theta = volumetric soil moisture in % (reported by sensors as moisture_pct).

## Soil constants (% volumetric; approximate, verified and cited in Step 6)
  texture	wilting_pt	field_cap	saturation	drainage_d (per day)
sand	6	17	43	10
loam	12	28	47	2
clay	20	32	47	0.5

wilting_pt  = below this, plants cannot extract water
field_cap   = water the soil holds after excess has drained
saturation  = all pores full; anything more runs off

## Other constants
    Z      = root zone depth = 300 mm
    dt     = 10 minutes = 1/144 day
    T_ref  = 20 C
    k_peak = peak drying rate per day (derived in Exercise 2)

## Equations
(1) Available water:        W = theta - wilting_pt
(2) Drying rate:            dW/dt = -k * W
                            k = k_peak * 2^((T - T_ref)/10) * s(h)
                            k = 0 if T <= 0 C
                            s(h) = max(0, sin(pi * (h - 6) / 12))
                            h = hour of day (0 to 24); daylight is 06:00 to 18:00
(3) Exact step solution:    W_new = W * e^(-k * dt)
(4) Water in:               theta += (rain_mm + irrigation_mm) / Z * 100
(5) Runoff cap:             theta = min(theta, saturation)
(6) Drainage:               if theta > field_cap:
                                theta = field_cap + (theta - field_cap) * e^(-d * dt)
(7) Irrigation depth:       irrigation_mm = flow_L_per_min * minutes / area_m2

Update order each time step: (3) drying, (4) water in, (5) cap, (6) drainage.

## Why these choices
(write this yourself after the exercises)

## Exercises
## Exercise answers

### Exercise 1: check the solution
W(t) = W0 * e^(-k*t)
dW/dt = W0 * (-k) * e^(-k*t) = -k * W(t), so it solves the equation.
Initial condition: W(0) = W0 * e^0 = W0, so it starts at the right value.
Units: k*t is dimensionless and t is in days, so k is in 1/day.

### Exercise 2: half-life, daylight average, k_peak
1. Half-life (constant k): W0/2 = W0 * e^(-k*t), so 1/2 = e^(-k*t),
   so -ln 2 = -k*t, so t_half = ln 2 / k.
2. Daylight average. Substitute u = pi*(h-6)/12, so dh = (12/pi) du,
   and h = 6..18 becomes u = 0..pi.
   Integral of sin(u) from 0 to pi = [-cos u] = 1 + 1 = 2.
   So the integral over the day = (12/pi) * 2 = 24/pi (about 7.64).
   s(h) is zero at night, so dividing by 24 hours gives the daily average
   of s = 1/pi (about 0.318).
3. We want an average k of ln 2 / 5 at 20 C (temperature factor = 1):
   k_peak * (1/pi) = ln 2 / 5
   k_peak = pi * ln 2 / 5 = 0.4355 per day.
   Check: the daily average k is 0.4355 / pi = 0.1386 per day,
   which gives a half-life of ln 2 / 0.1386 = 5.0 days.
Why the average is enough: with k changing through the day,
W(t) = W0 * exp(-integral of k dt), so over whole days only the daily
integral of k matters.
Temperature effect: the factor 2^((T-20)/10) means the half-life is about
10 days at 10 C and 2.5 days at 30 C.

### Exercise 3: irrigation
20 L/min * 30 min = 600 L over 100 m2 = 6 L/m2 = 6 mm.
Rise in theta = 6 / 300 * 100 = 2 percentage points.
Context: loam holds 28 - 12 = 16 points of available water = 48 mm in the
300 mm root zone, so 6 mm is only one eighth of it. Refilling 10 points
needs 30 mm = 3000 L = 150 minutes at 20 L/min.

### Exercise 4: why e^(-k*dt) and not W - k*W*dt
The simple version gives W_new = W * (1 - k*dt). With k*dt = 1.5 that is
W * (-0.5): NEGATIVE available water, which is impossible.
The exact version gives W * e^(-1.5) = 0.223 * W, which is always positive.
Simple stepping is only safe when k*dt is well below 1.
At our 10-minute step, k*dt is about 0.006 even at 30 C, so both methods
agree and the simple one would not visibly fail. We still use the exact
form as insurance, because later we will use big time steps (a whole day)
to generate machine learning data quickly. At 40 C noon, k is about 1.7 per
day, so with a one-day step the simple method would break.
This is tested in tests/test_field.py.

## Why these choices
- Bucket model: simple enough to understand and test, and it has the three
  states that matter to a farmer (wilting point, field capacity, saturation).
- Exponential drying: the less water left, the slower plants and soil can
  extract it, which matches observed drydown curves.
- Temperature doubles the rate every 10 C (a standard rule of thumb),
  and drying stops at freezing.
- Daylight factor: most evaporation and plant uptake happens in the day.
- Limits: no crop, no runoff beyond saturation, no groundwater, no slope.