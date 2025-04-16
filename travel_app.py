import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import streamlit as st
import numpy as np
from io import StringIO
import altair as alt




file_id = st.secrets["google_drive"]["file_id"]
url = f"https://drive.google.com/uc?export=download&id={file_id}"
df = pd.read_csv(url)


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
    "Are you traveling solo or as a couple?",
    ["Individual", "Couple"],
    horizontal=True,

    key="traveler_type"
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
    tab1, tab2 = st.tabs(["💰 Total Cost", "🍽️ Cost Breakdown"])

    with tab1:
        st.subheader(f"Estimated Trip Costs for {num_days} Days")
        cols = st.columns(len(selected_cities)) if len(selected_cities) <= 4 else None
        for i, city in enumerate(selected_cities):
            cost = estimate_trip_cost(city, num_days, traveler_type)
            if cols:
                with cols[i]:
                    st.metric(label=city, value=f"${cost:,.0f}")
            else:
                st.metric(label=city, value=f"${cost:,.0f}")

    with tab2:
        st.subheader("Cost Breakdown per Day for Solo Travelers")

        cost_cols = ["Accommodation1", "Local Transportation1", "Food2", "Entertainment1", "Alcohol2"]
        breakdown = filtered_df[filtered_df["City"].isin(selected_cities)][["City"] + cost_cols]
        breakdown.set_index("City", inplace=True)
        breakdown.rename(columns={
            "Accommodation1": "Accommodation",
            "Local Transportation1": "Transport",
            "Food2": "Food",
            "Entertainment1": "Entertainment",
            "Alcohol2": "Alcohol"
        }, inplace=True)

        st.dataframe(breakdown.style.format("${:,.0f}"))


        st.subheader(f"Cost Breakdown for {num_days} Days")

        trip_total = breakdown * num_days
        st.dataframe(trip_total.style.format("${:,.0f}"))

        # --- Bar chart of total trip cost breakdown by category ---
        melted = trip_total.reset_index().melt(
            id_vars="City",
            var_name="Category",
             value_name="Cost"
        )

        chart = alt.Chart(melted).mark_bar().encode(
                x=alt.X("Category:N", title="Category"),
                y=alt.Y("Cost:Q", title="Total Cost"),
                color="pastel2",
                column=alt.Column("City:N", title=None, spacing=10)
        ).properties(
        title=f"Total Trip Cost Breakdown by Category for {num_days} Days"
)

        st.altair_chart(chart, use_container_width=True)


else:
    st.info("Select one or more cities above to view estimated trip costs.")






