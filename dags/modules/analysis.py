import pandas as pd
import matplotlib.pyplot as plt

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    df['dt'] = pd.to_datetime(df['dt'])
    df['AverageTemperature'] = df['AverageTemperature'].fillna(df['AverageTemperature'].mean())
    df['AverageTemperatureUncertainty'] = df['AverageTemperatureUncertainty'].fillna(df['AverageTemperatureUncertainty'].mean())
    return df

def calculate_annual_global_avg(df):
    annual_avg = df.resample('Y', on='dt')['AverageTemperature'].mean().reset_index()
    return annual_avg

def save_visualization(annual_avg_temps, output_path):
    plt.figure(figsize=(10,5))
    plt.plot(annual_avg_temps['dt'], annual_avg_temps['AverageTemperature'], marker='o', linestyle='-')
    plt.title('Global Average Temperatures Over Time')
    plt.xlabel('Year')
    plt.ylabel('Average Temperature (°C)')
    plt.grid(True)
    plt.savefig(output_path)
