"""
Current Weather Dashboard
Comprehensive real-time weather information
"""
import streamlit as st
import sys
import os
import plotly.graph_objects as go

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_current_weather, get_weather_emoji, get_weather_description

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
