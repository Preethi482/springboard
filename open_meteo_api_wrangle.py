# ==============================================================
# 🌤️ API Data Wrangling with Open-Meteo
# Data Science Career Track | Mini Project
# Author: Your Name
# ==============================================================

# Install required packages (uncomment if running locally)
# !pip install requests pandas matplotlib --quiet

# --- Import Libraries ---
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configure matplotlib for inline display (Jupyter)
%matplotlib inline

# ==============================================================
# Step 1: Set Up Parameters
# ==============================================================

latitude = 40.7128  # New York City
longitude = -74.0060

start_date = '2023-01-01'
end_date = '2023-01-07'  # One week of data

hourly_variables = ['temperature_2m', 'relativehumidity_2m', 'precipitation']

base_url = 'https://archive-api.open-meteo.com/v1/archive'
params = {
    'latitude': latitude,
    'longitude': longitude,
    'start_date': start_date,
    'end_date': end_date,
    'hourly': ','.join(hourly_variables),
    'timezone': 'America/New_York'
}

# ==============================================================
# Step 2: Make the API Request
# ==============================================================

response = requests.get(base_url, params=params)

if response.status_code == 200:
    print('✅ Data fetched successfully!')
else:
    raise Exception(f'Failed to fetch data. Status code: {response.status_code}')

# ==============================================================
# Step 3: Load Data into pandas DataFrame
# ==============================================================

data = response.json()
hourly_data = data['hourly']
df = pd.DataFrame(hourly_data)

print("Data preview:")
df.head()

# ==============================================================
# Step 4: Data Cleaning
# ==============================================================

df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

df.ffill(inplace=True)  # Modern replacement for fillna(method='ffill')

print("Missing values per column:")
print(df.isnull().sum())

# ==============================================================
# Step 5: Exploratory Data Analysis
# ==============================================================

print("Summary statistics:")
print(df.describe())

# --- Plot Temperature Over Time ---
plt.figure(figsize=(14, 6))
plt.plot(df.index, df['temperature_2m'], label='Temperature (°C)')
plt.title('Temperature Over Time in New York City')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.show()

# --- Plot Relative Humidity Over Time ---
plt.figure(figsize=(14, 6))
plt.plot(df.index, df['relativehumidity_2m'], color='orange', label='Relative Humidity (%)')
plt.title('Relative Humidity Over Time in New York City')
plt.xlabel('Date')
plt.ylabel('Relative Humidity (%)')
plt.legend()
plt.show()

# --- Plot Precipitation Over Time ---
plt.figure(figsize=(14, 6))
plt.bar(df.index, df['precipitation'], label='Precipitation (mm)')
plt.title('Precipitation Over Time in New York City')
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.legend()
plt.show()

# ==============================================================
# Step 6: Correlation Analysis
# ==============================================================

correlation = df['temperature_2m'].corr(df['relativehumidity_2m'])
print(f'Correlation between Temperature and Relative Humidity: {correlation:.2f}')

plt.figure(figsize=(8, 6))
plt.scatter(df['temperature_2m'], df['relativehumidity_2m'], alpha=0.5)
plt.title('Temperature vs. Relative Humidity')
plt.xlabel('Temperature (°C)')
plt.ylabel('Relative Humidity (%)')
plt.show()

# ==============================================================
# Step 7: Resample Data to Daily Averages
# ==============================================================

daily_avg = df.resample('D').mean()
print(daily_avg.head())

plt.figure(figsize=(10, 5))
plt.plot(daily_avg.index, daily_avg['temperature_2m'], marker='o')
plt.title('Daily Average Temperature in New York City')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.show()

# ==============================================================
# Step 8: Compare with Another Location (Los Angeles)
# ==============================================================

latitude_la = 34.0522
longitude_la = -118.2437

params_la = {
    'latitude': latitude_la,
    'longitude': longitude_la,
    'start_date': start_date,
    'end_date': end_date,
    'hourly': ','.join(hourly_variables),
    'timezone': 'America/Los_Angeles'
}

response_la = requests.get(base_url, params=params_la)

data_la = response_la.json()
hourly_data_la = data_la['hourly']
df_la = pd.DataFrame(hourly_data_la)

df_la['time'] = pd.to_datetime(df_la['time'])
df_la.set_index('time', inplace=True)
df_la.ffill(inplace=True)

daily_avg_la = df_la.resample('D').mean()

# --- Combine DataFrames for Comparison ---
combined_temp = pd.DataFrame({
    'New York': daily_avg['temperature_2m'],
    'Los Angeles': daily_avg_la['temperature_2m']
})

combined_temp.plot(kind='bar', figsize=(10, 6))
plt.title('Daily Average Temperature: New York vs Los Angeles')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# ==============================================================
# Step 9: Advanced Analysis - Temperature Difference
# ==============================================================

combined_temp['Temp Difference'] = combined_temp['Los Angeles'] - combined_temp['New York']
print(combined_temp)

# ==============================================================
# Step 10: Save Data to CSV (Optional)
# ==============================================================

df.to_csv('new_york_weather.csv')
df_la.to_csv('los_angeles_weather.csv')

print("✅ Data saved to CSV files successfully.")

# ==============================================================
# Step 11: Conclusion
# ==============================================================

print("""
Conclusion:
- Successfully accessed and cleaned Open-Meteo weather data.
- Performed EDA and visualization for NYC and LA.
- Compared temperature patterns and computed differences.
- Next steps: Extend date range, add new variables, and forecast trends.
""")
