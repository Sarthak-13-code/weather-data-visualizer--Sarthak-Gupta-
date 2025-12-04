# weather_analysis.py
#
# Mini Project: Weather Data Visualizer
# This script:
# 1) Loads a CSV file with weather data
# 2) Cleans and processes the data
# 3) Calculates daily, monthly, yearly statistics using NumPy + Pandas
# 4) Creates different plots with Matplotlib
# 5) Groups data by month and season
# 6) Exports cleaned data, plots, and a summary report

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Task 1: Data Acquisition and Loading
# -----------------------------
def load_weather_data(filepath):
    """
    Load the CSV file into a Pandas DataFrame and
    print basic info (head, info, describe).
    """
    print("🔹 Task 1: Loading data from:", filepath)

    df = pd.read_csv(filepath)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nInfo:")
    print(df.info())

    print("\nDescribe:")
    print(df.describe())

    return df


# -----------------------------
# Task 2: Data Cleaning and Processing
# -----------------------------
def clean_weather_data(df):
    """
    - Handle missing values
    - Convert Date column to datetime
    - Keep only relevant columns: Date, Temperature, Rainfall, Humidity
    """
    print("\n🔹 Task 2: Cleaning data")

    # Rename columns if needed (optional helper)
    # df = df.rename(columns={"temp": "Temperature", "rain": "Rainfall", "hum": "Humidity"})

    # Drop completely empty rows
    df = df.dropna(how="all")

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # Keep only relevant columns if they exist
    cols = ["Date", "Temperature", "Rainfall", "Humidity"]
    df = df[[c for c in cols if c in df.columns]]

    # Fill missing numeric values with column mean
    for col in ["Temperature", "Rainfall", "Humidity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            mean_value = df[col].mean()
            df[col] = df[col].fillna(mean_value)

    print("✅ Cleaning done. Data shape:", df.shape)
    return df


# -----------------------------
# Task 3: Statistical Analysis with NumPy
# -----------------------------
def compute_statistics(df):
    """
    Compute daily, monthly, yearly stats using NumPy + groupby.
    Returns dictionaries / DataFrames with stats.
    """
    print("\n🔹 Task 3: Computing statistics")

    # Make sure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")

    stats_result = {}

    # DAILY STATS (group by each date)
    daily = df.resample("D").mean()  # mean of each day
    stats_result["daily"] = daily

    # MONTHLY STATS
    monthly = df.resample("M").agg(["mean", "min", "max", "std"])
    stats_result["monthly"] = monthly

    # YEARLY STATS
    yearly = df.resample("Y").agg(["mean", "min", "max", "std"])
    stats_result["yearly"] = yearly

    print("✅ Statistics computed.")
    return stats_result


# -----------------------------
# Task 4: Visualization with Matplotlib
# -----------------------------
def plot_daily_temperature(df, output_folder="output"):
    print("\n🔹 Task 4: Plotting daily temperature trend")

    os.makedirs(output_folder, exist_ok=True)

    df_temp = df.set_index("Date").resample("D").mean()

    plt.figure(figsize=(8, 4))
    plt.plot(df_temp.index, df_temp["Temperature"])
    plt.title("Daily Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    filepath = os.path.join(output_folder, "temp_trend.png")
    plt.savefig(filepath)
    plt.close()
    print("✅ Saved:", filepath)


def plot_monthly_rainfall(df, output_folder="output"):
    print("\n🔹 Task 4: Plotting monthly rainfall totals")

    os.makedirs(output_folder, exist_ok=True)

    df_monthly = df.set_index("Date").resample("M")["Rainfall"].sum()

    plt.figure(figsize=(8, 4))
    plt.bar(df_monthly.index.strftime("%Y-%m"), df_monthly.values)
    plt.title("Monthly Rainfall Total")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    filepath = os.path.join(output_folder, "monthly_rainfall.png")
    plt.savefig(filepath)
    plt.close()
    print("✅ Saved:", filepath)


def plot_humidity_vs_temperature(df, output_folder="output"):
    print("\n🔹 Task 4: Plotting humidity vs temperature (scatter)")

    os.makedirs(output_folder, exist_ok=True)

    plt.figure(figsize=(6, 4))
    plt.scatter(df["Temperature"], df["Humidity"])
    plt.title("Humidity vs Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.tight_layout()
    filepath = os.path.join(output_folder, "humidity_vs_temperature.png")
    plt.savefig(filepath)
    plt.close()
    print("✅ Saved:", filepath)


def plot_combined_figure(df, output_folder="output"):
    """
    Combine at least two plots in a single figure (subplots).
    """
    print("\n🔹 Task 4: Creating combined plots figure")

    os.makedirs(output_folder, exist_ok=True)

    df_daily = df.set_index("Date").resample("D").mean()
    df_monthly = df.set_index("Date").resample("M")["Rainfall"].sum()

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Left: Temperature line
    axes[0].plot(df_daily.index, df_daily["Temperature"])
    axes[0].set_title("Daily Temperature")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Temperature (°C)")

    # Right: Rainfall bar
    axes[1].bar(df_monthly.index.strftime("%Y-%m"), df_monthly.values)
    axes[1].set_title("Monthly Rainfall")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Rainfall (mm)")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    filepath = os.path.join(output_folder, "combined_plots.png")
    plt.savefig(filepath)
    plt.close()
    print("✅ Saved:", filepath)


# -----------------------------
# Task 5: Grouping and Aggregation
# -----------------------------
def add_season_column(df):
    """
    Add a Season column based on month.
    (You can adjust seasons if you want.)
    """
    def month_to_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    df["Month"] = df["Date"].dt.month
    df["Season"] = df["Month"].apply(month_to_season)
    return df


def group_by_month_and_season(df):
    """
    Group data by month and season and calculate basic stats.
    """
    print("\n🔹 Task 5: Grouping by month and season")

    df = add_season_column(df.copy())

    # Monthly average temperature and total rainfall
    monthly_stats = df.groupby("Month").agg({
        "Temperature": "mean",
        "Rainfall": "sum",
        "Humidity": "mean"
    })

    # Seasonal stats
    season_stats = df.groupby("Season").agg({
        "Temperature": "mean",
        "Rainfall": "sum",
        "Humidity": "mean"
    })

    print("\nMonthly stats:")
    print(monthly_stats)

    print("\nSeasonal stats:")
    print(season_stats)

    return monthly_stats, season_stats


# -----------------------------
# Task 6: Export and Storytelling
# -----------------------------
def export_cleaned_data(df, output_folder="output"):
    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, "cleaned_weather_data.csv")
    df.to_csv(filepath, index=False)
    print("\n🔹 Task 6: Exported cleaned data to:", filepath)


def write_summary_report(df, stats, monthly_stats, season_stats,
                        output_folder="output"):
    """
    Write a simple text report that describes trends and anomalies.
    """
    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, "summary_report.txt")

    # Some simple insights
    avg_temp = df["Temperature"].mean()
    max_temp = df["Temperature"].max()
    min_temp = df["Temperature"].min()

    total_rainfall = df["Rainfall"].sum()
    max_rain_day = df.loc[df["Rainfall"].idxmax(), "Date"]

    with open(filepath, "w") as f:
        f.write("Weather Data Summary Report\n")
        f.write("---------------------------\n\n")
        f.write(f"Average temperature: {avg_temp:.2f} °C\n")
        f.write(f"Highest temperature: {max_temp:.2f} °C\n")
        f.write(f"Lowest temperature: {min_temp:.2f} °C\n\n")

        f.write(f"Total rainfall: {total_rainfall:.2f} mm\n")
        f.write(f"Day with highest rainfall: {max_rain_day.date()}\n\n")

        f.write("Monthly overview (Temperature mean, Rainfall sum, Humidity mean):\n")
        f.write(str(monthly_stats))
        f.write("\n\nSeasonal overview:\n")
        f.write(str(season_stats))
        f.write("\n\nObservations:\n")
        f.write("- Temperatures and rainfall vary between months and seasons.\n")
        f.write("- Look for months with unusually high rainfall or temperature spikes.\n")
        f.write("- This information can help with planning and climate awareness.\n")

    print("🔹 Task 6: Summary report saved to:", filepath)


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():
    # Path to the weather CSV
    data_path = os.path.join("data", "weather.csv")

    # Task 1: Load data
    df = load_weather_data(data_path)

    # Task 2: Clean data
    df = clean_weather_data(df)

    # Task 3: Statistics
    stats = compute_statistics(df)

    # Reset index to have Date as a column again for later functions
    df = df.reset_index(drop=True)

    # Task 4: Plots
    plot_daily_temperature(df)
    plot_monthly_rainfall(df)
    plot_humidity_vs_temperature(df)
    plot_combined_figure(df)

    # Task 5: Grouping & Aggregation
    monthly_stats, season_stats = group_by_month_and_season(df)

    # Task 6: Export & Storytelling
    export_cleaned_data(df)
    write_summary_report(df, stats, monthly_stats, season_stats)

    print("\n✅ Weather data pipeline completed successfully!")


if __name__ == "__main__":
    main()
