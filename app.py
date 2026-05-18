import pandas as pd
import plotly.express as px
import streamlit as st

from src.optimizer import carbon_aware_shift
from src.metrics import calculate_emissions, summarize_results


st.set_page_config(
    page_title="Carbon-Aware Load Shifting",
    layout="wide"
)

st.title("Carbon-Aware Load Shifting: Level 0 Backtest")

st.markdown(
    """
    This is a personal open-data portfolio prototype.

    It uses sample building-load and carbon-intensity data to test whether
    flexible electricity demand can be shifted away from high-carbon hours
    toward lower-carbon hours.

    This Level 0 version is an offline backtest. It does not use employer data,
    live APIs, or real building-control actions.
    """
)

load_path = "data/sample/sample_building_load.csv"
carbon_path = "data/sample/sample_carbon_signal.csv"

load_df = pd.read_csv(load_path, parse_dates=["timestamp"])
carbon_df = pd.read_csv(carbon_path, parse_dates=["timestamp"])

df = pd.merge(load_df, carbon_df, on="timestamp", how="inner")

st.sidebar.header("Scenario Settings")

flexible_fraction = st.sidebar.slider(
    "Flexible load fraction",
    min_value=0.00,
    max_value=0.30,
    value=0.10,
    step=0.01,
    format="%.2f"
)

high_carbon_quantile = st.sidebar.slider(
    "High-carbon threshold quantile",
    min_value=0.50,
    max_value=0.95,
    value=0.75,
    step=0.05
)

low_carbon_quantile = st.sidebar.slider(
    "Low-carbon threshold quantile",
    min_value=0.05,
    max_value=0.50,
    value=0.25,
    step=0.05
)

optimized_df = carbon_aware_shift(
    df=df,
    flexible_fraction=flexible_fraction,
    high_carbon_quantile=high_carbon_quantile,
    low_carbon_quantile=low_carbon_quantile,
)

result_df = calculate_emissions(optimized_df)
summary = summarize_results(result_df)

st.subheader("Backtest Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Estimated Avoided CO₂",
    f"{summary['avoided_emissions_kg']:,.1f} kg"
)

col2.metric(
    "Avoided CO₂ %",
    f"{summary['avoided_emissions_percent']:.2f}%"
)

col3.metric(
    "Shifted Load",
    f"{summary['shifted_kwh']:,.1f} kWh"
)

col4.metric(
    "Peak Load Change",
    f"{summary['optimized_peak_kwh'] - summary['baseline_peak_kwh']:.1f} kWh"
)

st.subheader("Baseline vs Optimized Load")

load_chart_df = result_df[
    ["timestamp", "load_kwh", "optimized_load_kwh"]
].melt(
    id_vars="timestamp",
    var_name="schedule",
    value_name="load_value_kwh"
)

fig_load = px.line(
    load_chart_df,
    x="timestamp",
    y="load_value_kwh",
    color="schedule",
    title="Building Load Before and After Carbon-Aware Shifting"
)

st.plotly_chart(fig_load, width="stretch")

st.subheader("Carbon Intensity Signal")

fig_carbon = px.line(
    result_df,
    x="timestamp",
    y="carbon_intensity_kg_per_mwh",
    title="Carbon Intensity Signal"
)

st.plotly_chart(fig_carbon, width="stretch")


st.subheader("Emissions Comparison")

emissions_chart_df = result_df[
    ["timestamp", "baseline_emissions_kg", "optimized_emissions_kg"]
].melt(
    id_vars="timestamp",
    var_name="scenario",
    value_name="emissions_kg"
)

fig_emissions = px.line(
    emissions_chart_df,
    x="timestamp",
    y="emissions_kg",
    color="scenario",
    title="Baseline vs Optimized Estimated Emissions"
)

st.plotly_chart(fig_emissions, width="stretch")

st.subheader("Data Preview")

st.dataframe(result_df.head(100))
