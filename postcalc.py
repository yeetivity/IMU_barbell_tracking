import json
from tkinter import Tk, filedialog
from kalmanFilter import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt

# Open file dialog to choose acceleration file (.json)
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

dT = 1/52 # sampling frequency
time = len(x)*dT # total duration of the data, assuming the data is sampled at 1/52Hz, i.e. 52Hz

#sliding window function
def sliding_window(elements, window_size):
    result = []
    if len(elements) <= window_size:
        return elements
    for i in range(len(elements) - window_size + 1):
        window = elements[i:i+window_size]
        window_mean = round(sum(window) / window_size, 3)  # Round to 3 decimal places
        result.append(window_mean)
    return result

resultx = sliding_window(x, 10)
resulty = sliding_window(y, 10)
resultz = sliding_window(z, 10)

# Set up Kalman filter (2D x,y (not z!!))
dt = 1/52 # sampling time
u_x = 0 # assuming zero acceleration
u_y = 0
std_acc = 0.1 # tune this
x_std_meas = 0.5 # tune this
y_std_meas = 0.5 # tune this

self = None

kf = KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)

# Filter each axis
filtered_x = []
for x_meas in resultx:
  x = kf.update(np.matrix([[x_meas]]))
  filtered_x.append(x[0,0])

filtered_y = []  
for y_meas in resulty:
  y = kf.update(np.matrix([[y_meas]]))
  filtered_y.append(y[1,0])

g = 9.82

def calcStartAngle(yAcc, g):
    
    # Calculate the average of the first 5 values in yAcc
    avg_yAcc = np.mean(yAcc[:5])

    startangle = np.arccos(avg_yAcc/-g) * 180 / np.pi
    print(startangle)
    
    if (startangle < 0):
        startangle = startangle + 180
    else:
        startangle = startangle - 180
    
    print(startangle)
    return startangle

startangle = calcStartAngle(filtered_y, g)
 
#checks if the device is moving
def checkmovement(i):
    if ((filtered_x[i] > 0.1 or filtered_x[i] < -0.1) and (filtered_y[i] > 0.1 or filtered_y[i] < -0.1)):
        return True
    else:
        return False

# Calculate velocity from filtered acceleration data using numerical integration
def integrate_acceleration(filtered_acceleration, dt):
    velocity = [0]  # Initial velocity is 0
    for i in range(1, len(filtered_acceleration)):
        if (checkmovement(i)):
            velocity.append(0)
        else:
            # Use trapezoidal rule for numerical integration
            delta_velocity = (filtered_acceleration[i] + filtered_acceleration[i - 1]) / 2 * dt
            velocity.append(velocity[-1] + delta_velocity)
    return velocity

# Assuming dt is the sampling time (which is 1/52 in your case)
sampling_time = 1/52

# Calculate velocity for filtered x and y acceleration data
velocity_x = integrate_acceleration(filtered_x, sampling_time)
velocity_y = integrate_acceleration(filtered_y, sampling_time)

# Now, velocity_x and velocity_y contain the calculated velocities from filtered x and y acceleration data respectively

# Plot the velocities
plt.figure(figsize=(10, 6))
plt.plot(velocity_x, label='Velocity X')
plt.plot(velocity_y, label='Velocity Y')
plt.xlabel('Time Steps')
plt.ylabel('Velocity')
plt.title('Velocity Calculated from Filtered Acceleration Data')
plt.legend()
plt.grid(True)
plt.show()