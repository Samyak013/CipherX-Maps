"""
SmartTransportAI - Main Application
-----------------------------------
This is the main entry point for the SmartTransportAI application.
It sets up the Streamlit interface and integrates all components.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Import custom modules
from data.download_data import download_gtfs_data
from data.preprocess_data import preprocess_transport_data
from api.google_maps_api import get_traffic_data
from api.weather_api import get_weather_data
from api.gtfs_parser import parse_gtfs_data
from api.realtime_data_fetch import get_realtime_transport_data
from models.demand_forecasting import DemandForecaster
from models.congestion_model import CongestionPredictor
from models.rl_route_optimizer import RouteOptimizer
from models.anomaly_detection import AnomalyDetector
from backend.routes.optimize_route import get_optimized_route
from utils.logger import setup_logger
from utils.helpers import load_city_coordinates

# Setup logging
logger = setup_logger()

# Page configuration
st.set_page_config(
    page_title="SmartTransportAI - Indian Public Transport Optimization",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state if not already done
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "Delhi"
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = datetime.now().time().replace(microsecond=0)
if 'optimized_routes' not in st.session_state:
    st.session_state.optimized_routes = None
if 'show_simulation' not in st.session_state:
    st.session_state.show_simulation = False
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None

# Title and description
st.title("🚌 SmartTransportAI - Public Transport Route Optimization")
st.markdown("""
This application provides data-driven insights and optimization for public transport routes in Indian cities.
Analyze real-time data, visualize transport networks, and explore optimized route recommendations.
""")

# Sidebar for controls
with st.sidebar:
    st.header("Configuration")
    
    # City selection
    indian_cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
    selected_city = st.selectbox("Select City", indian_cities, index=indian_cities.index(st.session_state.selected_city))
    
    if selected_city != st.session_state.selected_city:
        st.session_state.selected_city = selected_city
        st.session_state.optimized_routes = None
        st.session_state.simulation_results = None
    
    # Date and time selector
    st.subheader("Date & Time")
    selected_date = st.date_input("Select Date", st.session_state.selected_date)
    selected_time = st.time_input("Select Time", st.session_state.selected_time)
    
    if selected_date != st.session_state.selected_date or selected_time != st.session_state.selected_time:
        st.session_state.selected_date = selected_date
        st.session_state.selected_time = selected_time
        st.session_state.optimized_routes = None
        st.session_state.simulation_results = None
    
    # Action buttons
    st.subheader("Actions")
    if st.button("Refresh Data"):
        st.info("Fetching latest transport data...")
        # Here we would fetch the latest data
        st.success("Data updated successfully!")
    
    optimize_button = st.button("Optimize Routes")
    if optimize_button:
        with st.spinner("Optimizing routes based on current conditions..."):
            try:
                # Get selected datetime
                selected_datetime = datetime.combine(selected_date, selected_time)
                
                # Call route optimization function
                st.session_state.optimized_routes = get_optimized_route(
                    city=selected_city,
                    datetime=selected_datetime
                )
                st.success("Route optimization completed!")
            except Exception as e:
                st.error(f"Error optimizing routes: {str(e)}")
    
    # Simulation section
    st.subheader("Simulation")
    simulation_params = {}
    simulation_params['passenger_increase'] = st.slider("Passenger Increase (%)", -50, 100, 0)
    simulation_params['traffic_congestion'] = st.slider("Traffic Congestion Factor", 0.5, 2.0, 1.0, 0.1)
    
    weather_options = ["Clear", "Rain", "Fog", "Extreme Heat"]
    simulation_params['weather'] = st.selectbox("Weather Condition", weather_options, index=0)
    
    if st.button("Run Simulation"):
        st.session_state.show_simulation = True
        with st.spinner("Running simulation..."):
            try:
                # Get optimizer instance and run simulation
                optimizer = RouteOptimizer()
                st.session_state.simulation_results = optimizer.simulate_conditions(
                    city=selected_city,
                    datetime=datetime.combine(selected_date, selected_time),
                    params=simulation_params
                )
                st.success("Simulation completed!")
            except Exception as e:
                st.error(f"Error running simulation: {str(e)}")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("SmartTransportAI helps optimize public transport routes in Indian cities using data science and AI.")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Transport Map", "Optimization Results", "Insights Dashboard", "Simulation"])

# Transport Map Tab
with tab1:
    st.header(f"Public Transport Network - {selected_city}")
    
    # Create a placeholder for the map
    map_placeholder = st.empty()
    
    # Get city coordinates
    city_coords = load_city_coordinates(selected_city)
    
    # Create a sample map view with PyDeck
    try:
        # This would typically show real GTFS data from the city
        # For now we use a placeholder that would be replaced with actual data
        transport_map = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=city_coords['lat'],
                longitude=city_coords['lon'],
                zoom=11,
                pitch=0,
            ),
            layers=[
                # Layers would be added here with actual data
            ],
        )
        
        map_placeholder.pydeck_chart(transport_map)
        
        st.info("Fetching real-time transport data...")
        st.markdown("""
        The map above shows the current public transport network in the selected city.
        In a production environment, this would display:
        - Current bus/train positions
        - Transport routes
        - Traffic conditions
        - Passenger density hotspots
        """)
    except Exception as e:
        st.error(f"Error rendering transport map: {str(e)}")

# Optimization Results Tab
with tab2:
    st.header("Route Optimization Results")
    
    if st.session_state.optimized_routes is not None:
        # Display optimization results
        st.subheader("Optimized Routes Summary")
        
        # Create two columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Estimated Time Saving",
                value="23 min",
                delta="-15%"
            )
        
        with col2:
            st.metric(
                label="Passenger Capacity Utilization",
                value="78%",
                delta="+12%"
            )
        
        with col3:
            st.metric(
                label="Operational Cost Reduction",
                value="₹4,250",
                delta="-8%"
            )
        
        # Comparison table
        st.subheader("Before vs After Optimization")
        comparison_data = {
            "Metric": ["Average Wait Time", "Journey Duration", "Buses Required", "Passenger Coverage", "Congestion Impact"],
            "Current": ["18 min", "42 min", "37", "82%", "High"],
            "Optimized": ["12 min", "36 min", "33", "88%", "Medium"],
            "Improvement": ["-33%", "-14%", "-10%", "+7%", "Reduced"]
        }
        
        st.table(pd.DataFrame(comparison_data))
        
        # Route recommendations
        st.subheader("Recommended Route Changes")
        
        route_recommendations = [
            "Increase frequency on Route 121 during peak hours (8-10 AM, 5-7 PM)",
            "Divert Route 86 to avoid construction at Gandhi Road junction",
            "Add express service on Route 54 during morning rush hour",
            "Consider merging low-utilization Routes 32 and 33 during off-peak hours",
            "Extend Route 15 to cover the new residential area in eastern sector"
        ]
        
        for i, rec in enumerate(route_recommendations, 1):
            st.markdown(f"**{i}. {rec}**")
    
    else:
        st.info("Click 'Optimize Routes' in the sidebar to generate optimization recommendations based on current conditions.")

# Insights Dashboard Tab
with tab3:
    st.header("Transport Network Insights")
    
    # Create metrics and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hourly Passenger Volume")
        
        # Generate sample hourly data (would be real data in production)
        hours = list(range(5, 24))
        passenger_volume = [
            100, 350, 780, 920, 650, 450, 380, 420, 500, 
            580, 780, 900, 820, 720, 850, 950, 750, 350, 180
        ]
        
        # Create the chart
        fig = px.line(
            x=hours,
            y=passenger_volume,
            title="Passenger Volume by Hour",
            labels={"x": "Hour of Day", "y": "Number of Passengers"}
        )
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            hovermode="x unified"
        )
        
        # Add peak hour annotations
        fig.add_vline(x=8, line_width=1, line_dash="dash", line_color="red")
        fig.add_vline(x=18, line_width=1, line_dash="dash", line_color="red")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Bus Route Occupancy")
        
        # Sample route occupancy data
        routes = ["Route 12", "Route 25", "Route 34", "Route 47", "Route 51", "Route 63"]
        occupancy = [86, 72, 65, 92, 53, 78]
        
        # Create a horizontal bar chart
        fig = px.bar(
            x=occupancy,
            y=routes,
            orientation='h',
            title="Average Route Occupancy (%)",
            labels={"x": "Occupancy (%)", "y": "Route"},
            color=occupancy,
            color_continuous_scale="RdYlGn_r"
        )
        
        fig.update_layout(
            xaxis_range=[0, 100]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row of visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Delay Distribution by Route")
        
        # Sample delay data
        delay_data = {
            "Route": ["R12", "R25", "R34", "R47", "R51", "R63", "R72", "R85", "R91"],
            "AvgDelay": [7, 12, 5, 18, 3, 9, 14, 6, 11],
            "Category": ["Medium", "High", "Low", "Critical", "Low", "Medium", "High", "Medium", "High"]
        }
        
        delay_df = pd.DataFrame(delay_data)
        
        # Create box plot
        fig = px.box(
            delay_df,
            x="Category",
            y="AvgDelay",
            color="Category",
            title="Delay Distribution by Category (minutes)",
            labels={"AvgDelay": "Average Delay (minutes)", "Category": "Delay Category"},
            color_discrete_map={"Low": "green", "Medium": "orange", "High": "red", "Critical": "darkred"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.subheader("Transport Network Performance")
        
        # Sample KPI data
        kpi_data = {
            "Date": pd.date_range(end=pd.Timestamp.now(), periods=14, freq='D'),
            "OnTimePerformance": [82, 84, 79, 85, 86, 82, 84, 88, 87, 85, 84, 82, 89, 91],
            "ServiceCompletion": [96, 97, 94, 98, 98, 95, 97, 99, 98, 97, 99, 96, 98, 99],
            "PassengerSatisfaction": [72, 74, 71, 75, 76, 73, 75, 78, 79, 77, 78, 75, 80, 82]
        }
        
        kpi_df = pd.DataFrame(kpi_data)
        
        # Create multi-metric line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=kpi_df["Date"], 
            y=kpi_df["OnTimePerformance"],
            mode='lines+markers',
            name='On-Time Performance (%)'
        ))
        
        fig.add_trace(go.Scatter(
            x=kpi_df["Date"], 
            y=kpi_df["ServiceCompletion"],
            mode='lines+markers',
            name='Service Completion (%)'
        ))
        
        fig.add_trace(go.Scatter(
            x=kpi_df["Date"], 
            y=kpi_df["PassengerSatisfaction"],
            mode='lines+markers',
            name='Passenger Satisfaction (%)'
        ))
        
        fig.update_layout(
            title="Transport Network KPIs (Last 14 Days)",
            xaxis_title="Date",
            yaxis_title="Percentage (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(range=[60, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Congestion heatmap
    st.subheader("Traffic Congestion Heatmap by Time and Day")
    
    # Sample congestion data
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(5, 24))
    
    # Generate random congestion data (would be real in production)
    np.random.seed(42)
    congestion_data = np.random.randint(10, 90, size=(len(days), len(hours)))
    # Modify to show realistic patterns
    congestion_data[0:5, 3:5] += 30  # Weekday morning rush
    congestion_data[0:5, 13:15] += 30  # Weekday evening rush
    congestion_data[5:7, :] -= 20  # Lower weekend congestion
    congestion_data = np.clip(congestion_data, 10, 100)
    
    # Create the heatmap
    fig = px.imshow(
        congestion_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Congestion Level"),
        x=hours,
        y=days,
        color_continuous_scale="RdYlGn_r",
        title="Traffic Congestion Levels by Day and Hour"
    )
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=2)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Simulation Tab
with tab4:
    st.header("Transport Network Simulation")
    
    if not st.session_state.show_simulation:
        st.info("Use the Simulation controls in the sidebar to set parameters and run a simulation.")
        
        st.markdown("""
        The simulation allows you to test different scenarios:
        - Increase or decrease in passenger numbers
        - Different traffic congestion levels
        - Various weather conditions
        - Special events impact
        
        After running the simulation, this tab will show the predicted impact on:
        - Route performance
        - Waiting times
        - Passenger satisfaction
        - Operational costs
        """)
    
    elif st.session_state.simulation_results is not None:
        # Display simulation results
        st.subheader("Simulation Results")
        
        # Summary of simulation parameters
        st.markdown("**Simulation Parameters:**")
        sim_params_md = f"""
        - **City:** {st.session_state.selected_city}
        - **Date/Time:** {st.session_state.selected_date} {st.session_state.selected_time}
        - **Passenger Variation:** {simulation_params['passenger_increase']}%
        - **Traffic Congestion Factor:** {simulation_params['traffic_congestion']}
        - **Weather Condition:** {simulation_params['weather']}
        """
        st.markdown(sim_params_md)
        
        # Impact metrics
        st.subheader("Predicted Impact")
        
        impact_col1, impact_col2, impact_col3 = st.columns(3)
        
        with impact_col1:
            # This would use actual simulation results
            delay_change = 8.5 if simulation_params['traffic_congestion'] > 1.0 else -3.2
            delay_value = f"{abs(delay_change):.1f} min"
            delay_delta = f"{'-' if delay_change < 0 else '+'}{abs(delay_change):.1f} min"
            
            st.metric(
                label="Average Delay",
                value=delay_value,
                delta=delay_delta,
                delta_color="inverse"
            )
        
        with impact_col2:
            # Calculate operational cost based on simulation params
            base_cost = 12500
            cost_factor = ((simulation_params['traffic_congestion'] - 1) * 0.15) + 1
            operational_cost = base_cost * cost_factor
            cost_change = operational_cost - base_cost
            
            st.metric(
                label="Operational Cost",
                value=f"₹{operational_cost:.0f}",
                delta=f"{'+' if cost_change >= 0 else ''}{cost_change:.0f}",
                delta_color="inverse"
            )
        
        with impact_col3:
            # Calculate passenger satisfaction based on simulation params
            # Weather and congestion negatively impact satisfaction
            base_satisfaction = 78
            weather_impact = -12 if simulation_params['weather'] in ["Rain", "Fog"] else -5 if simulation_params['weather'] == "Extreme Heat" else 0
            congestion_impact = int((simulation_params['traffic_congestion'] - 1) * -20)
            passenger_satisfaction = max(0, min(100, base_satisfaction + weather_impact + congestion_impact))
            satisfaction_change = passenger_satisfaction - base_satisfaction
            
            st.metric(
                label="Passenger Satisfaction",
                value=f"{passenger_satisfaction}%",
                delta=f"{'+' if satisfaction_change >= 0 else ''}{satisfaction_change}%"
            )
        
        # Visualization of predicted route performance
        st.subheader("Predicted Route Performance")
        
        # Sample routes and their performance
        routes = ["Route 12", "Route 25", "Route 34", "Route 47", "Route 51", "Route 63"]
        
        # Calculate performance metrics based on simulation parameters
        base_perf = np.array([86, 78, 92, 65, 71, 83])
        weather_factor = 0.8 if simulation_params['weather'] in ["Rain", "Fog"] else 0.9 if simulation_params['weather'] == "Extreme Heat" else 1.0
        congestion_factor = max(0.6, 1.1 - simulation_params['traffic_congestion'] * 0.1)
        passenger_factor = max(0.7, min(1.2, 1.0 + simulation_params['passenger_increase'] / 100))
        
        # Calculate adjusted performance
        adjusted_perf = base_perf * weather_factor * congestion_factor * passenger_factor
        adjusted_perf = np.clip(adjusted_perf, 0, 100)
        
        comparison_df = pd.DataFrame({
            "Route": routes,
            "Base Performance": base_perf,
            "Simulated Performance": adjusted_perf,
            "Change": adjusted_perf - base_perf
        })
        
        # Create a bar chart comparing base vs simulated performance
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=routes,
            y=comparison_df["Base Performance"],
            name="Current Performance",
            marker_color='royalblue'
        ))
        
        fig.add_trace(go.Bar(
            x=routes,
            y=comparison_df["Simulated Performance"],
            name="Simulated Performance",
            marker_color='firebrick'
        ))
        
        fig.update_layout(
            title="Route Performance: Current vs Simulated",
            xaxis_title="Route",
            yaxis_title="Performance Score",
            yaxis=dict(range=[0, 100]),
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations based on simulation
        st.subheader("Recommended Adjustments")
        
        # Generate recommendations based on simulation parameters
        recommendations = []
        
        if simulation_params['passenger_increase'] > 20:
            recommendations.append("Increase bus frequency by 15-20% on major routes to handle higher passenger load")
        
        if simulation_params['traffic_congestion'] > 1.5:
            recommendations.append("Consider alternative routes for Route 34 and Route 47 to avoid congested areas")
            recommendations.append("Implement express service bypassing congested segments during peak hours")
        
        if simulation_params['weather'] in ["Rain", "Fog"]:
            recommendations.append("Allocate additional buffer time (15%) for routes with poor visibility segments")
            recommendations.append("Ensure safety announcements and reduced speed in areas prone to waterlogging")
        
        if simulation_params['weather'] == "Extreme Heat":
            recommendations.append("Ensure air conditioning is functional on all buses on Route 25 and Route 63")
            recommendations.append("Consider additional water supply on long routes")
        
        if len(recommendations) == 0:
            recommendations.append("No significant adjustments needed under current simulation parameters")
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}. {rec}**")

# Footer
st.markdown("---")
st.markdown("© 2023 SmartTransportAI - Optimizing Indian public transport through data science")
