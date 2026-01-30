"""
Weather Prediction Portfolio
Professional weather forecasting application using Open-Meteo API and Folium maps
"""
import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(__file__))

# Page configuration
st.set_page_config(
    page_title="Weather Prediction Portfolio",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    
    .weather-icon {
        font-size: 4rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌤️ Weather Prediction Portfolio</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        Professional Weather Forecasting with Interactive Maps & Real-time Data
    </p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("## 👋 Welcome!")
st.markdown("""
This portfolio showcases advanced weather prediction capabilities using:
- **Open-Meteo API** for accurate, real-time weather data
- **Folium Maps** for interactive location selection
- **Advanced Visualizations** with Altair and Plotly
- **Comprehensive Forecasts** from hourly to weekly predictions
""")

st.markdown("---")

# Features Overview
st.markdown("## 🎯 Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🗺️ Interactive Maps</h3>
        <p>Click anywhere on the map to get instant weather data. Search cities or select from popular locations.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🌤️ Real-time Weather</h3>
        <p>Current conditions including temperature, humidity, wind, pressure, and more.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📅 Forecasts</h3>
        <p>7-day daily forecasts and 48-hour hourly predictions with detailed metrics.</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Analysis</h3>
        <p>Historical weather data analysis with trends and patterns visualization.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🌍 Multi-City</h3>
        <p>Compare weather across multiple cities simultaneously.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📈 Visualizations</h3>
        <p>Beautiful charts and graphs for temperature, precipitation, and wind data.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Stats
st.markdown("## 📊 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700;">100%</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Free API</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700;">16 Days</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Forecast Range</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700;">Global</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Coverage</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700;">Real-time</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Updates</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# How to Use
st.markdown("## 🚀 How to Use")

st.markdown("""
1. **Navigate** to any page using the sidebar
2. **Select Location** on the Interactive Map page
3. **View Weather** data and forecasts
4. **Analyze** historical trends
5. **Compare** multiple cities

👈 **Start by selecting a page from the sidebar!**
""")

st.markdown("---")

# Technology Stack
st.markdown("## 🛠️ Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Data & APIs:**
    - Open-Meteo API (Weather Data)
    - Geocoding API (Location Search)
    - Pandas (Data Processing)
    """)

with col2:
    st.markdown("""
    **Visualization:**
    - Folium (Interactive Maps)
    - Altair (Statistical Charts)
    - Plotly (Interactive Graphs)
    - Streamlit (Web Framework)
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>Built with ❤️ using Streamlit, Folium, and Open-Meteo API</p>
    <p>© 2024 Weather Prediction Portfolio</p>
</div>
""", unsafe_allow_html=True)
