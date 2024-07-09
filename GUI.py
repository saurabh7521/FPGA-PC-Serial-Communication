import serial
import time
import threading
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure the serial connection
ser = serial.Serial(
    port='COM5',  # Replace with your COM port
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# Global variables for counter values
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0

# Data lists for plotting
data1 = []
data2 = []
data3 = []
data4 = []

# Function to receive and update the counters
def receive_and_update():
    global counter1, counter2, counter3, counter4
    while True:
        try:
            # Read exactly 12 bytes (3 bytes for each counter)
            data = ser.read(12)
            if len(data) == 12:
                counter1 = (data[2] << 16) | (data[1] << 8) | data[0]
                counter2 = (data[5] << 16) | (data[4] << 8) | data[3]
                counter3 = (data[8] << 16) | (data[7] << 8) | data[6]
                counter4 = (data[11] << 16) | (data[10] << 8) | data[9]
                print(f"Received: Counter1 = {counter1}, Counter2 = {counter2}, Counter3 = {counter3}, Counter4 = {counter4}")

                # Update GUI and plot
                update_gui()
                update_plot()

        except serial.SerialException as e:
            print(f"Serial error: {e}")
            time.sleep(1)  # Wait before trying again
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)  # Wait before trying again

        # Small delay between reads
        time.sleep(0.1)

# Function to update the GUI
def update_gui():
    label_counter1.config(text=f"Counter 1: {counter1}")
    label_counter2.config(text=f"Counter 2: {counter2}")
    label_counter3.config(text=f"Counter 3: {counter3}")
    label_counter4.config(text=f"Counter 4: {counter4}")
    window.update_idletasks()  # Force update of the GUI

# Function to update the plot
def update_plot():
    data1.append(counter1 / 1000)
    data2.append(counter2 / 1000)
    data3.append(counter3 / 1000)
    data4.append(counter4 / 1000)

    if len(data1) > 50:  # Keep the data lists to a manageable size
        data1.pop(0)
        data2.pop(0)
        data3.pop(0)
        data4.pop(0)

    ax.clear()
    ax.plot(data1, label='Counter 1')
    ax.plot(data2, label='Counter 2')
    ax.plot(data3, label='Counter 3')
    ax.plot(data4, label='Counter 4')
    ax.legend()
    ax.set_ylabel('Counter Values (in 1000s)')
    ax.set_title('Real-time Counter Values')
    canvas.draw()

# Set up the GUI
window = tk.Tk()
window.geometry('800x400')
window.title("Counter Values")

# Labels for displaying counters
label_counter1 = tk.Label(window, text="Counter 1: 0", font=("Helvetica", 16))
label_counter1.pack(pady=5)

label_counter2 = tk.Label(window, text="Counter 2: 0", font=("Helvetica", 16))
label_counter2.pack(pady=5)

label_counter3 = tk.Label(window, text="Counter 3: 0", font=("Helvetica", 16))
label_counter3.pack(pady=5)

label_counter4 = tk.Label(window, text="Counter 4: 0", font=("Helvetica", 16))
label_counter4.pack(pady=5)

# Matplotlib figure and axis
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

# Start the receiving function in a background thread
receiver_thread = threading.Thread(target=receive_and_update, daemon=True)
receiver_thread.start()

# Function to close the application
def on_closing():
    ser.close()
    window.quit()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
window.mainloop()