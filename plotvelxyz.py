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
x = data['xVel']
y = data['yVel']
z = data['zVel']

fig, axs = plt.subplots(3)
axs[0].plot(x)
axs[0].set_title('Vel X')
axs[1].plot(y)
axs[1].set_title('Vel Y')
axs[2].plot(z)
axs[2].set_title('Vel Z')

plt.tight_layout()
plt.show()