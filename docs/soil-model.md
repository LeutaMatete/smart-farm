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
(answers below)