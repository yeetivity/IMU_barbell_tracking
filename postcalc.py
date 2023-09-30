import json
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
print(resultx)

