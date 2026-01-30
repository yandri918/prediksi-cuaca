"""
Current Weather Dashboard
Comprehensive real-time weather information
"""
import streamlit as st
import sys
import os
import plotly.graph_objects as go
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_current_weather, get_weather_emoji, get_weather_description
from utils.moon_phase import calculate_moon_phase

# Page configuration
st.set_page_config(
    page_title="Current Weather",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-box {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌤️ Current Weather Dashboard")
st.markdown("**Real-time weather conditions for your selected location**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Fetch current weather
with st.spinner("Fetching current weather data..."):
    weather = get_current_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon']
    )

if weather:
    emoji = get_weather_emoji(weather.get('weather_code', 0))
    description = get_weather_description(weather.get('weather_code', 0))
    
    # Main weather display
    st.markdown(f"""
    <div class="weather-card">
        <div style="font-size: 5rem;">{emoji}</div>
        <h2 style="margin: 1rem 0;">{description}</h2>
        <h1 style="font-size: 4rem; margin: 0;">{weather.get('temperature', 'N/A')}°C</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Feels like {weather.get('feels_like', 'N/A')}°C</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed metrics
    st.markdown("### 📊 Detailed Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 2rem;">💧</div>
            <h3>{weather.get('humidity', 'N/A')}%</h3>
            <p style="color: #666; margin: 0;">Humidity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 2rem;">🌬️</div>
            <h3>{weather.get('wind_speed', 'N/A')} km/h</h3>
            <p style="color: #666; margin: 0;">Wind Speed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 2rem;">🌡️</div>
            <h3>{weather.get('pressure', 'N/A')} hPa</h3>
            <p style="color: #666; margin: 0;">Pressure</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 2rem;">☁️</div>
            <h3>{weather.get('cloud_cover', 'N/A')}%</h3>
            <p style="color: #666; margin: 0;">Cloud Cover</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional Detailed Metrics
    st.markdown("### 🔬 Advanced Atmospheric Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate dew point (approximation)
        temp = weather.get('temperature', 0)
        humidity = weather.get('humidity', 0)
        
        # Magnus formula for dew point
        a = 17.27
        b = 237.7
        alpha = ((a * temp) / (b + temp)) + (humidity / 100.0)
        dew_point = (b * alpha) / (a - alpha) if alpha < a else temp
        
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0;">
            <h4 style="margin: 0 0 1rem 0;">💧 Dew Point</h4>
            <h2 style="color: #4299e1; margin: 0;">{dew_point:.1f}°C</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Temperature at which air becomes saturated
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Precipitation
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0;">
            <h4 style="margin: 0 0 1rem 0;">🌧️ Precipitation</h4>
            <h2 style="color: #4299e1; margin: 0;">{weather.get('precipitation', 0):.1f} mm</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Current precipitation amount
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Altimeter / Barometer
        pressure = weather.get('pressure', 1013.25)
        
        # Calculate approximate altitude from pressure (barometric formula)
        # Standard atmosphere: P = P0 * (1 - 0.0065*h/288.15)^5.255
        # Solving for h: h = 288.15/0.0065 * (1 - (P/P0)^(1/5.255))
        P0 = 1013.25  # Sea level standard pressure
        altitude = (288.15 / 0.0065) * (1 - (pressure / P0) ** (1 / 5.255))
        
        # Pressure tendency (simplified)
        if pressure > 1020:
            pressure_trend = "High - Fair weather expected"
            trend_color = "#48bb78"
            trend_icon = "📈"
        elif pressure < 1000:
            pressure_trend = "Low - Stormy weather possible"
            trend_color = "#e53e3e"
            trend_icon = "📉"
        else:
            pressure_trend = "Normal - Stable conditions"
            trend_color = "#4299e1"
            trend_icon = "➡️"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 12px; color: white;">
            <h4 style="margin: 0 0 1rem 0;">🎚️ Altimeter / Barometer</h4>
            <h2 style="margin: 0;">{pressure:.2f} hPa</h2>
            <p style="opacity: 0.9; margin: 0.5rem 0; font-size: 0.9rem;">
                {pressure * 0.02953:.2f} inHg
            </p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 1rem 0;">
            <p style="margin: 0.3rem 0;"><b>Estimated Altitude:</b> {altitude:.0f} m ({altitude * 3.28084:.0f} ft)</p>
            <p style="margin: 0.3rem 0;"><b>Trend:</b> {trend_icon} {pressure_trend}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Wind Gusts
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0;">
            <h4 style="margin: 0 0 1rem 0;">💨 Wind Gusts</h4>
            <h2 style="color: #9f7aea; margin: 0;">{weather.get('wind_gusts', 'N/A')} km/h</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Maximum wind gust speed
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Atmospheric Conditions Analysis
    st.markdown("### 🌍 Atmospheric Conditions Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Comfort Index
        comfort_index = "Comfortable"
        comfort_color = "#48bb78"
        
        if temp > 30 or temp < 10:
            comfort_index = "Uncomfortable"
            comfort_color = "#e53e3e"
        elif temp > 25 or temp < 15:
            comfort_index = "Moderate"
            comfort_color = "#ed8936"
        
        st.markdown(f"""
        **🌡️ Comfort Level**
        
        <div style="background: {comfort_color}; color: white; padding: 0.5rem 1rem; 
                    border-radius: 8px; text-align: center; font-weight: 700;">
            {comfort_index}
        </div>
        
        Based on temperature: {temp}°C
        """, unsafe_allow_html=True)
    
    with col2:
        # Air Quality Indicator (based on pressure and humidity)
        if humidity < 30:
            air_quality = "Dry Air"
            aq_color = "#ed8936"
        elif humidity > 70:
            air_quality = "Humid Air"
            aq_color = "#4299e1"
        else:
            air_quality = "Good"
            aq_color = "#48bb78"
        
        st.markdown(f"""
        **💨 Air Quality Indicator**
        
        <div style="background: {aq_color}; color: white; padding: 0.5rem 1rem; 
                    border-radius: 8px; text-align: center; font-weight: 700;">
            {air_quality}
        </div>
        
        Humidity: {humidity}%
        """, unsafe_allow_html=True)
    
    with col3:
        # Weather Stability
        if 1010 <= pressure <= 1020:
            stability = "Stable"
            stab_color = "#48bb78"
        elif pressure > 1020:
            stability = "Very Stable"
            stab_color = "#4299e1"
        else:
            stability = "Unstable"
            stab_color = "#e53e3e"
        
        st.markdown(f"""
        **⚖️ Weather Stability**
        
        <div style="background: {stab_color}; color: white; padding: 0.5rem 1rem; 
                    border-radius: 8px; text-align: center; font-weight: 700;">
            {stability}
        </div>
        
        Pressure: {pressure:.1f} hPa
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Astronomical Data
    st.markdown("### 🌅 Astronomical Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sunrise & Sunset
        sunrise = weather.get('sunrise')
        sunset = weather.get('sunset')
        
        if sunrise and sunset:
            # Parse times
            sunrise_time = datetime.fromisoformat(sunrise.replace('Z', '+00:00'))
            sunset_time = datetime.fromisoformat(sunset.replace('Z', '+00:00'))
            
            # Calculate daylight duration
            daylight_seconds = (sunset_time - sunrise_time).total_seconds()
            daylight_hours = daylight_seconds / 3600
            daylight_minutes = (daylight_seconds % 3600) / 60
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); 
                        padding: 1.5rem; border-radius: 12px; color: white;">
                <h4 style="margin: 0 0 1rem 0;">🌅 Sunrise & Sunset</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <p style="margin: 0; opacity: 0.9;">Sunrise</p>
                        <h3 style="margin: 0.3rem 0;">{sunrise_time.strftime('%H:%M')}</h3>
                    </div>
                    <div>
                        <p style="margin: 0; opacity: 0.9;">Sunset</p>
                        <h3 style="margin: 0.3rem 0;">{sunset_time.strftime('%H:%M')}</h3>
                    </div>
                </div>
                <hr style="border-color: rgba(255,255,255,0.3); margin: 1rem 0;">
                <p style="margin: 0;"><b>Daylight Duration:</b> {int(daylight_hours)}h {int(daylight_minutes)}m</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Sunrise/Sunset data not available")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sunshine Duration
        sunshine_duration = weather.get('sunshine_duration', 0)
        sunshine_hours = sunshine_duration / 3600
        
        # Calculate sunshine percentage
        if sunrise and sunset:
            sunshine_percentage = (sunshine_duration / daylight_seconds) * 100 if daylight_seconds > 0 else 0
        else:
            sunshine_percentage = 0
        
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0;">
            <h4 style="margin: 0 0 1rem 0;">☀️ Sunshine Duration</h4>
            <h2 style="color: #f6d365; margin: 0;">{sunshine_hours:.1f} hours</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0;">
                {sunshine_percentage:.1f}% of daylight hours
            </p>
            <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-top: 1rem; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #f6d365 0%, #fda085 100%); 
                            height: 100%; width: {sunshine_percentage}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Moon Phase
        moon_data = calculate_moon_phase()
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
            <h4 style="margin: 0 0 1rem 0;">🌙 Moon Phase</h4>
            <div style="font-size: 5rem; margin: 1rem 0;">{moon_data['emoji']}</div>
            <h3 style="margin: 0.5rem 0;">{moon_data['phase_name']}</h3>
            <p style="opacity: 0.9; margin: 0.5rem 0;">
                Illumination: {moon_data['illumination']}%
            </p>
            <p style="opacity: 0.9; margin: 0; font-size: 0.9rem;">
                Age: {moon_data['age_days']:.1f} days
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Current Time & Timezone
        current_time = datetime.now()
        timezone = weather.get('timezone', 'UTC')
        
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0;">
            <h4 style="margin: 0 0 1rem 0;">🕐 Current Time</h4>
            <h2 style="color: #667eea; margin: 0;">{current_time.strftime('%H:%M:%S')}</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0;">
                {current_time.strftime('%A, %B %d, %Y')}
            </p>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Timezone: {timezone}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Wind information
    st.markdown("### 🌬️ Wind Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Wind compass
        wind_dir = weather.get('wind_direction', 0)
        wind_speed = weather.get('wind_speed', 0)
        
        fig = go.Figure()
        
        # Add compass
        fig.add_trace(go.Scatterpolar(
            r=[wind_speed],
            theta=[wind_dir],
            mode='markers+text',
            marker=dict(size=20, color='#667eea'),
            text=[f'{wind_speed} km/h'],
            textposition='top center'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(wind_speed * 1.5, 20)]),
                angularaxis=dict(direction='clockwise', rotation=90)
            ),
            showlegend=False,
            title="Wind Direction",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        **Wind Details:**
        - **Speed:** {weather.get('wind_speed', 'N/A')} km/h
        - **Direction:** {weather.get('wind_direction', 'N/A')}°
        - **Gusts:** {weather.get('wind_gusts', 'N/A')} km/h
        
        **Precipitation:**
        - **Current:** {weather.get('precipitation', 'N/A')} mm
        
        **Last Updated:**
        - {weather.get('time', 'N/A')}
        """)
    
    st.markdown("---")
    
    # Quick navigation
    st.markdown("### 🎯 View More")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 7-Day Forecast", use_container_width=True):
            st.switch_page("pages/03_📅_7-Day_Forecast.py")
    
    with col2:
        if st.button("⏰ Hourly Forecast", use_container_width=True):
            st.switch_page("pages/04_⏰_Hourly_Forecast.py")
    
    with col3:
        if st.button("🗺️ Change Location", use_container_width=True):
            st.switch_page("pages/01_🗺️_Interactive_Map.py")

else:
    st.error("❌ Unable to fetch weather data. Please try again or select a different location.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
