import fastf1 as ff1
import pandas as pd
import matplotlib.pyplot as plt

# Enable cache
ff1.Cache.enable_cache('f1_cache')

# Get the schedule for the 2023 season
events_2023 = ff1.get_event_schedule(2023)

# Manually define the track lengths for 2023 races (in kilometers)
# Data obtained from official F1 sources or other reliable datasets
track_lengths = {
    'Bahrain Grand Prix': 5.412,
    'Saudi Arabian Grand Prix': 6.174,
    'Australian Grand Prix': 5.278,
    'Azerbaijan Grand Prix': 6.003,
    'Miami Grand Prix': 5.412,
    'Emilia Romagna Grand Prix': 4.909,
    'Monaco Grand Prix': 3.337,
    'Spanish Grand Prix': 4.675,
    'Canadian Grand Prix': 4.361,
    'Austrian Grand Prix': 4.318,
    'British Grand Prix': 5.891,
    'Hungarian Grand Prix': 4.381,
    'Belgian Grand Prix': 7.004,
    'Dutch Grand Prix': 4.259,
    'Italian Grand Prix': 5.793,
    'Singapore Grand Prix': 4.940,
    'Japanese Grand Prix': 5.807,
    'Qatar Grand Prix': 5.380,
    'United States Grand Prix': 5.513,
    'Mexico City Grand Prix': 4.304,
    'São Paulo Grand Prix': 4.309,
    'Las Vegas Grand Prix': 6.120,
    'Abu Dhabi Grand Prix': 5.281
}

# Initialize lists to store results
race_names = []
average_lap_times = []
lap_time_variabilities = []
average_speeds = []

# Loop through the events and compute the metrics
for event in events_2023.itertuples():
    race_name = event.EventName

    try:
        print(f"Analyzing lap data for {race_name}...")

        # Get track length from the dictionary
        track_length = track_lengths[race_name]

        # Load the race session
        race_session = ff1.get_session(2023, race_name, 'Race')
        race_session.load()

        # Access lap data
        laps = race_session.laps

        # Calculate average lap time in seconds
        avg_lap_time = laps['LapTime'].mean().total_seconds()

        # Calculate lap time variability (standard deviation)
        lap_time_variability = laps['LapTime'].std().total_seconds()

        # Calculate average speed using track length and average lap time (in km/h)
        avg_speed = (track_length / (avg_lap_time / 3600))

        # Append results to the lists
        race_names.append(race_name)
        average_lap_times.append(avg_lap_time)
        lap_time_variabilities.append(lap_time_variability)
        average_speeds.append(avg_speed)

    except Exception as e:
        print(f"Failed to analyze lap data for {race_name}: {e}")

# Create a DataFrame for easier analysis
difficulty_df = pd.DataFrame({
    'Race': race_names,
    'Average Lap Time (seconds)': average_lap_times,
    'Lap Time Variability (seconds)': lap_time_variabilities,
    'Average Speed (km/h)': average_speeds
})

# Display the DataFrame
print(difficulty_df)

# Visualization: Average Speed
plt.figure(figsize=(12, 6))
plt.bar(difficulty_df['Race'], difficulty_df['Average Speed (km/h)'], color='green')
plt.xlabel('Race')
plt.ylabel('Average Speed (km/h)')
plt.title('Average Speed by Race')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualization: Lap Time Variability
plt.figure(figsize=(12, 6))
plt.bar(difficulty_df['Race'], difficulty_df['Lap Time Variability (seconds)'], color='red')
plt.xlabel('Race')
plt.ylabel('Lap Time Variability (seconds)')
plt.title('Lap Time Variability by Race')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
