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
velocity = data
fig, axs = plt.subplots(1)
axs.plot(velocity)

plt.tight_layout()
plt.show()