"""
Weather Statistics & Correlations
Advanced statistical analysis of weather patterns
"""
import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy import stats

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_historical_weather

# Page configuration
st.set_page_config(
    page_title="Weather Statistics",
    page_icon="📈",
    layout="wide"
)

# Header
st.title("📈 Weather Statistics & Correlations")
st.markdown("**Advanced statistical analysis and pattern recognition**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Sidebar - Analysis period
st.sidebar.markdown("### 📅 Analysis Period")
days_back = st.sidebar.slider("Days of Historical Data", 30, 365, 90)

end_date = datetime.now() - timedelta(days=1)
start_date = end_date - timedelta(days=days_back)

# Fetch data
with st.spinner(f"Analyzing {days_back} days of weather data..."):
    weather_df = get_historical_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

if weather_df is not None and len(weather_df) > 0:
    # Process data
    weather_df['date'] = pd.to_datetime(weather_df['time'])
    
    # Statistical Summary
    st.markdown("## 📊 Statistical Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌡️ Temperature")
        temp_mean = weather_df['temperature_2m_mean'].mean()
        temp_std = weather_df['temperature_2m_mean'].std()
        temp_median = weather_df['temperature_2m_mean'].median()
        
        st.metric("Mean", f"{temp_mean:.1f}°C")
        st.metric("Std Dev", f"{temp_std:.2f}°C")
        st.metric("Median", f"{temp_median:.1f}°C")
    
    with col2:
        st.markdown("### 💧 Precipitation")
        precip_total = weather_df['precipitation_sum'].sum()
        precip_mean = weather_df['precipitation_sum'].mean()
        precip_max = weather_df['precipitation_sum'].max()
        
        st.metric("Total", f"{precip_total:.1f} mm")
        st.metric("Daily Avg", f"{precip_mean:.2f} mm")
        st.metric("Max Daily", f"{precip_max:.1f} mm")
    
    with col3:
        st.markdown("### 🌬️ Wind Speed")
        wind_mean = weather_df['wind_speed_10m_max'].mean()
        wind_std = weather_df['wind_speed_10m_max'].std()
        wind_max = weather_df['wind_speed_10m_max'].max()
        
        st.metric("Mean", f"{wind_mean:.1f} km/h")
        st.metric("Std Dev", f"{wind_std:.2f} km/h")
        st.metric("Max", f"{wind_max:.1f} km/h")
    
    st.markdown("---")
    
    # Correlation Analysis
    st.markdown("## 🔗 Correlation Analysis")
    
    # Calculate correlations
    corr_data = weather_df[['temperature_2m_mean', 'precipitation_sum', 'wind_speed_10m_max']].corr()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Correlation heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_data.values,
            x=['Temperature', 'Precipitation', 'Wind Speed'],
            y=['Temperature', 'Precipitation', 'Wind Speed'],
            colorscale='RdBu',
            zmid=0,
            text=corr_data.values.round(3),
            texttemplate='%{text}',
            textfont={"size": 14},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Weather Variables Correlation Matrix',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Scatter plot: Temperature vs Precipitation
        scatter_fig = go.Figure()
        
        scatter_fig.add_trace(go.Scatter(
            x=weather_df['temperature_2m_mean'],
            y=weather_df['precipitation_sum'],
            mode='markers',
            marker=dict(
                size=8,
                color=weather_df['wind_speed_10m_max'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Wind Speed<br>(km/h)")
            ),
            text=weather_df['date'].dt.strftime('%Y-%m-%d'),
            hovertemplate='<b>%{text}</b><br>Temp: %{x:.1f}°C<br>Precip: %{y:.1f}mm<extra></extra>'
        ))
        
        scatter_fig.update_layout(
            title='Temperature vs Precipitation',
            xaxis_title='Temperature (°C)',
            yaxis_title='Precipitation (mm)',
            height=400
        )
        
        st.plotly_chart(scatter_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Time Series Decomposition
    st.markdown("## 📉 Temperature Trend Analysis")
    
    # Calculate moving averages
    weather_df['temp_ma7'] = weather_df['temperature_2m_mean'].rolling(window=7, center=True).mean()
    weather_df['temp_ma30'] = weather_df['temperature_2m_mean'].rolling(window=30, center=True).mean()
    
    # Create trend chart
    trend_fig = go.Figure()
    
    trend_fig.add_trace(go.Scatter(
        x=weather_df['date'],
        y=weather_df['temperature_2m_mean'],
        name='Daily Temperature',
        line=dict(color='lightgray', width=1),
        opacity=0.5
    ))
    
    trend_fig.add_trace(go.Scatter(
        x=weather_df['date'],
        y=weather_df['temp_ma7'],
        name='7-Day Moving Average',
        line=dict(color='#4299e1', width=2)
    ))
    
    trend_fig.add_trace(go.Scatter(
        x=weather_df['date'],
        y=weather_df['temp_ma30'],
        name='30-Day Moving Average',
        line=dict(color='#e53e3e', width=2)
    ))
    
    trend_fig.update_layout(
        title='Temperature Trends with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(trend_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Distribution Analysis
    st.markdown("## 📊 Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature distribution
        temp_hist = go.Figure()
        
        temp_hist.add_trace(go.Histogram(
            x=weather_df['temperature_2m_mean'],
            nbinsx=30,
            name='Temperature',
            marker_color='#4299e1',
            opacity=0.7
        ))
        
        # Add normal distribution overlay
        mu = weather_df['temperature_2m_mean'].mean()
        sigma = weather_df['temperature_2m_mean'].std()
        x_range = np.linspace(weather_df['temperature_2m_mean'].min(), 
                             weather_df['temperature_2m_mean'].max(), 100)
        y_normal = stats.norm.pdf(x_range, mu, sigma) * len(weather_df) * \
                   (weather_df['temperature_2m_mean'].max() - weather_df['temperature_2m_mean'].min()) / 30
        
        temp_hist.add_trace(go.Scatter(
            x=x_range,
            y=y_normal,
            name='Normal Distribution',
            line=dict(color='red', width=2)
        ))
        
        temp_hist.update_layout(
            title='Temperature Distribution',
            xaxis_title='Temperature (°C)',
            yaxis_title='Frequency',
            height=350
        )
        
        st.plotly_chart(temp_hist, use_container_width=True)
    
    with col2:
        # Precipitation distribution (log scale)
        precip_data = weather_df[weather_df['precipitation_sum'] > 0]['precipitation_sum']
        
        precip_hist = go.Figure()
        
        precip_hist.add_trace(go.Histogram(
            x=precip_data,
            nbinsx=30,
            name='Precipitation',
            marker_color='#48bb78',
            opacity=0.7
        ))
        
        precip_hist.update_layout(
            title='Precipitation Distribution (Rainy Days Only)',
            xaxis_title='Precipitation (mm)',
            yaxis_title='Frequency',
            height=350
        )
        
        st.plotly_chart(precip_hist, use_container_width=True)
    
    st.markdown("---")
    
    # Percentile Analysis
    st.markdown("## 📏 Percentile Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Temperature Percentiles")
        percentiles = [10, 25, 50, 75, 90, 95, 99]
        temp_percentiles = np.percentile(weather_df['temperature_2m_mean'], percentiles)
        
        for p, val in zip(percentiles, temp_percentiles):
            st.markdown(f"**{p}th percentile:** {val:.1f}°C")
    
    with col2:
        st.markdown("### Precipitation Percentiles")
        precip_percentiles = np.percentile(weather_df['precipitation_sum'], percentiles)
        
        for p, val in zip(percentiles, precip_percentiles):
            st.markdown(f"**{p}th percentile:** {val:.1f} mm")
    
    with col3:
        st.markdown("### Wind Speed Percentiles")
        wind_percentiles = np.percentile(weather_df['wind_speed_10m_max'], percentiles)
        
        for p, val in zip(percentiles, wind_percentiles):
            st.markdown(f"**{p}th percentile:** {val:.1f} km/h")
    
    st.markdown("---")
    
    # Extreme Events
    st.markdown("## ⚡ Extreme Weather Events")
    
    # Define thresholds
    temp_high_threshold = np.percentile(weather_df['temperature_2m_max'], 95)
    temp_low_threshold = np.percentile(weather_df['temperature_2m_min'], 5)
    precip_threshold = np.percentile(weather_df['precipitation_sum'], 95)
    wind_threshold = np.percentile(weather_df['wind_speed_10m_max'], 95)
    
    # Find extreme events
    hot_days = weather_df[weather_df['temperature_2m_max'] > temp_high_threshold]
    cold_days = weather_df[weather_df['temperature_2m_min'] < temp_low_threshold]
    heavy_rain = weather_df[weather_df['precipitation_sum'] > precip_threshold]
    windy_days = weather_df[weather_df['wind_speed_10m_max'] > wind_threshold]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔥 Hot Days",
            len(hot_days),
            delta=f">{temp_high_threshold:.1f}°C"
        )
    
    with col2:
        st.metric(
            "❄️ Cold Days",
            len(cold_days),
            delta=f"<{temp_low_threshold:.1f}°C"
        )
    
    with col3:
        st.metric(
            "🌧️ Heavy Rain Days",
            len(heavy_rain),
            delta=f">{precip_threshold:.1f}mm"
        )
    
    with col4:
        st.metric(
            "💨 Windy Days",
            len(windy_days),
            delta=f">{wind_threshold:.1f}km/h"
        )
    
    st.markdown("---")
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Historical Analysis", use_container_width=True):
            st.switch_page("pages/05_📊_Historical_Analysis.py")
    
    with col2:
        if st.button("🌧️ Annual Rainfall", use_container_width=True):
            st.switch_page("pages/08_🌧️_Annual_Rainfall.py")
    
    with col3:
        if st.button("🗺️ Change Location", use_container_width=True):
            st.switch_page("pages/01_🗺️_Interactive_Map.py")

else:
    st.error("❌ Unable to fetch weather data. Please try again.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
