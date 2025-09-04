# Import Meteostat library and dependencies
import calendar
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Normals, Stations, Point, Daily



stations = Stations()
# Santa Fe coordinates: 35.6870° N, 105.9378° W
stations = stations.nearby(35.6870, -105.9378)
station = stations.fetch(1)

print(station)

data = Normals(station)
data = data.fetch()

# Convert temperature columns from Celsius to Fahrenheit
data['tavg'] = (data['tavg'] * 9/5) + 32
data['tmin'] = (data['tmin'] * 9/5) + 32
data['tmax'] = (data['tmax'] * 9/5) + 32

print(data)
# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax'])

# Set the X-axis labels to month names
plt.xticks(
    range(12), # There are 12 months, so ticks from 1 to 12
    [calendar.month_abbr[i] for i in range(1, 13)] # Get abbreviated month names
)

# Add a title
plt.title('Monthly Temperature Normals in Santa Fe (1991-2020)')

# Add Y-axis label
plt.ylabel('Temperature (°C)')

# Add X-axis label
plt.xlabel('Month')

# Save the figure to a file
plt.savefig('SantaFe.png', dpi=600, bbox_inches='tight')
print("Plot saved to SantaFe.png")
