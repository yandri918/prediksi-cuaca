"""
Weather Radar Visualization
Simulated weather radar with precipitation intensity
"""
import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_hourly_forecast, get_current_weather

# Page configuration
st.set_page_config(
    page_title="Weather Radar",
    page_icon="📡",
    layout="wide"
)

# Header
st.title("📡 Weather Radar Visualization")
st.markdown("**Real-time precipitation intensity and forecast radar**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Fetch data
with st.spinner("Loading radar data..."):
    current = get_current_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon']
    )
    
    hourly = get_hourly_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        hours=24
    )

if current and hourly is not None:
    # Current Radar Status
    st.markdown("## 📡 Current Radar Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        precip_now = current.get('precipitation', 0)
        if precip_now > 10:
            status = "Heavy Rain"
            color = "#e53e3e"
            icon = "🔴"
        elif precip_now > 2:
            status = "Moderate Rain"
            color = "#ed8936"
            icon = "🟠"
        elif precip_now > 0:
            status = "Light Rain"
            color = "#48bb78"
            icon = "🟢"
        else:
            status = "No Precipitation"
            color = "#4299e1"
            icon = "⚪"
        
        st.markdown(f"""
        <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
            <div style="font-size: 3rem;">{icon}</div>
            <h3 style="margin: 0.5rem 0;">{status}</h3>
            <p style="margin: 0; opacity: 0.9;">{precip_now:.1f} mm/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cloud_cover = current.get('cloud_cover', 0)
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0; text-align: center;">
            <div style="font-size: 2rem;">☁️</div>
            <h3 style="color: #2d3748; margin: 0.5rem 0;">{cloud_cover}%</h3>
            <p style="color: #666; margin: 0;">Cloud Cover</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        humidity = current.get('humidity', 0)
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0; text-align: center;">
            <div style="font-size: 2rem;">💧</div>
            <h3 style="color: #2d3748; margin: 0.5rem 0;">{humidity}%</h3>
            <p style="color: #666; margin: 0;">Humidity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        wind = current.get('wind_speed', 0)
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; border: 2px solid #e2e8f0; text-align: center;">
            <div style="font-size: 2rem;">🌬️</div>
            <h3 style="color: #2d3748; margin: 0.5rem 0;">{wind:.1f} km/h</h3>
            <p style="color: #666; margin: 0;">Wind Speed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Simulated Radar Map
    st.markdown("## 🗺️ Precipitation Radar Map")
    
    # Create simulated radar data around location
    lat = st.session_state['selected_lat']
    lon = st.session_state['selected_lon']
    
    # Generate grid
    grid_size = 20
    lat_range = np.linspace(lat - 0.5, lat + 0.5, grid_size)
    lon_range = np.linspace(lon - 0.5, lon + 0.5, grid_size)
    
    # Simulate precipitation intensity based on current conditions
    np.random.seed(int(datetime.now().timestamp()) % 1000)
    base_intensity = precip_now
    
    # Create precipitation grid with some randomness
    precip_grid = np.zeros((grid_size, grid_size))
    if base_intensity > 0:
        # Create precipitation pattern
        center_x, center_y = grid_size // 2, grid_size // 2
        for i in range(grid_size):
            for j in range(grid_size):
                distance = np.sqrt((i - center_x)**2 + (j - center_y)**2)
                precip_grid[i, j] = max(0, base_intensity * (1 - distance / (grid_size * 0.7)) + 
                                       np.random.normal(0, base_intensity * 0.3))
    
    # Create radar visualization
    fig = go.Figure(data=go.Heatmap(
        z=precip_grid,
        x=lon_range,
        y=lat_range,
        colorscale=[
            [0, 'rgba(255, 255, 255, 0)'],
            [0.1, 'rgba(144, 238, 144, 0.3)'],
            [0.3, 'rgba(135, 206, 250, 0.5)'],
            [0.5, 'rgba(65, 105, 225, 0.7)'],
            [0.7, 'rgba(255, 165, 0, 0.8)'],
            [0.9, 'rgba(255, 69, 0, 0.9)'],
            [1, 'rgba(139, 0, 0, 1)']
        ],
        colorbar=dict(
            title="Precipitation (mm/h)",
            titleside="right"
        ),
        hovertemplate='Lat: %{y:.3f}<br>Lon: %{x:.3f}<br>Intensity: %{z:.1f} mm/h<extra></extra>'
    ))
    
    # Add location marker
    fig.add_trace(go.Scattergeo(
        lat=[lat],
        lon=[lon],
        mode='markers+text',
        marker=dict(size=15, color='red', symbol='circle'),
        text=['📍 Your Location'],
        textposition='top center',
        showlegend=False
    ))
    
    fig.update_layout(
        title='Precipitation Intensity Radar',
        height=500,
        geo=dict(
            scope='world',
            projection_type='mercator',
            center=dict(lat=lat, lon=lon),
            lonaxis=dict(range=[lon - 0.6, lon + 0.6]),
            lataxis=dict(range=[lat - 0.6, lat + 0.6]),
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 24-Hour Precipitation Forecast
    st.markdown("## ⏰ 24-Hour Precipitation Forecast")
    
    # Precipitation timeline
    precip_fig = go.Figure()
    
    # Add precipitation bars
    precip_fig.add_trace(go.Bar(
        x=hourly['time'],
        y=hourly['precipitation'],
        name='Precipitation',
        marker=dict(
            color=hourly['precipitation'],
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="mm/h")
        ),
        hovertemplate='%{x}<br>Precipitation: %{y:.1f} mm/h<extra></extra>'
    ))
    
    # Add precipitation probability line
    precip_fig.add_trace(go.Scatter(
        x=hourly['time'],
        y=hourly['precipitation_probability'],
        name='Probability',
        yaxis='y2',
        line=dict(color='orange', width=2),
        hovertemplate='%{x}<br>Probability: %{y:.0f}%<extra></extra>'
    ))
    
    precip_fig.update_layout(
        title='Hourly Precipitation Forecast',
        xaxis_title='Time',
        yaxis_title='Precipitation (mm/h)',
        yaxis2=dict(
            title='Probability (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(precip_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Radar Legend
    st.markdown("## 📊 Radar Intensity Legend")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(144, 238, 144, 0.5); padding: 1rem; border-radius: 8px; text-align: center;">
            <p style="margin: 0; font-weight: 700;">Light</p>
            <p style="margin: 0; font-size: 0.9rem;">0-2 mm/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(135, 206, 250, 0.7); padding: 1rem; border-radius: 8px; text-align: center;">
            <p style="margin: 0; font-weight: 700;">Moderate</p>
            <p style="margin: 0; font-size: 0.9rem;">2-5 mm/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(65, 105, 225, 0.8); padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <p style="margin: 0; font-weight: 700;">Heavy</p>
            <p style="margin: 0; font-size: 0.9rem;">5-10 mm/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: rgba(255, 165, 0, 0.9); padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <p style="margin: 0; font-weight: 700;">Very Heavy</p>
            <p style="margin: 0; font-size: 0.9rem;">10-20 mm/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="background: rgba(139, 0, 0, 1); padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <p style="margin: 0; font-weight: 700;">Extreme</p>
            <p style="margin: 0; font-size: 0.9rem;">>20 mm/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌤️ Current Weather", use_container_width=True):
            st.switch_page("pages/02_🌤️_Current_Weather.py")
    
    with col2:
        if st.button("⏰ Hourly Forecast", use_container_width=True):
            st.switch_page("pages/04_⏰_Hourly_Forecast.py")
    
    with col3:
        if st.button("🗺️ Change Location", use_container_width=True):
            st.switch_page("pages/01_🗺️_Interactive_Map.py")

else:
    st.error("❌ Unable to fetch radar data. Please try again.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
