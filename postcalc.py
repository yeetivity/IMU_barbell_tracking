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
#z = data['accZ']

plt.subplot(2, 1, 1)
plt.plot(x, label='Raw Acceleration X')
plt.ylabel('Acceleration (m/s^2)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(y, label='Raw Acceleration Y') 
plt.xlabel('Time Steps')
plt.ylabel('Acceleration (m/s^2)')
plt.legend()

plt.tight_layout()
plt.show()

dT = 1/52 # sampling frequency
time = len(x)*dT # total duration of the data, assuming the data is sampled at 1/52Hz, i.e. 52Hz

#sliding window function that takes a certain window size and returns a vector containing averages
def sliding_window(elements, window_size):
    result = []
    if len(elements) <= window_size:
        return elements
    for i in range(len(elements) - window_size + 1):
        window = elements[i:i+window_size]
        window_mean = round(sum(window) / window_size, 3)  # Round to 3 decimal places
        result.append(window_mean)
    return result

#resultx = sliding_window(x, 10)
#resulty = sliding_window(y, 10)
#resultz = sliding_window(z, 10)

# Set up Kalman filter (2D x,y (not z!!))
dt = 1/52 # sample time
u_x = 0 # assuming zero acceleration
u_y = 0
std_acc = 0.1 # tune this
x_std_meas = 0.01 # tune this
y_std_meas = 0.01 # tune this

#initiates the kalman filter
kf = KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)

x_filtered = []
y_filtered = []

# Make x and y 1D arrays (maybe not needed)
x = np.squeeze(x)
y = np.squeeze(y)

# Kalman filtering loop
for i in range(len(x)):
    # Predict  
    x_est = kf.predict()
    
    # Update
    state = kf.update(np.array([[x[i]], [y[i]]]))
    
    # Extract x and y   
    x_filtered.append(state[0, 0])
    y_filtered.append(state[1, 0])

#kalman filters are defined for linear systems
# Filter each axis
  
# Plot filtered vs raw data  
plt.plot(x, label='x raw')
plt.plot(x_filtered, label='x filtered')
plt.plot(y, label='y raw')
plt.plot(y_filtered, label='y filtered')
plt.legend()
plt.show()

#filtered_y = y
g = 9.82

def calcStartAngle(yAcc, g):
    
    # Calculate the average of the first 10 values in yAcc
    avg_yAcc = np.mean(yAcc[:10])
    print(avg_yAcc)
    
    startangle = np.arccos(avg_yAcc/-g) * 180 / np.pi
    print(startangle)
    
    if (startangle < 0):
        startangle = startangle + 180
    else:
        startangle = startangle - 180
    
    print(startangle)
    return startangle

startangle = calcStartAngle(y_filtered, g)
threshold = 0.5

#takes a acceleration vector and loop index as input 
def detect_turning_point(acc, i):

    if i == 0: 
        return False
    
    pos_to_neg = acc[i-1] > 0 and acc[i] < 0
    neg_to_pos = acc[i-1] < 0 and acc[i] > 0
    
    if pos_to_neg or neg_to_pos:
        return True
    
    else:
        return False    
 
#checks if the device is moving
def checkmovement(i):
    if ((x_filtered[i] > threshold or x_filtered[i] < -threshold) and (y_filtered[i] > threshold or y_filtered[i] < -threshold)):
        return True
    else:
        return False

# Calculate velocity from filtered acceleration data using numerical integration
def integrate_acceleration(filtered_acceleration, dt):
    velocity = [0]  # Initial velocity is 0
    for i in range(1, len(filtered_acceleration)):
        
        if (filtered_acceleration[i] > threshold or filtered_acceleration[i]<-threshold):    
            # Use trapezoidal rule for numerical integration
            delta_velocity = (filtered_acceleration[i] + filtered_acceleration[i - 1]) / 2 * dt

            # Adjust velocity based on the sign of acceleration
            if filtered_acceleration[i] > 0:
                velocity.append(velocity[-1] + delta_velocity)
            else:
                velocity.append(velocity[-1] + delta_velocity)
    return velocity

# Assuming dt is the sampling time (which is 1/52 in your case)
sampling_time = 1/52

# Calculate velocity for filtered x and y acceleration data

velocity_x = integrate_acceleration(x_filtered, sampling_time)
velocity_y = integrate_acceleration(y_filtered, sampling_time)

# Now, velocity_x and velocity_y contain the calculated velocities from filtered x and y acceleration data respectively

# Plot velocity x and y
plt.subplot(2, 1, 1)
plt.plot(velocity_x, label='Velocity X')
plt.ylabel('Velocity (m/s)')
plt.legend()

plt.subplot(2, 1, 2)  
plt.plot(velocity_y, label='Velocity Y')
plt.xlabel('Time Steps')
plt.ylabel('Velocity (m/s)') 
plt.legend()

plt.tight_layout()
plt.show()
# Plot raw acceleration 