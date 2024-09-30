import fastf1 as ff1

# Enable cache
ff1.Cache.enable_cache('f1_cache')

# Get a list of all races in the 2023 season
events_2023 = ff1.get_event_schedule(2023)

# Loop through each event in the 2023 season
for event in events_2023.itertuples():
    race_name = event.EventName
    try:
        print(f"Fetching lap data for {race_name}...")

        # Load the race session
        race_session = ff1.get_session(2023, race_name, 'Race')
        race_session.load()

        # Access lap data for all drivers
        laps = race_session.laps

        # Display the first few rows of lap data to verify
        print(f"Lap data for {race_name}:")
        print(laps.head())
        print("\n" + "="*60 + "\n")  # Separator between races

    except Exception as e:
        print(f"Failed to fetch lap data for {race_name}: {e}")
