import json
import math
from tkinter import Tk, filedialog
import numpy as np
#from ahrs import filters
import ahrs as ahrs
from ahrs.filters import Madgwick
from ahrs.filters import EKF
from ahrs.common.orientation import q2R, q2euler
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as Rr
from scipy import integrate as dx

# Removes the variance from the data
def compensatevariance(x):
    variance = np.var(x)
    # subtract each value in x with the variance
    compensatedvariance = [i - variance for i in x]
    return compensatedvariance

samplecount = 0
sampleFreq = 52
beta = 0.1

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
xgyro = data['magX']
ygyro = data['magY']
zgyro = data['magZ']
timestampsAcc = data['timeStampsAcc']
timestampsGyro = data['timeStampsGyro']


degToRad = math.pi / 180

print("TimeStampsAcc: ",timestampsAcc)
print("TimeStampsGyro: ",timestampsGyro)


print(len(y))
print(len(ygyro))
# Creating NumPy arrays for acceleration and gyro values
acceleration_values = np.array([x, y, z]).T
gyro_values = np.array([xgyro, ygyro, zgyro]).T

print(len(acceleration_values))
print(len(gyro_values))

plt.plot(xgyro, label = 'xGyro')
plt.plot(ygyro, label = 'yGyro')
plt.plot(zgyro, label = 'zGyro')
plt.show()
#print(gyro_values)

#print(gyro_values.shape)

#if len(gyro_values) != len(acceleration_values):
#    raise ValueError("gyro_values and acceleration_values arrays must have the same length")

#ekf = EKF()

ekf = EKF(gyr=gyro_values, acc=acceleration_values, frequency=sampleFreq)

# Convert quaternion to rotation matrix
R = np.array([q2R(q) for q in ekf.Q]) 

# Or convert to Euler angles
euler = np.array([q2euler(q) for q in ekf.Q])

# Rotate raw accelerometer data
acc_global = np.array([R[i] @ acceleration_values[i] for i in range(len(acceleration_values))])

# Rotate raw gyroscope data 
gyro_global = np.array([R[i] @ gyro_values[i] for i in range(len(gyro_values))])




Q = ekf.Q
n_samples = acceleration_values.shape[0]
new_acce = np.zeros((n_samples, 3))
totalacc = np.zeros(n_samples)
# Initializing Array to hold the Linear acceleration Vector


for t in range(n_samples):
    r = Rr.from_quat(Q[t])
    
    
    # Getting a Rotation Matrix from the Quaternions
    new_acce[t] = np.matmul(r.as_matrix().T,acceleration_values[t])
    
    # matmul Rotation Matrix Transpose to orignal Acceleration to produce the clean linear acceleration
    if(new_acce[t, 2] != 0):
        totalacc[t] = math.sqrt(new_acce[t, 0]**2 + new_acce[t, 1]**2 + new_acce[t, 2]**2)-9.82
    

plt.plot(totalacc)
plt.show()

# Create a figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot rotated X-axis acceleration data
ax1.plot(new_acce[:, 0], label='Rotated X')
ax1.plot(new_acce[:, 1], label='Rotated Y')
ax1.plot(new_acce[:, 2], label='Rotated Z')
ax1.set_ylabel('Acceleration (m/s^2)')
ax1.legend()
ax1.grid(True)

# Plot raw X-axis acceleration data as a subplot
ax2.plot(acceleration_values[:, 0], color='orange', label='Raw X')
ax2.plot(acceleration_values[:, 1], color='green', label='Raw Y')
ax2.plot(acceleration_values[:, 2], color='blue', label='Raw Z')
ax2.set_xlabel('Sample Index')
ax2.set_ylabel('Acceleration (m/s^2)')
ax2.legend()
ax2.grid(True)

# Set the title for the entire subplot
plt.suptitle('Acceleration Data Comparison')
plt.show()

# Calculate time between samples (time step)
time_step = 1 / sampleFreq  # Assuming sampleFreq is in Hz

# Integrate acceleration using the trapezoidal rule to get velocity
velocityx = dx.cumtrapz(new_acce[:, 0], dx=time_step) 
velocityy = dx.cumtrapz(new_acce[:, 1], dx=time_step) 
velocityz = dx.cumtrapz(new_acce[:, 2], dx=time_step)

# Plot the calculated velocity
plt.figure(figsize=(10, 6))
plt.plot(velocityx, color='red', label='Xvel')
plt.plot(velocityy, color='green', label='Yvel')
plt.plot(velocityz, color = 'blue', label = 'Zvel')
plt.title('Calculated Velocity (X-axis)')
plt.xlabel('Sample Index')
plt.ylabel('Velocity (m/s)')
plt.grid(True)
plt.show()

velocitytot = dx.cumtrapz(totalacc, dx=time_step)

plt.plot(velocitytot)
plt.show()

# q: why do i get this error: 'Madgwick' object has no attribute 'Q'?
#madgwick = Madgwick(gyr=gyro_values, acc=acceleration_values, frequency=sampleFreq)

#shape = madgwick.Q.shape

#type(madgwick.Q), madgwick.Q.shape 


#x = compensatevariance(x)
#y = compensatevariance(y)
#z = compensatevariance(z)

def zeroVelocityUpdate(x, y, z, xgyro, ygyro, zgyro):
    """
    Check if any of the values in x, y, z, xgyro, ygyro, zgyro are above the threshold value.
    """
    threshacc = 0.2
    threshgyro = 0.1
    if (all(abs(val) > threshacc for val in x) and
            all(abs(val) > threshacc for val in y) and
            all(abs(val) > threshacc for val in z) and
            all(abs(val) > threshgyro for val in xgyro) and
            all(abs(val) > threshgyro for val in ygyro) and
            all(abs(val) > threshgyro for val in zgyro)):
        samplecount = samplecount + 1
    else:
        samplecount = 0
    return (samplecount >= 10)       

