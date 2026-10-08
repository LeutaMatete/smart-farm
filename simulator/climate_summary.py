import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("simulator/climates/qachas_nek_daily.csv", parse_dates=["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["frost"] = df["tmin_c"] < 0

rain = df.groupby(["year", "month"])["precip_mm"].sum().groupby("month").mean()
frost_days = df.groupby(["year", "month"])["frost"].sum().groupby("month").mean()

summary = pd.DataFrame({
    "tmax_c": df.groupby("month")["tmax_c"].mean(),
    "tmin_c": df.groupby("month")["tmin_c"].mean(),
    "rain_mm": rain,
    "frost_days": frost_days,
    "et0_mm_day": df.groupby("month")["et0_mm"].mean(),
}).round(1)
print(summary)

annual_rain = df.groupby("year")["precip_mm"].sum()
print(f"\nAnnual rain: mean {annual_rain.mean():.0f} mm, "
      f"min {annual_rain.min():.0f}, max {annual_rain.max():.0f}")
print(f"Annual mean temperature: {df['tmean_c'].mean():.1f} C")
print("\nMissing values per column:")
print(df.isna().sum())

fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(summary.index, summary["rain_mm"], color="tab:blue", alpha=0.4)
ax1.set_xlabel("Month")
ax1.set_ylabel("Rain (mm)")
ax1.set_xticks(range(1, 13))
ax2 = ax1.twinx()
ax2.plot(summary.index, summary["tmax_c"], "r-o", label="Mean max (C)")
ax2.plot(summary.index, summary["tmin_c"], "b-o", label="Mean min (C)")
ax2.axhline(0, color="grey", lw=0.8)
ax2.set_ylabel("Temperature (C)")
ax2.legend(loc="upper left")
ax1.set_title("Qacha's Nek monthly climate, 2016-2025 (Open-Meteo / ERA5)")
fig.tight_layout()
fig.savefig("docs/qachas_nek_climate.png", dpi=120)
print("\nSaved docs/qachas_nek_climate.png")