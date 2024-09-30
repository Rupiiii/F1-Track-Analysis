import fastf1 as ff1
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib as mpl

# Enable cache
ff1.Cache.enable_cache('f1_cache')

# Define a colormap
colormap = mpl.cm.plasma

# Get the schedule for the 2023 season
events_2023 = ff1.get_event_schedule(2023)

# Define a driver whose fastest lap data will be used for the speed heatmap
driver = 'VER'  # Max Verstappen, you can change this to any driver you'd like

# Loop through the races in 2023
for event in events_2023.itertuples():
    race_name = event.EventName
    year = 2023
    session_name = 'Race'
    
    try:
        print(f"Generating heatmap for {race_name}...")

        # Load the race session for the current event
        race_session = ff1.get_session(year, race_name, session_name)
        race_session.load()

        # Select the fastest lap for the chosen driver
        lap = race_session.laps.pick_driver(driver).pick_fastest()

        # Get telemetry data
        x = lap.telemetry['X']              # values for x-axis (track position)
        y = lap.telemetry['Y']              # values for y-axis (track position)
        color = lap.telemetry['Speed']      # value to base color gradient on (speed)

        # Create a set of line segments so that we can color them individually
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Plot the data
        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        
        # Set background colors
        fig.patch.set_facecolor('black')  # Set figure background to black
        ax.set_facecolor('black')          # Set axes background to black
        
        # Set title color
        fig.suptitle(f'{race_name} {year} - {driver} - Speed', size=24, y=0.97, color='white')

        # Adjust margins and turn off axis
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis('off')

        # Create background track line
        ax.plot(x, y, color='black', linestyle='-', linewidth=16, zorder=0)

        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(color.min(), color.max())
        lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

        # Set the values used for colormapping
        lc.set_array(color)

        # Merge all line segments together
        line = ax.add_collection(lc)

        # Add a color bar as a legend
        cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
        legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")
        
        # Change color of color bar labels to white
        legend.ax.yaxis.set_tick_params(color='white')
        legend.ax.xaxis.set_tick_params(color='white')
        legend.ax.set_ylabel('Speed (mph)', color='white')

        # Show the color bar text in white
        for label in legend.ax.get_xticklabels() + legend.ax.get_yticklabels():
            label.set_color('white')

        # Save the plot for each track
        plt.savefig(f"{race_name}_Speed_Heatmap.png")
        plt.show()

    except Exception as e:
        print(f"Failed to generate heatmap for {race_name}: {e}")
