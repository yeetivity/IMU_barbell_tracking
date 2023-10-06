import json
import matplotlib.pyplot as plt

from tkinter import Tk, filedialog

# Open file dialog
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

root.destroy()
# Load accelerometer data
with open(file_path) as f:
  data = json.load(f)

# Assuming your JSON structure contains 'x' and 'y' arrays, modify as needed
x = data['accX']
y = data['accY']
z = data['accZ']

# Create subplots
fig, axs = plt.subplots(3)

# Set the line color to red and increase y-axis size and range for each subplot
axs[0].plot(x, color='red')
axs[0].set_title('Acceleration x direction')
axs[0].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
axs[0].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
axs[0].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting

axs[1].plot(y, color='blue')
axs[1].set_title('Acceleration y direction')
axs[1].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
axs[1].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
axs[1].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting

axs[2].plot(z, color='green')
axs[2].set_title('Acceleration z direction')
axs[2].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
axs[2].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
axs[2].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting

# Adjust layout and display the plot
plt.tight_layout()
plt.show()