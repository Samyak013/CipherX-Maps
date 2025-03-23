"""
SmartTransportAI - Urban Public Transport Route Optimization System
------------------------------------------------------------------
A data-driven application that optimizes public transport routes in Indian cities
using real-time data, predictive analytics, and reinforcement learning.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from datetime import datetime, timedelta
import json
import os
import requests
from io import BytesIO
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="SmartTransportAI - Urban Transport Optimization",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application title and description
st.title("🚌 SmartTransportAI")
st.markdown("### Smart Public Transport Route Optimization for Indian Cities")
st.markdown("""
This application uses data science and AI to optimize public transport routes based on:
- Real-time traffic conditions and GPS location data
- Passenger demand patterns
- Weather impacts
- Special events
""")

# Create sidebar for navigation and filters
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose a mode",
    ["Route Planner", "Dashboard", "Route Optimization", "Demand Forecasting", "Congestion Analysis", "About"]
)

# City selection (expanded with more Indian cities)
city = st.sidebar.selectbox(
    "Select City",
    [
        "Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", 
        "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur", 
        "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Patna",
        "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad",
        "Meerut", "Rajkot", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad",
        "Amritsar", "Allahabad", "Ranchi", "Coimbatore", "Jabalpur", "Guwahati",
        "Chandigarh", "Thiruvananthapuram", "Solapur", "Tiruchirappalli"
    ]
)

# Function to get user's current location (placeholder for actual GPS implementation)
def get_current_location():
    # In a real implementation, this would use the browser's geolocation API
    # For now, we'll return default coordinates based on the selected city
    city_coordinates = {
        "Mumbai": [19.0760, 72.8777],
        "Delhi": [28.6139, 77.2090],
        "Bangalore": [12.9716, 77.5946],
        "Chennai": [13.0827, 80.2707],
        "Hyderabad": [17.3850, 78.4867],
        "Kolkata": [22.5726, 88.3639],
        "Pune": [18.5204, 73.8567],
        "Ahmedabad": [23.0225, 72.5714],
        "Jaipur": [26.9124, 75.7873],
        # Add other cities as needed
    }
    
    return city_coordinates.get(city, [20.5937, 78.9629])  # Default to center of India

# Load transport infrastructure data
@st.cache_data
def load_transport_infrastructure(selected_city):
    """Load transport infrastructure data for the selected city"""
    # In a real implementation, this would load from a database or API
    # For now, we'll use sample data
    
    # Dictionary with sample data for each city
    city_infrastructure = {
        "Mumbai": {
            "railway_stations": [
                {"name": "Chhatrapati Shivaji Terminus (CST)", "lat": 18.9402, "lon": 72.8351},
                {"name": "Dadar Railway Station", "lat": 19.0211, "lon": 72.8426},
                {"name": "Lokmanya Tilak Terminus", "lat": 19.0712, "lon": 72.8889},
                {"name": "Mumbai Central", "lat": 18.9712, "lon": 72.8213},
                {"name": "Bandra Terminus", "lat": 19.0596, "lon": 72.8295}
            ],
            "airports": [
                {"name": "Chhatrapati Shivaji International Airport", "lat": 19.0896, "lon": 72.8656}
            ],
            "bus_stations": [
                {"name": "Mumbai Central Bus Depot", "lat": 18.9693, "lon": 72.8198},
                {"name": "Dadar Bus Depot", "lat": 19.0178, "lon": 72.8478},
                {"name": "Borivali Bus Depot", "lat": 19.2278, "lon": 72.8620},
                {"name": "Thane Bus Depot", "lat": 19.1943, "lon": 72.9627},
                {"name": "Kurla Bus Depot", "lat": 19.0703, "lon": 72.8810}
            ],
            "metro_stations": [
                {"name": "Ghatkopar Metro Station", "lat": 19.0866, "lon": 72.9093},
                {"name": "Andheri Metro Station", "lat": 19.1197, "lon": 72.8464},
                {"name": "Versova Metro Station", "lat": 19.1344, "lon": 72.8186},
                {"name": "Saki Naka Metro Station", "lat": 19.0984, "lon": 72.8889}
            ]
        },
        "Delhi": {
            "railway_stations": [
                {"name": "New Delhi Railway Station", "lat": 28.6425, "lon": 77.2198},
                {"name": "Old Delhi Railway Station", "lat": 28.6586, "lon": 77.2284},
                {"name": "Hazrat Nizamuddin Railway Station", "lat": 28.5877, "lon": 77.2518},
                {"name": "Anand Vihar Terminal", "lat": 28.6472, "lon": 77.3016},
                {"name": "Delhi Sarai Rohilla", "lat": 28.6653, "lon": 77.1927}
            ],
            "airports": [
                {"name": "Indira Gandhi International Airport", "lat": 28.5561, "lon": 77.0998}
            ],
            "bus_stations": [
                {"name": "ISBT Kashmere Gate", "lat": 28.6680, "lon": 77.2304},
                {"name": "ISBT Anand Vihar", "lat": 28.6462, "lon": 77.2821},
                {"name": "ISBT Sarai Kale Khan", "lat": 28.5903, "lon": 77.2495},
                {"name": "Dhaula Kuan Bus Terminal", "lat": 28.5921, "lon": 77.1536}
            ],
            "metro_stations": [
                {"name": "Rajiv Chowk Metro Station", "lat": 28.6333, "lon": 77.2195},
                {"name": "Central Secretariat Metro Station", "lat": 28.6147, "lon": 77.2117},
                {"name": "Kashmere Gate Metro Station", "lat": 28.6674, "lon": 77.2295},
                {"name": "Hauz Khas Metro Station", "lat": 28.5432, "lon": 77.2044}
            ]
        },
        # Add data for other cities
    }
    
    # Return data for the selected city, or empty lists if city not in the dictionary
    if selected_city in city_infrastructure:
        return city_infrastructure[selected_city]
    else:
        return {
            "railway_stations": [],
            "airports": [],
            "bus_stations": [],
            "metro_stations": []
        }

# Function to calculate routes between places
def calculate_routes(start_location, end_location, city, transport_modes=None):
    """
    Calculate routes between start and end locations using various transport modes
    
    Args:
        start_location (str): Starting location
        end_location (str): Destination location
        city (str): City name
        transport_modes (list): List of transport modes to include
        
    Returns:
        dict: Dictionary with route options
    """
    # In a real implementation, this would use Google Maps API or similar
    # For now, we'll generate synthetic routes for demo purposes
    
    # Default transport modes if none provided
    if transport_modes is None:
        transport_modes = ["bus", "train", "metro", "walking", "cycling"]
    
    # Calculate straight-line distance (simplified)
    # In real implementation, we would geocode addresses and use actual route distances
    if city == "Mumbai":
        # Example coordinates for Mumbai
        coordinates = {
            "CST": (18.9402, 72.8351),
            "Dadar": (19.0211, 72.8426),
            "Andheri": (19.1197, 72.8464),
            "Borivali": (19.2278, 72.8620),
            "Thane": (19.1943, 72.9627),
            "Bandra": (19.0596, 72.8295),
            "Kurla": (19.0703, 72.8810),
            "Powai": (19.1214, 72.9097),
            "Ghatkopar": (19.0866, 72.9093),
            "Worli": (19.0217, 72.8170),
            "BKC": (19.0654, 72.8695),
            "Juhu": (19.1075, 72.8263),
            "Chembur": (19.0534, 72.9002),
            "Sion": (19.0379, 72.8691),
            "Versova": (19.1344, 72.8186),
            "Airport": (19.0896, 72.8656),
            "Vashi": (19.0759, 72.9963),
            "Mulund": (19.1763, 72.9572),
            "Goregaon": (19.1663, 72.8526),
            "Kandivali": (19.2065, 72.8570)
        }
    else:
        # For other cities, we would have similar dictionaries
        # For now, just use placeholder values
        coordinates = {
            "Central": (20.0, 77.0),
            "North": (20.1, 77.0),
            "South": (19.9, 77.0),
            "East": (20.0, 77.1),
            "West": (20.0, 76.9),
            "Airport": (20.05, 77.05),
            "Station": (20.02, 77.03),
            "Downtown": (20.01, 77.01),
            "Suburb": (20.08, 77.08)
        }
    
    # Try to find coordinates for the locations
    start_coords = None
    end_coords = None
    
    # Simple matching (in a real app, we'd use geocoding)
    for name, coords in coordinates.items():
        if name.lower() in start_location.lower():
            start_coords = coords
        if name.lower() in end_location.lower():
            end_coords = coords
    
    # If locations not found, use defaults
    if start_coords is None:
        start_coords = coordinates.get(list(coordinates.keys())[0])
    if end_coords is None:
        end_coords = coordinates.get(list(coordinates.keys())[-1])
    
    # Calculate distance in km using haversine formula
    import math
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    distance = haversine(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
    
    # Generate route options
    routes = []
    
    # Add route options based on selected transport modes
    if "bus" in transport_modes:
        # Bus route
        routes.append({
            "mode": "bus",
            "icon": "🚌",
            "duration_minutes": int(distance * 4),  # Assumption: bus travels at 15 km/h
            "distance_km": round(distance * 1.3, 1),  # Bus routes are typically longer
            "cost": int(distance * 5),  # ₹5 per km
            "emissions": round(distance * 0.7, 1),  # kg CO2
            "transfers": 1 if distance > 5 else 0,
            "congestion_level": 0.7,
            "departure_frequency": "Every 10-15 minutes",
            "route_steps": [
                {"step": 1, "description": f"Walk to nearest bus stop", "time": "5 min"},
                {"step": 2, "description": f"Take Bus Route {100 + int(distance)}", "time": f"{int(distance * 3)} min"},
                {"step": 3, "description": "Walk to destination", "time": "5 min"}
            ]
        })
    
    if "train" in transport_modes:
        # Train route
        train_available = distance > 3  # Only show train option for longer distances
        if train_available:
            routes.append({
                "mode": "train",
                "icon": "🚆",
                "duration_minutes": int(distance * 2),  # Assumption: train travels at 30 km/h avg
                "distance_km": round(distance * 1.2, 1),
                "cost": int(distance * 3),  # ₹3 per km
                "emissions": round(distance * 0.4, 1),
                "transfers": 0 if distance < 10 else 1,
                "congestion_level": 0.8,
                "departure_frequency": "Every 15-20 minutes",
                "route_steps": [
                    {"step": 1, "description": "Walk to nearest railway station", "time": "8 min"},
                    {"step": 2, "description": f"Take {('Western' if start_coords[1] < 72.9 else 'Central')} Line train", "time": f"{int(distance * 1.5)} min"},
                    {"step": 3, "description": "Walk to destination", "time": "10 min"}
                ]
            })
    
    if "metro" in transport_modes:
        # Metro route
        metro_available = city in ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata"]
        if metro_available:
            routes.append({
                "mode": "metro",
                "icon": "🚇",
                "duration_minutes": int(distance * 1.5),  # Metro is faster
                "distance_km": round(distance * 1.1, 1),
                "cost": int(distance * 4),  # ₹4 per km
                "emissions": round(distance * 0.2, 1),
                "transfers": 0 if distance < 8 else 1,
                "congestion_level": 0.6,
                "departure_frequency": "Every 5-8 minutes",
                "route_steps": [
                    {"step": 1, "description": "Walk to nearest metro station", "time": "6 min"},
                    {"step": 2, "description": "Take Metro Line 1", "time": f"{int(distance * 1.2)} min"},
                    {"step": 3, "description": "Walk to destination", "time": "7 min"}
                ]
            })
    
    if "walking" in transport_modes:
        # Walking route
        walking_available = distance < 5  # Only show walking for shorter distances
        if walking_available:
            routes.append({
                "mode": "walking",
                "icon": "🚶",
                "duration_minutes": int(distance * 12),  # Assumption: walking at 5 km/h
                "distance_km": round(distance, 1),
                "cost": 0,
                "emissions": 0,
                "transfers": 0,
                "congestion_level": 0.1,
                "departure_frequency": "On demand",
                "route_steps": [
                    {"step": 1, "description": f"Walk from {start_location} to {end_location}", "time": f"{int(distance * 12)} min"}
                ]
            })
    
    if "cycling" in transport_modes:
        # Cycling route
        cycling_available = distance < 10  # Only show cycling for moderate distances
        if cycling_available:
            routes.append({
                "mode": "cycling",
                "icon": "🚲",
                "duration_minutes": int(distance * 4),  # Assumption: cycling at 15 km/h
                "distance_km": round(distance * 1.05, 1),
                "cost": 0 if distance < 3 else 20,  # Free for short distances, otherwise rental cost
                "emissions": 0,
                "transfers": 0,
                "congestion_level": 0.3,
                "departure_frequency": "On demand",
                "route_steps": [
                    {"step": 1, "description": "Pick up bicycle", "time": "3 min"},
                    {"step": 2, "description": f"Cycle from {start_location} to {end_location}", "time": f"{int(distance * 4)} min"}
                ]
            })
    
    # Sort routes by duration
    routes.sort(key=lambda x: x["duration_minutes"])
    
    return {
        "start_location": start_location,
        "end_location": end_location,
        "city": city,
        "total_routes": len(routes),
        "routes": routes
    }

# Based on the selected mode, show the appropriate content
if app_mode == "Route Planner":
    st.header(f"Public Transport Route Planner - {city}")
    
    st.markdown("""
    Find the optimal public transport routes between any two locations.
    This planner will suggest the best routes based on real-time traffic conditions, 
    weather, and available transport options.
    """)
    
    # Load transportation infrastructure for the selected city
    infrastructure = load_transport_infrastructure(city)
    
    # Get all major locations in the selected city for suggestions
    all_locations = []
    for station in infrastructure["railway_stations"]:
        all_locations.append(station["name"])
    for station in infrastructure["metro_stations"]:
        all_locations.append(station["name"])
    for station in infrastructure["bus_stations"]:
        all_locations.append(station["name"])
    for airport in infrastructure["airports"]:
        all_locations.append(airport["name"])
    
    # If Mumbai, add additional landmarks
    if city == "Mumbai":
        landmarks = ["CST", "Dadar", "Andheri", "Borivali", "Thane", "Bandra", "Kurla", 
                    "Powai", "Ghatkopar", "Worli", "BKC", "Juhu", "Chembur", "Sion", 
                    "Versova", "Vashi", "Mulund", "Goregaon", "Kandivali"]
        all_locations.extend(landmarks)
    
    # If no locations available, add some default ones
    if not all_locations:
        all_locations = ["Downtown", "Airport", "Central Station", "University", "Mall", "Business District"]
    
    # Add current location option
    all_locations = ["Current Location"] + sorted(set(all_locations))
    
    # Create route planning form
    with st.form("route_planner_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Starting Point")
            
            # Option to use current location
            use_current_location = st.checkbox("Use current GPS location", key="use_current_location")
            
            if use_current_location:
                start_location = "Current Location"
                st.info("Using your current location as the starting point.")
            else:
                # Dropdown with autocomplete for start location
                start_location = st.selectbox(
                    "Select starting point",
                    all_locations,
                    index=0,
                    key="start_location_select"
                )
                
                # Or allow typing custom location
                custom_start = st.text_input("Or enter a custom starting point", key="custom_start")
                if custom_start:
                    start_location = custom_start
        
        with col2:
            st.subheader("Destination")
            
            # Dropdown with autocomplete for destination
            end_location = st.selectbox(
                "Select destination",
                all_locations,
                index=min(1, len(all_locations) - 1),
                key="end_location_select"
            )
            
            # Or allow typing custom destination
            custom_end = st.text_input("Or enter a custom destination", key="custom_end")
            if custom_end:
                end_location = custom_end
        
        # Add travel preferences
        st.subheader("Travel Preferences")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            travel_time = st.selectbox(
                "When do you want to travel?",
                ["Now", "Morning (8-10 AM)", "Midday (11 AM-3 PM)", "Evening (5-7 PM)", "Night (8 PM-12 AM)"],
                index=0
            )
            
            travel_date = st.date_input(
                "Travel date",
                datetime.now().date()
            )
        
        with col2:
            # Transport mode selection
            st.write("Transport modes to include:")
            
            bus_mode = st.checkbox("Bus", value=True)
            train_mode = st.checkbox("Train", value=True)
            metro_mode = st.checkbox("Metro", value=True)
            walking_mode = st.checkbox("Walking", value=True)
            cycling_mode = st.checkbox("Cycling", value=True)
        
        with col3:
            # Route preferences
            route_preference = st.radio(
                "Route preference",
                ["Fastest", "Cheapest", "Eco-friendly", "Least transfers"]
            )
            
            accessibility_needed = st.checkbox("Need accessible route", value=False)
        
        # Submit button
        submit_button = st.form_submit_button(label="Find Routes")
    
    # Process the form submission
    if submit_button:
        # Get selected transport modes
        transport_modes = []
        if bus_mode:
            transport_modes.append("bus")
        if train_mode:
            transport_modes.append("train")
        if metro_mode:
            transport_modes.append("metro")
        if walking_mode:
            transport_modes.append("walking")
        if cycling_mode:
            transport_modes.append("cycling")
        
        # Check if at least one mode is selected
        if not transport_modes:
            st.error("Please select at least one transport mode.")
        else:
            # If using current location, get it
            if start_location == "Current Location":
                current_coords = get_current_location()
                start_location = f"Your Location ({current_coords[0]:.4f}, {current_coords[1]:.4f})"
            
            # Calculate routes
            with st.spinner(f"Finding routes from {start_location} to {end_location}..."):
                routes_result = calculate_routes(start_location, end_location, city, transport_modes)
            
            if routes_result["total_routes"] > 0:
                st.success(f"Found {routes_result['total_routes']} routes from {start_location} to {end_location}")
                
                # Show route on map
                st.subheader("Route Map")
                
                # Create a dataframe for the route
                if start_location != "Current Location" and city == "Mumbai":
                    try:
                        # Since we're not using actual geocoding, this is approximate
                        route_points = pd.DataFrame({
                            'lat': [19.0760, 19.0790, 19.0850, 19.0930, 19.0980, 19.1010],
                            'lon': [72.8777, 72.8800, 72.8850, 72.8890, 72.8920, 72.8950],
                            'stop_name': [f'Start - {start_location}', 'Stop 1', 'Stop 2', 'Stop 3', 'Stop 4', f'End - {end_location}'],
                            'congestion': [0.2, 0.5, 0.8, 0.4, 0.3, 0.2]
                        })
                        
                        # Create a Streamlit map showing the route
                        st.map(route_points)
                    except:
                        # Fallback if there's an error with the map
                        st.warning("Route map visualization not available for this route.")
                
                # Display route options
                st.subheader("Available Routes")
                
                # Create tabs for different route options
                route_tabs = st.tabs([f"{route['icon']} {route['mode'].capitalize()}" for route in routes_result["routes"]])
                
                for i, tab in enumerate(route_tabs):
                    route = routes_result["routes"][i]
                    
                    with tab:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.markdown(f"### {route['mode'].capitalize()} Route")
                            st.markdown(f"**Time:** {route['duration_minutes']} minutes")
                            st.markdown(f"**Distance:** {route['distance_km']} km")
                            st.markdown(f"**Cost:** ₹{route['cost']}")
                            
                            if route['transfers'] > 0:
                                st.markdown(f"**Transfers:** {route['transfers']}")
                        
                        with col2:
                            st.markdown("**Departure**")
                            st.markdown(f"{route['departure_frequency']}")
                            
                            st.markdown("**Emissions**")
                            st.markdown(f"{route['emissions']} kg CO₂")
                        
                        with col3:
                            st.markdown("**Congestion Level**")
                            
                            # Display congestion as a progress bar
                            congestion_color = "red" if route['congestion_level'] > 0.7 else "orange" if route['congestion_level'] > 0.4 else "green"
                            st.markdown(f"<div style='width:100%;background-color:#ddd;border-radius:3px;'><div style='width:{int(route['congestion_level']*100)}%;background-color:{congestion_color};height:10px;border-radius:3px;'></div></div>", unsafe_allow_html=True)
                            
                            if route['congestion_level'] > 0.7:
                                st.markdown("High congestion")
                            elif route['congestion_level'] > 0.4:
                                st.markdown("Moderate congestion")
                            else:
                                st.markdown("Low congestion")
                        
                        # Show step-by-step directions
                        st.markdown("### Step-by-Step Directions")
                        
                        for step in route['route_steps']:
                            st.markdown(f"**{step['step']}.** {step['description']} ({step['time']})")
            else:
                st.error(f"No routes found between {start_location} and {end_location}. Please try different locations or transport modes.")

elif app_mode == "Dashboard":
    st.header(f"Public Transport Dashboard - {city}")
    
    # Display key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Active Vehicles", value="237", delta="12")
    with col2:
        st.metric(label="Avg. Delay", value="4.2 min", delta="-0.8 min")
    with col3:
        st.metric(label="On-time %", value="86%", delta="3%")
    with col4:
        st.metric(label="Passenger Load", value="High", delta=None)
    
    # Add a map view
    st.subheader("Real-time Transport Network")
    
    # We'll create a basic map view with some dummy locations for now
    # This will be replaced with actual data later
    df = pd.DataFrame({
        'lat': [19.076, 19.0760, 19.0790, 19.0850, 19.0930, 19.0898],
        'lon': [72.8777, 72.8795, 72.8780, 72.8877, 72.8919, 72.8882],
        'name': ['Chhatrapati Shivaji Terminus', 'Stop A', 'Stop B', 'Stop C', 'Stop D', 'Stop E'],
        'congestion': [1, 2, 3, 1, 2, 3]
    })
    
    st.map(df)
    
    # We'll add more visualizations here later
    st.subheader("Traffic Congestion by Hour")
    
    # Create some example data for a 24-hour traffic pattern
    hours = list(range(24))
    congestion = [0.2, 0.1, 0.1, 0.1, 0.2, 0.4, 0.7, 0.9, 0.8, 0.6, 0.5, 0.6, 
                 0.7, 0.6, 0.6, 0.7, 0.8, 0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2]
    
    # Create a bar chart
    fig = px.bar(
        x=hours,
        y=congestion,
        labels={'x': 'Hour of Day', 'y': 'Congestion Level'},
        color=congestion,
        color_continuous_scale='RdYlGn_r'
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif app_mode == "Route Optimization":
    st.header(f"Route Optimization - {city}")
    
    st.markdown("""
    This section demonstrates how AI can optimize public transport routes based on current conditions.
    
    Choose parameters below to simulate different scenarios:
    """)
    
    # Create selection options for route optimization
    col1, col2 = st.columns(2)
    
    with col1:
        route_type = st.selectbox(
            "Transport Type",
            ["Bus", "Metro/Train", "Both"]
        )
        
        optimization_goal = st.selectbox(
            "Optimization Goal",
            ["Minimize Travel Time", "Maximize Ridership", "Minimize Transfers", "Minimize Operational Cost"]
        )
    
    with col2:
        time_of_day = st.selectbox(
            "Time of Day",
            ["Morning Rush (8-10 AM)", "Midday (11 AM-3 PM)", "Evening Rush (5-7 PM)", "Night (8 PM-12 AM)"]
        )
        
        weather_condition = st.selectbox(
            "Weather Condition",
            ["Normal", "Heavy Rain", "Extreme Heat", "Fog/Low Visibility"]
        )
    
    # Button to trigger optimization
    if st.button("Optimize Routes"):
        st.info("Optimizing routes based on selected criteria...")
        
        # Show a progress bar to simulate processing
        import time
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)  # Small delay
            progress_bar.progress(i + 1)
        
        # Display a sample optimized route on the map
        st.subheader("Optimized Route Map")
        
        # Sample data for Mumbai
        if city == "Mumbai":
            route_points = pd.DataFrame({
                'lat': [19.0760, 19.0790, 19.0850, 19.0930, 19.0980, 19.1010],
                'lon': [72.8777, 72.8800, 72.8850, 72.8890, 72.8920, 72.8950],
                'stop_name': ['Start - CST', 'Stop 1', 'Stop 2', 'Stop 3', 'Stop 4', 'End - Dadar'],
                'congestion': [0.2, 0.5, 0.8, 0.4, 0.3, 0.2]
            })
            
            # Create a Streamlit map showing the route
            st.map(route_points)
            
            # Display route statistics
            st.subheader("Optimized Route Statistics")
            
            st.markdown(f"""
            **Route**: CST to Dadar  
            **Distance**: 7.2 km  
            **Estimated Time**: 22 minutes (12 minutes saved)  
            **Expected Ridership**: 142 passengers  
            **Service Frequency**: Every 8 minutes during {time_of_day}  
            """)
            
            # Show before and after comparison
            st.subheader("Before vs After Optimization")
            
            comparison_data = pd.DataFrame({
                'Metric': ['Travel Time (min)', 'Ridership', 'Operational Cost (₹)', 'CO2 Emissions (kg)'],
                'Before': [34, 98, 4200, 86],
                'After': [22, 142, 3800, 74],
                'Improvement': ['35%', '45%', '10%', '14%']
            })
            
            st.table(comparison_data)

elif app_mode == "Demand Forecasting":
    st.header(f"Passenger Demand Forecasting - {city}")
    
    st.markdown("""
    This section shows forecasted passenger demand patterns based on historical data,
    upcoming events, weather forecasts, and other factors.
    """)
    
    # Create date selection for forecasting
    forecast_date = st.date_input(
        "Select date for forecast",
        datetime.now().date()
    )
    
    # Create a selector for route or area
    area_selector = st.selectbox(
        "Select Route/Area",
        ["All Routes", "Central Lines", "Harbor Line", "Western Line", "Metro Line 1", "Metro Line 2"]
    )
    
    if st.button("Generate Forecast"):
        st.info(f"Generating passenger demand forecast for {area_selector} on {forecast_date}...")
        
        # Create a line chart showing hourly demand forecast
        hours = list(range(24))
        
        # Different demand patterns based on the selected route/area
        if area_selector == "Western Line":
            demand = [120, 80, 40, 60, 180, 620, 1200, 1400, 1100, 800, 600, 650, 
                     700, 650, 600, 750, 950, 1350, 1150, 850, 600, 450, 320, 180]
        elif area_selector == "Metro Line 1":
            demand = [60, 30, 10, 20, 90, 320, 700, 950, 800, 550, 400, 480, 
                     520, 450, 400, 500, 680, 900, 750, 520, 380, 240, 150, 90]
        else:
            demand = [200, 120, 50, 70, 220, 720, 1400, 1800, 1500, 1100, 900, 950, 
                     1000, 950, 900, 1100, 1400, 1900, 1600, 1200, 900, 650, 450, 250]
        
        # Create a dataframe for visualization
        forecast_df = pd.DataFrame({
            'Hour': hours,
            'Passengers': demand
        })
        
        # Plot the forecast
        fig = px.line(
            forecast_df, 
            x='Hour', 
            y='Passengers',
            title=f'Passenger Demand Forecast for {area_selector} on {forecast_date}',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Estimated Passengers",
            hovermode="x unified"
        )
        
        # Add ranges for morning and evening rush hours
        fig.add_vrect(
            x0=7, x1=10, 
            fillcolor="rgba(255, 0, 0, 0.1)", opacity=0.3, 
            layer="below", line_width=0,
            annotation_text="Morning Rush Hour", 
            annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=17, x1=20, 
            fillcolor="rgba(255, 0, 0, 0.1)", opacity=0.3, 
            layer="below", line_width=0,
            annotation_text="Evening Rush Hour", 
            annotation_position="top left"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add recommendation based on forecast
        st.subheader("AI Recommendations")
        
        st.markdown(f"""
        Based on the forecast for {area_selector} on {forecast_date}, we recommend:
        
        1. **Increase service frequency** between 8-10 AM and 5-8 PM to accommodate peak demand
        2. **Add 4 additional vehicles** during morning rush hour
        3. **Reduce service frequency** between 11 AM-3 PM to save operational costs
        4. **Expected impact**: 15% reduction in wait times and 8% increase in ridership
        """)

elif app_mode == "Congestion Analysis":
    st.header(f"Traffic Congestion Analysis - {city}")
    
    st.markdown("""
    This section analyzes traffic congestion patterns and their impact on public transport.
    It helps identify bottlenecks and suggests route adjustments.
    """)
    
    # Create a map showing congestion hotspots
    st.subheader("Congestion Hotspots")
    
    # Create some sample congestion data
    if city == "Mumbai":
        congestion_data = pd.DataFrame({
            'lat': [19.0760, 19.0660, 19.0560, 19.1170, 19.0430, 19.0890, 19.0590],
            'lon': [72.8777, 72.8700, 72.8695, 72.9075, 72.8820, 72.8882, 72.8350],
            'location': ['CST Area', 'Marine Drive', 'Nariman Point', 'BKC', 'Worli', 'Dadar', 'Mahim'],
            'congestion_level': [0.9, 0.7, 0.5, 0.8, 0.7, 0.9, 0.6]
        })
    else:
        # Generate some random data for other cities
        np.random.seed(42)  # For reproducibility
        congestion_data = pd.DataFrame({
            'lat': np.random.uniform(17.0, 28.7, 7),
            'lon': np.random.uniform(72.0, 88.4, 7),
            'location': [f'Location {i}' for i in range(1, 8)],
            'congestion_level': np.random.uniform(0.4, 0.9, 7)
        })
    
    # Create a custom map with congestion color coding
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=congestion_data['lat'].mean(),
            longitude=congestion_data['lon'].mean(),
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=congestion_data,
                get_position='[lon, lat]',
                get_color='[255, int(255 * (1 - congestion_level)), 0, 160]',
                get_radius=500,
                pickable=True,
            ),
        ],
        tooltip={"text": "{location}\nCongestion Level: {congestion_level}"},
    ))
    
    # Show hourly congestion pattern
    st.subheader("Hourly Congestion Pattern")
    
    # Create hours
    hours = list(range(24))
    
    # Create different congestion patterns for different areas
    areas = ['CST Area', 'Dadar', 'BKC', 'Worli']
    
    # Create a DataFrame with hourly congestion for each area
    hourly_data = pd.DataFrame({
        'Hour': hours * len(areas),
        'Area': [area for area in areas for _ in range(24)],
        'Congestion': [
            # CST Area
            0.3, 0.2, 0.1, 0.1, 0.2, 0.4, 0.7, 0.9, 0.8, 0.6, 0.5, 0.6, 
            0.7, 0.6, 0.5, 0.6, 0.7, 0.9, 0.7, 0.5, 0.4, 0.3, 0.3, 0.3,
            # Dadar
            0.4, 0.3, 0.2, 0.2, 0.3, 0.5, 0.8, 0.9, 0.7, 0.6, 0.6, 0.6, 
            0.6, 0.6, 0.6, 0.7, 0.9, 0.9, 0.8, 0.6, 0.5, 0.5, 0.4, 0.4,
            # BKC
            0.2, 0.1, 0.1, 0.1, 0.2, 0.4, 0.8, 0.9, 0.9, 0.8, 0.7, 0.7, 
            0.8, 0.8, 0.7, 0.8, 0.8, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2,
            # Worli
            0.3, 0.2, 0.2, 0.2, 0.3, 0.5, 0.7, 0.8, 0.7, 0.6, 0.5, 0.6, 
            0.6, 0.5, 0.5, 0.6, 0.8, 0.9, 0.7, 0.5, 0.4, 0.3, 0.3, 0.3,
        ]
    })
    
    # Create a line chart
    fig = px.line(
        hourly_data, 
        x='Hour', 
        y='Congestion', 
        color='Area',
        title='Hourly Congestion by Area',
        labels={'Congestion': 'Congestion Level', 'Hour': 'Hour of Day'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add recommendation based on congestion analysis
    st.subheader("Congestion Impact Analysis")
    
    st.markdown("""
    Based on the congestion analysis, we've identified several key insights:
    
    1. **Morning Peak (8-10 AM)**: Severe congestion in CST Area and BKC
    2. **Evening Peak (5-7 PM)**: Severe congestion in Dadar and Worli
    3. **Midday (11 AM-3 PM)**: Moderate congestion in all areas
    
    **Recommended Route Adjustments:**
    
    1. **Route Diversion**: Reroute buses from CST to Dadar via alternate roads during 8-10 AM
    2. **Express Service**: Implement express buses that skip less congested stops during peak hours
    3. **Dynamic Scheduling**: Adjust departure times based on predicted congestion patterns
    """)

elif app_mode == "About":
    st.header("About SmartTransportAI")
    
    st.markdown("""
    ### Project Overview
    
    SmartTransportAI is an AI-driven public transport route optimization system developed specifically for Indian cities.
    It uses data science, machine learning, and reinforcement learning to dynamically optimize bus and train routes
    based on real-time conditions, historical patterns, and predictive analytics.
    
    ### Key Features
    
    - **Real-time route optimization** based on current traffic, weather, and passenger demand
    - **Predictive analytics** to forecast passenger demand and congestion
    - **Reinforcement learning** for continuous improvement of route recommendations
    - **Anomaly detection** to identify unusual patterns requiring immediate attention
    - **Actionable insights** for transport authorities to improve efficiency
    
    ### Technologies Used
    
    - **Python** for data processing and backend logic
    - **Streamlit** for interactive web interface
    - **Pandas & NumPy** for data manipulation
    - **Plotly & PyDeck** for data visualization
    - **Machine Learning** for predictive models
    - **Reinforcement Learning** for optimization algorithms
    
    ### Data Sources
    
    - GTFS (General Transit Feed Specification) data for public transport schedules
    - Traffic APIs for real-time traffic conditions
    - Weather APIs for current and forecasted weather
    - Census and demographic data for population density analysis
    """)
    
    # Add contact information
    st.markdown("""
    ### Contact
    
    For more information or to provide feedback, please contact:
    
    **Email**: contact@smarttransport.ai  
    **Website**: www.smarttransport.ai  
    """)