# Project Charter: Smart Farm Platform

## Problem
Farmers in cool highland areas such as Qacha's Nek, Lesotho, have to decide
what to plant and when to water, often without data on their soil or weather.
Wrong crop choices and badly timed watering can waste a season, water and money.
(Hypothesis: to be tested in the Phase 2 user interviews.)

## Users
- Primary: a smallholder farmer or home gardener who owns a smartphone.
- Secondary: a farm manager or agricultural extension officer who looks after
  several fields.

## What we will build
1. A farm simulator (virtual soil, weather, sensors and a pump).
2. A messaging and data pipeline.
3. A Crop Advisor that ranks crops for a field and explains why.
4. An irrigation brain that decides when to water.
5. A mobile-first app for farmers.
6. An AI assistant that answers questions using live data.

## Non-goals
- No real hardware at Level 0 (everything is simulated).
- Not a commercial product yet.
- No real farmer data; synthetic data only.
- No claims that the advice is accurate on real farms until it is tested with
  real soil and yield data.

## Success metrics
1. Water saved: the best irrigation strategy uses at least 15% less water than a
   fixed schedule, with no more crop stress events (target to be revised after
   the Phase 3 experiments).
2. Advisor quality: Crop Advisor rankings correlate with simulated yields
   (Spearman correlation of at least 0.6 across 100 simulated fields).
3. Alert speed: a moisture alert reaches the app within 30 seconds of the
   reading in the simulation.

## First simulated site
Qacha's Nek, Lesotho: cool highland climate, summer rainfall, winter frost.