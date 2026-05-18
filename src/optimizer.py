def carbon_aware_shift(df, flexible_fraction, high_carbon_quantile, low_carbon_quantile):
    optimized_df = df.copy()
    optimized_df["optimized_load_kwh"] = optimized_df["load_kwh"]

    high_carbon_threshold = optimized_df["carbon_intensity_kg_per_mwh"].quantile(
        high_carbon_quantile
    )
    low_carbon_threshold = optimized_df["carbon_intensity_kg_per_mwh"].quantile(
        low_carbon_quantile
    )

    high_carbon_mask = (
        optimized_df["carbon_intensity_kg_per_mwh"] >= high_carbon_threshold
    )
    low_carbon_mask = optimized_df["carbon_intensity_kg_per_mwh"] <= low_carbon_threshold

    shiftable_kwh = optimized_df.loc[high_carbon_mask, "load_kwh"] * flexible_fraction
    optimized_df.loc[high_carbon_mask, "optimized_load_kwh"] -= shiftable_kwh

    total_shifted_kwh = shiftable_kwh.sum()
    low_carbon_hours = low_carbon_mask.sum()
    if low_carbon_hours > 0:
        redistributed_kwh_per_hour = total_shifted_kwh / low_carbon_hours
        optimized_df.loc[low_carbon_mask, "optimized_load_kwh"] += redistributed_kwh_per_hour

    return optimized_df

