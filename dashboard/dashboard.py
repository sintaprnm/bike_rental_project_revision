import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset
day_data = pd.read_csv("day.csv")

# Convert dteday from object to datetime
day_data['dteday'] = pd.to_datetime(day_data['dteday'])

# Create function to summarize daily rentals based on temperature, humidity, and windspeed
def weather_effect_df(df):
    weather_effect = df.groupby('weathersit').agg({
        'cnt': 'mean',  # Average rentals
        'temp': 'mean',  # Average temperature
        'hum': 'mean',  # Average humidity
        'windspeed': 'mean'  # Average wind speed
    }).reset_index()
    return weather_effect

# Create function to analyze seasonal and weekday effects
def season_workingday_df(df):
    season_effect = df.groupby('season').agg({'cnt': 'mean'}).reset_index()
    workingday_effect = df.groupby('workingday').agg({'cnt': 'mean'}).reset_index()
    return season_effect, workingday_effect

# Apply functions
weather_effect = weather_effect_df(day_data)
season_effect, workingday_effect = season_workingday_df(day_data)

# Streamlit layout
st.title("Bike Rent Analysis Dashboard")

# Weather effect table
st.header("Effect of Weather on Rentals")
st.dataframe(weather_effect)
st.caption("This table summarizes the average bike rentals across different weather conditions, such as temperature, humidity, and wind speed. We will explore how these factors influence bike rentals in the following sections.")

# Plot: Rentals vs Temperature, Humidity, Wind Speed
st.subheader("Scatter Plots: Weather vs Rentals")
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
sns.scatterplot(data=day_data, x='temp', y='cnt', ax=ax[0])
ax[0].set_title("Rentals vs Temperature")
sns.scatterplot(data=day_data, x='hum', y='cnt', ax=ax[1])
ax[1].set_title("Rentals vs Humidity")
sns.scatterplot(data=day_data, x='windspeed', y='cnt', ax=ax[2])
ax[2].set_title("Rentals vs Wind Speed")
st.pyplot(fig)
st.caption("""
- **Rentals vs Temperature**: As the temperature rises, the number of bike rentals increases significantly. This trend shows a strong positive correlation between temperature and the comfort level for cycling. Warmer weather encourages people to rent bikes for both leisure and transportation, as outdoor activities become more enjoyable. This highlights the importance of focusing marketing efforts during warmer seasons to boost bike rentals.
  
- **Rentals vs Humidity**: Higher humidity is associated with a decline in bike rentals. As humidity rises, outdoor activities become more uncomfortable due to the heavy, sticky air, which discourages people from renting bikes. This suggests that business strategies during high-humidity periods should focus on promotions or incentives to overcome this barrier.
  
- **Rentals vs Wind Speed**: Wind speed, unlike temperature or humidity, has a minimal effect on the number of rentals. While extreme wind conditions might deter rentals, moderate wind does not significantly influence people's decisions to rent a bike. This indicates that users prioritize temperature and humidity more than wind speed when choosing to cycle.
""")

# Plot: Rentals by Season
st.header("Seasonal Analysis")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=season_effect, x='season', y='cnt', palette='coolwarm')
ax.set_title("Average Rentals by Season")
st.pyplot(fig)
st.caption("""
This plot shows how bike rentals fluctuate across different seasons. Summer and fall exhibit the highest average rentals. Warmer and more pleasant weather during these seasons likely encourages outdoor activities, including cycling. Summer in particular is known for vacations and outdoor adventures, making it a peak time for bike rentals.

In contrast, spring and winter show lower rental averages, which can be attributed to less favorable weather conditions. Cold temperatures and potential precipitation in winter make it less appealing for people to engage in outdoor activities like cycling. Thus, seasonal variations play a crucial role in determining rental demand, and rental businesses should anticipate lower demand during these periods.
""")

# Plot: Rentals by Working Day
st.header("Working Day Analysis")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=workingday_effect, x='workingday', y='cnt', palette='coolwarm')
ax.set_title("Average Rentals by Working Day")
st.pyplot(fig)
st.caption("""
The bar plot indicates that the number of rentals is higher on working days compared to non-working days. This trend suggests that many people use bikes for commuting and transportation purposes during weekdays. The steady demand on working days reflects the utility of bikes as a convenient and eco-friendly mode of transportation in urban settings.

On non-working days, the number of rentals slightly decreases, possibly because people engage in a variety of recreational activities, not all of which involve cycling. However, it is still essential for rental services to maintain adequate supply on weekends, as there remains a considerable amount of demand for leisure cycling.
""")
