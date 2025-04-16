import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import streamlit as st
import numpy as np

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

# filter cities based on country selection
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

# individual or couple?
traveler_type = st.radio(
    "Who are you traveling as?",
    ["Individual", "Couple"],
    horizontal=True  
)


def estimate_trip_cost(city, days, traveler_type):
    row = df[df["City"] == city].iloc[0]

    suffix = "(Individual)" if traveler_type == "Individual" else "(Couple)"

    if days <= 3:
        return row["Daily Cost"] * days

    elif days <= 7:
        daily_total = row["Daily Cost"] * days
        week_total = row[f"1 Week {suffix}"]
        return np.interp(days, [3, 7], [daily_total, week_total])

    elif days <= 14:
        return np.interp(days, [7, 14], [row[f"1 Week {suffix}"], row[f"2 Weeks {suffix}"]])

    elif days <= 30:
        return np.interp(days, [14, 30], [row[f"2 Weeks {suffix}"], row[f"1 Month {suffix}"]])

    else:
        months = days // 30
        remainder = days % 30
        return months * row[f"1 Month {suffix}"] + remainder * row["Daily Cost"]

selected_city = st.selectbox("Select a city for custom trip estimate:", filtered_df["City"].unique())
num_days = st.number_input("How many days are you traveling?", min_value=1, max_value=365, value=7)


estimated_total = estimate_trip_cost(selected_city, num_days, traveler_type)
st.metric(label=f"Estimated Trip Cost for {num_days} days in {selected_city}", value=f"${estimated_total:,.0f}")
