def calculate_emissions(df):
    result_df = df.copy()
    result_df["baseline_emissions_kg"] = (
        result_df["load_kwh"] * result_df["carbon_intensity_kg_per_mwh"] / 1000
    )
    result_df["optimized_emissions_kg"] = (
        result_df["optimized_load_kwh"] * result_df["carbon_intensity_kg_per_mwh"] / 1000
    )
    return result_df


def summarize_results(result_df):
    avoided_emissions_kg = (
        result_df["baseline_emissions_kg"] - result_df["optimized_emissions_kg"]
    ).sum()
    baseline_total_emissions_kg = result_df["baseline_emissions_kg"].sum()

    avoided_emissions_percent = 0.0
    if baseline_total_emissions_kg > 0:
        avoided_emissions_percent = (
            avoided_emissions_kg / baseline_total_emissions_kg
        ) * 100

    shifted_kwh = (result_df["load_kwh"] - result_df["optimized_load_kwh"]).clip(
        lower=0
    ).sum()

    return {
        "avoided_emissions_kg": avoided_emissions_kg,
        "avoided_emissions_percent": avoided_emissions_percent,
        "shifted_kwh": shifted_kwh,
        "baseline_peak_kwh": result_df["load_kwh"].max(),
        "optimized_peak_kwh": result_df["optimized_load_kwh"].max(),
    }

