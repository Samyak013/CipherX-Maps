# SmartTransportAI

## Urban Public Transport Route Optimization System for Indian Cities

SmartTransportAI is a data-driven public transport route optimization system designed specifically for Indian cities. The application uses real-time data, predictive analytics, and reinforcement learning to optimize public transport routes, improving commuter experience and reducing congestion.

![SmartTransportAI Interface](generated-icon.png)

## Features

- **Intelligent Route Planning**: Find the optimal routes between any two locations in supported Indian cities using various transport modes.
- **Real-time Data Integration**: Incorporates live traffic, GPS location data, and weather impacts to provide up-to-date recommendations.
- **Multi-city Support**: Currently supports major Indian cities including Mumbai, Delhi, Bangalore, Chennai, Hyderabad, and more.
- **Comprehensive Transport Options**: Integrates buses, trains, metro, walking, and cycling routes.
- **Demand Forecasting**: Predicts passenger demand patterns to optimize service frequency.
- **Congestion Analysis**: Identifies traffic hotspots and provides congestion mitigation strategies.
- **Interactive Visualizations**: User-friendly dashboards and maps for easy data interpretation.

## Installation

### Prerequisites

- Python 3.11 or higher
- Visual Studio Code with recommended extensions (see [VS Code Setup Guide](vs_code_setup.md))

### Setting Up the Development Environment

1. Clone the repository:
   ```
   git clone <repository-url>
   cd SmartTransportAI
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in required API keys

## Running the Application

```
streamlit run app.py --server.port 5000
```

Or use the VS Code Run Configuration "Streamlit: Run App".

## Directory Structure

```
SmartTransportAI/
├── .streamlit/            # Streamlit configuration
├── .vscode/               # VS Code settings
├── api/                   # External API integrations
├── backend/               # API endpoints and server logic
├── config/                # Configuration files
├── data/                  # Data storage and processing
├── frontend/              # Frontend components
├── logs/                  # Application logs
├── models/                # ML models for optimization
├── tests/                 # Test cases
├── utils/                 # Utility functions
├── app.py                 # Main Streamlit application
├── .env.example           # Example environment variables
└── README.md              # This file
```

## Technology Stack

- **Frontend**: Streamlit, Plotly, PyDeck
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, TensorFlow (optional)
- **Optimization**: NetworkX, Reinforcement Learning (Gym)
- **Visualization**: Matplotlib, Seaborn, Plotly

## Data Sources

- GTFS feeds for public transport timetables
- Traffic data from Google Maps API
- Weather data from OpenWeatherMap API
- Census and demographic data for demand modeling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Indian Transit Authorities for public transport data
- OpenStreetMap contributors for map data
- Academic research on transport optimization algorithms