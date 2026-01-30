<div align="center">

# 🌤️ Weather Prediction Portfolio

### *Advanced Weather Analytics & Forecasting Platform*

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Open-Meteo](https://img.shields.io/badge/Open--Meteo-00A8E8?style=for-the-badge&logo=weather&logoColor=white)](https://open-meteo.com/)

**A comprehensive, data-driven weather analysis platform featuring real-time forecasts, historical trends, and advanced statistical analytics.**

[🚀 Live Demo](#) • [📖 Documentation](#features) • [🤝 Contributing](#contributing)

---

</div>

## ✨ Features

### 🗺️ **Interactive Weather Map**
- **Folium-powered** interactive map with global coverage
- Click anywhere to get instant weather data
- City search with geocoding API
- Popular cities quick selection
- Real-time location-based weather updates

### 🌤️ **Current Weather Dashboard**
- **Comprehensive metrics**: Temperature, humidity, wind, pressure, cloud cover
- **Advanced atmospheric data**:
  - Dew point calculation (Magnus formula)
  - Barometric altimeter with altitude estimation
  - Atmospheric stability analysis
  - Comfort index and air quality indicators
- **Astronomical data**:
  - Sunrise & sunset times
  - Sunshine duration with coverage percentage
  - Moon phase tracking (8 phases)
  - Local time display with timezone

### 📅 **7-Day Forecast**
- Daily weather cards with emoji indicators
- Temperature trends (max, min, mean)
- Precipitation probability charts
- UV index and wind speed forecasts
- Downloadable CSV reports

### ⏰ **Hourly Forecast**
- Up to 48-hour detailed forecasts
- Interactive Plotly charts:
  - Temperature & "Feels Like" comparison
  - Precipitation probability & humidity (dual-axis)
  - Wind speed & gusts analysis
- Hourly data table with 3-hour sampling

### 📊 **Historical Analysis**
- Customizable date ranges (7, 14, 30 days, or custom)
- Statistical summaries (avg, max, min temperatures)
- Multi-line temperature trends
- Precipitation analysis with rainy days statistics
- Temperature distribution (histogram & box plot)
- Wind speed trend analysis
- CSV export functionality

### 🌍 **Multi-City Comparison**
- Compare up to 5 cities simultaneously
- Current weather comparison cards
- Temperature bar chart comparison
- Radar chart for multiple metrics
- 7-day forecast trends comparison
- Weather rankings (warmest/coolest)
- Exportable comparison data

### ⚠️ **Weather Alerts & Warnings**
- Customizable alert thresholds
- Real-time monitoring for:
  - High/low temperature warnings
  - High wind speed alerts
  - Heavy precipitation alerts
  - High humidity warnings
- Severity-based categorization (High/Medium)
- Weather safety tips
- Alert statistics dashboard

### 🌧️ **Annual Rainfall Analysis**
- Yearly precipitation statistics
- Monthly distribution charts
- Daily rainfall patterns
- Rainfall intensity categorization:
  - Light (0-5mm)
  - Moderate (5-20mm)
  - Heavy (20-50mm)
  - Very Heavy (>50mm)
- Wettest/driest month identification
- Downloadable monthly statistics

### 📈 **Weather Statistics & Correlations**
- **Statistical analysis**:
  - Mean, standard deviation, median
  - Correlation matrix heatmap
  - Scatter plots with color coding
- **Trend analysis**:
  - 7-day & 30-day moving averages
  - Time series decomposition
- **Distribution analysis**:
  - Temperature histogram with normal distribution overlay
  - Precipitation distribution (rainy days)
- **Percentile analysis**: 10th to 99th percentiles
- **Extreme events detection**: Hot/cold days, heavy rain, windy days

### 📡 **Weather Radar Visualization**
- Simulated precipitation radar map
- Real-time precipitation intensity indicators
- 24-hour precipitation forecast timeline
- Intensity legend (Light to Extreme)
- Geographic heatmap visualization
- Color-coded status indicators

---

## 🛠️ Technology Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Framework** | Streamlit 1.28+ |
| **Mapping** | Folium 0.14+, Streamlit-Folium 0.15+ |
| **Visualization** | Plotly 5.17+, Altair 5.0+ |
| **Data Processing** | Pandas 2.0+, NumPy 1.24+ |
| **Statistical Analysis** | SciPy 1.11+ |
| **API** | Open-Meteo API (Free, No API Key Required) |
| **HTTP Requests** | Requests 2.31+ |

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yandri918/prediksi-cuaca.git
   cd prediksi-cuaca
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   ```
   The app will automatically open at http://localhost:8501
   ```

---

## 📁 Project Structure

```
prediksi-cuaca/
├── app.py                              # Main landing page
├── pages/
│   ├── 01_🗺️_Interactive_Map.py       # Interactive weather map
│   ├── 02_🌤️_Current_Weather.py       # Current weather dashboard
│   ├── 03_📅_7-Day_Forecast.py        # 7-day forecast
│   ├── 04_⏰_Hourly_Forecast.py        # Hourly forecast (48h)
│   ├── 05_📊_Historical_Analysis.py   # Historical weather data
│   ├── 06_🌍_Multi-City_Comparison.py # Multi-city comparison
│   ├── 07_⚠️_Weather_Alerts.py        # Weather alerts & warnings
│   ├── 08_🌧️_Annual_Rainfall.py       # Annual rainfall analysis
│   ├── 09_📈_Weather_Statistics.py    # Statistical analysis
│   └── 10_📡_Weather_Radar.py         # Weather radar visualization
├── utils/
│   ├── weather_api.py                  # Weather API integration
│   ├── map_utils.py                    # Folium map utilities
│   └── moon_phase.py                   # Moon phase calculations
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## 📊 Data Source

This application uses the **[Open-Meteo API](https://open-meteo.com/)**, a free weather API that provides:

- ✅ **No API key required**
- ✅ **High-quality data** from national weather services
- ✅ **Global coverage** with 11km resolution
- ✅ **Real-time updates** every 15 minutes
- ✅ **Historical data** dating back to 1940
- ✅ **Free for non-commercial use**

### API Endpoints Used:
- **Forecast API**: Current weather & forecasts
- **Geocoding API**: City search & coordinates
- **Historical API**: Past weather data

---

## 🎨 Key Features Highlights

### 🔬 Advanced Analytics
- **Correlation Analysis**: Understand relationships between weather variables
- **Trend Decomposition**: 7-day and 30-day moving averages
- **Statistical Distributions**: Normal distribution overlays
- **Extreme Events**: Automated detection of unusual weather

### 🌐 Interactive Visualizations
- **Plotly Charts**: Fully interactive with zoom, pan, hover
- **Altair Charts**: Statistical visualizations with tooltips
- **Folium Maps**: Click-to-select locations worldwide
- **Radar Maps**: Simulated precipitation intensity

### 📱 User Experience
- **Responsive Design**: Works on desktop and mobile
- **Session State**: Maintains location across pages
- **Quick Navigation**: Easy switching between features
- **Data Export**: Download CSV reports for analysis

---

## 🧮 Scientific Calculations

### Dew Point (Magnus Formula)
```python
α = (17.27 × T) / (237.7 + T) + ln(RH/100)
Td = (237.7 × α) / (17.27 - α)
```

### Barometric Altitude
```python
h = (288.15 / 0.0065) × (1 - (P / P₀)^(1/5.255))
```

### Moon Phase
```python
phase = (days_since_new_moon % 29.53) / 29.53
```

---

## 📸 Screenshots

*Coming soon: Add screenshots of your deployed application*

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Yandri**

- GitHub: [@yandri918](https://github.com/yandri918)
- Repository: [prediksi-cuaca](https://github.com/yandri918/prediksi-cuaca)

---

## 🙏 Acknowledgments

- **[Open-Meteo](https://open-meteo.com/)** - Free weather API
- **[Streamlit](https://streamlit.io/)** - Amazing Python web framework
- **[Plotly](https://plotly.com/)** - Interactive visualization library
- **[Folium](https://python-visualization.github.io/folium/)** - Leaflet.js integration for Python

---

## 📈 Project Stats

- **10 Interactive Pages** with comprehensive features
- **50+ Weather Metrics** tracked and analyzed
- **Multiple Visualization Types** (charts, maps, radar)
- **Statistical Analysis** with correlation and trends
- **Real-time Data** updated every 15 minutes
- **Historical Data** access up to 80+ years

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ and ☕ by Yandri**

</div>
