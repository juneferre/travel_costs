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



st.sidebar.title('Country Selection')

# sidebar
selected_countries = st.sidebar.multiselect(
    "Filter by Country/Territory (optional)", 
    options=sorted(df["Country / Territory"].unique()),
    default=[]
)

# Filter cities based on country selection
if selected_countries:
    filtered_df = df[df["Country / Territory"].isin(selected_countries)]
else:
    filtered_df = df  # no filter applied

# Main Panel: City Selector from Filtered List
selected_cities = st.multiselect(
    "Choose cities to compare:",
    options=sorted(filtered_df["City"].unique()),
    default=[]
)

# Show filtered data or metrics
if selected_cities:
    city_data = df[df["City"].isin(selected_cities)]
    st.dataframe(city_data)
