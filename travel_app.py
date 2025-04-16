import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import streamlit as st

# import the dataset
df = pd.read_csv("final_trip_costs.csv") 

# title of the app
st.title('Trip Costs Planner')
st.write('This app helps you financially plan your trip costs. The costs are approximate and for the Mid-Range Budget Traveler (according to [BudgetYourTrip.com](https://www.budgetyourtrip.com)).')


# sidebar
st.sidebar.title('Country Selection')
with st.sidebar:
    selected_country = st.selectbox(
        "Filter by Country/Territory", 
        options=["All"] + sorted(df["Country / Territory"].unique())
    )

if selected_country == "All":
    city_options = df["City"].unique()
else:
    city_options = df[df["Country / Territory"] == selected_country]["City"].unique()

selected_cities = st.multiselect(
    "Choose cities to compare:", 
    options=city_options,
    default=["London", "Paris", "New York"]  
)