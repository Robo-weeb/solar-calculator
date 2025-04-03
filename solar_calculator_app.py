import streamlit as st
import math

# --- TITLE ---
st.title("🌞 Solar Energy Calculator")

# --- USER INPUTS ---
latitude = st.number_input("Latitude (°)", value=44.08)
longitude = st.number_input("Longitude (°)", value=-103.21)
timezone = st.number_input("Time Zone Offset (UTC)", value=-7.0)
day_of_year = st.number_input("Day of Year (1–365)", min_value=1, max_value=365, value=91)
time_of_day = st.number_input("Time of Day (24h format)", value=12.0)
cloud_cover = st.slider("Cloud Cover (%)", 0, 100, 40)
panel_area = st.number_input("Solar Panel Area (m²)", value=2.0)
efficiency = st.number_input("Panel Efficiency (as decimal)", min_value=0.0, max_value=1.0, value=0.18)
hours = st.slider("Duration (Hours)", 1, 12, 1)

# --- HELPER FUNCTION ---
def to_radians(deg):
    return math.pi * deg / 180

# --- SOLAR POSITION CALCULATIONS ---
declination = 23.45 * math.sin(to_radians((360 * (284 + day_of_year)) / 365))
eot = 2.29 * math.sin(to_radians(360 * (day_of_year - 81) / 365))  # equation of time
time_correction = 4 * (longitude - (timezone * 15)) + eot
local_solar_time = time_of_day + time_correction / 60
hour_angle = 15 * (local_solar_time - 12)

# --- SOLAR ALTITUDE ANGLE ---
solar_altitude = math.asin(
    math.sin(to_radians(latitude)) * math.sin(to_radians(declination)) +
    math.cos(to_radians(latitude)) * math.cos(to_radians(declination)) * math.cos(to_radians(hour_angle))
)

# --- IRRADIANCE CALCULATIONS ---
clear_sky_irradiance = max(0, 1000 * math.sin(solar_altitude))  # W/m²
cloud_constant = 0.75
cloud_factor = 1 - (cloud_cover / 100) * cloud_constant
adjusted_irradiance = clear_sky_irradiance * cloud_factor

# --- ENERGY OUTPUT ---
energy_output = (adjusted_irradiance * panel_area * efficiency * hours) / 1000  # in kWh

# --- RESULTS ---
st.markdown("### 📊 Results")
st.write(f"**Solar Declination:** {declination:.2f}°")
st.write(f"**Equation of Time:** {eot:.2f} min")
st.write(f"**Hour Angle:** {hour_angle:.2f}°")
st.write(f"**Solar Altitude Angle:** {math.degrees(solar_altitude):.2f}°")
st.write(f"**Clear Sky Irradiance:** {clear_sky_irradiance:.2f} W/m²")
st.write(f"**Cloud Factor:** {cloud_factor:.2f}")
st.write(f"**Adjusted Irradiance:** {adjusted_irradiance:.2f} W/m²")
st.write(f"### ⚡ Estimated Energy Output: **{energy_output:.3f} kWh** (for {hours} hours)")

