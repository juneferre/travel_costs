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

# --- Sidebar: Country filter ---
st.sidebar.title('Country Selection')
selected_countries = st.sidebar.multiselect(
    "Filter by Country/Territory (optional)",
    options=sorted(df["Country / Territory"].unique()),
    default=[]
)

# --- Filter data based on selected countries ---
if selected_countries:
    filtered_df = df[df["Country / Territory"].isin(selected_countries)]
else:
    filtered_df = df  # No filter applied

# --- Main panel: City multiselect ---
selected_cities = st.multiselect(
    "Choose cities to compare:",
    options=sorted(filtered_df["City"].unique()),
    default=[]
)

# --- Traveler type selector ---
traveler_type = st.radio(
    "Are you traveling solo or as a?",
    ["Individual", "Couple"],
    horizontal=True
)

# --- Number of days input ---
num_days = st.number_input(
    "How many days are you traveling?",
    min_value=1,
    max_value=365,
    value=7
)

# --- Cost estimation function ---
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

# --- Show estimated trip costs for selected cities ---
if selected_cities:
    st.subheader(f"Estimated Trip Costs for {num_days} Days")
    cols = st.columns(len(selected_cities)) if len(selected_cities) <= 4 else None

    for i, city in enumerate(selected_cities):
        cost = estimate_trip_cost(city, num_days, traveler_type)
        if cols:
            with cols[i]:
                st.metric(label=city, value=f"${cost:,.0f}")
        else:
            st.metric(label=city, value=f"${cost:,.0f}")
else:
    st.info("Select one or more cities above to view estimated trip costs.")
