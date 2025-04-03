import streamlit as st
import math

st.title("🌞 Solar Energy Calculator")

latitude = st.number_input("Latitude (°)", value=0.0)
longitude = st.number_input("Longitude (°)", value=0.0)
timezone = st.number_input("Time Zone Offset (UTC)", value=-7.0)
day_of_year = st.number_input("Day of Year (1–365)", min_value=1, max_value=365, value=80)
time_of_day = st.number_input("Time of Day (24h format)", value=12.0)
cloud_cover = st.slider("Cloud Cover (%)", 0, 100, 0)
panel_area = st.number_input("Panel Area (m²)", value=1.0)
efficiency = st.number_input("Efficiency (as decimal)", min_value=0.0, max_value=1.0, value=0.18)

def to_radians(deg):
    return math.pi * deg / 180

declination = 23.45 * math.sin(to_radians((360 * (284 + day_of_year)) / 365))
eot = 2.29 * math.sin(to_radians(360 * (day_of_year - 81) / 365))
time_correction = 4 * (longitude - (timezone * 15)) + eot
local_solar_time = time_of_day + time_correction / 60
hour_angle = 15 * (local_solar_time - 12)

solar_altitude = math.asin(
    math.sin(to_radians(latitude)) * math.sin(to_radians(declination)) +
    math.cos(to_radians(latitude)) * math.cos(to_radians(declination)) * math.cos(to_radians(hour_angle))
)

clear_sky_irradiance = max(0, 1000 * math.sin(solar_altitude))
cloud_constant = 0.75
cloud_factor = 1 - (cloud_cover / 100) * cloud_constant
adjusted_irradiance = clear_sky_irradiance * cloud_factor
energy_output = (adjusted_irradiance * panel_area * efficiency * 1) / 1000  # 1 hour

st.markdown("### 📈 Results")
st.write(f"**Declination:** {declination:.2f}°")
st.write(f"**Equation of Time:** {eot:.2f} min")
st.write(f"**Hour Angle:** {hour_angle:.2f}°")
st.write(f"**Clear Sky Irradiance:** {clear_sky_irradiance:.2f} W/m²")
st.write(f"**Adjusted Irradiance:** {adjusted_irradiance:.2f} W/m²")
st.write(f"**Estimated Energy Output:** {energy_output:.3f} kWh")
