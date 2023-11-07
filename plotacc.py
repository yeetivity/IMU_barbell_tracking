import json
import matplotlib.pyplot as plt
import os

from tkinter import Tk, filedialog

# Open file dialog
# file_path = "./6DOF_6peak.json"
# file_path = "./6DOF_6peak_sensorold.json"
# file_path = "./6DOF_horizontal_slide.json"
# file_path = "./6DOF_lying_still.json"
file_path = "./6DOF_gyrotest.json"

filepaths = ("./6DOF_gyrotest.json", "./6DOF_horizontal_slide.json", "./6DOF_lying_still.json", "./6DOF_6peak_sensorold.json", "./6DOF_6peak.json")

for file in filepaths:
  # Load accelerometer data
  with open(file) as f:
    data = json.load(f)

  ####################
  # plot acc
  ####################

  # Assuming your JSON structure contains 'x' and 'y' arrays, modify as needed
  x = data['accX']
  y = data['accY']
  z = data['accZ']

  max_value = max(max(x), max(y), max(z))
  min_value = min(min(x), min(y), min(z))

  # Create subplots
  fig, axs = plt.subplots(3)

  # Set the line color to red and increase y-axis size and range for each subplot
  axs[0].plot(x, color='red')
  axs[0].set_title('Acceleration x direction')
  axs[0].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
  axs[0].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
  axs[0].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting
  axs[0].set_ylim(min_value, max_value)

  axs[1].plot(y, color='blue')
  axs[1].set_title('Acceleration y direction')
  axs[1].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
  axs[1].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
  axs[1].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting
  axs[1].set_ylim(min_value, max_value)

  axs[2].plot(z, color='green')
  axs[2].set_title('Acceleration z direction')
  axs[2].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
  axs[2].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
  axs[2].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting
  axs[2].set_ylim(min_value, max_value)

  #####################
  # plot gyro
  #####################
  # Assuming the JSON structure contains magX, magY, magZ
  mx = data['magX']
  my = data['magY']
  mz = data['magZ']

  mMax_value = max(max(mx), max(my), max(mz))
  mMin_value = min(min(mx), min(my), min(mz))

  # Create subplots
  mfig, mAxs = plt.subplots(3)

  # Set the line color to red and increase y-axis size and range for each subplot
  mAxs[0].plot(mx, color='red')
  mAxs[0].set_title('Gyro x direction')
  mAxs[0].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
  mAxs[0].set_xlabel('', fontsize=10)  # X-axis label with smaller font size
  mAxs[0].set_ylabel('', fontsize=10)  # Y-axis label with LaTeX formatting
  mAxs[0].set_ylim(mMin_value, mMax_value)

  mAxs[1].plot(my, color='blue')
  mAxs[1].set_title('Gyro y direction')
  mAxs[1].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
  mAxs[1].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
  mAxs[1].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting
  mAxs[1].set_ylim(mMin_value, mMax_value)

  mAxs[2].plot(mz, color='green')
  mAxs[2].set_title('Gyro z direction')
  mAxs[2].tick_params(axis='both', labelsize=12)  # Increase both x and y-axis tick font size
  mAxs[2].set_xlabel('dT [1/52*s]', fontsize=10)  # X-axis label with smaller font size
  mAxs[2].set_ylabel('[$m/s^2$]', fontsize=10)  # Y-axis label with LaTeX formatting
  mAxs[2].set_ylim(mMin_value, mMax_value)

  savepath = os.path.splitext(os.path.basename(file))[0].replace("6DOF_","")

  # Save the figures
  fig.savefig("./analysis/" + savepath + "_acc.png")
  mfig.savefig("./analysis/" + savepath + "_gyro.png")