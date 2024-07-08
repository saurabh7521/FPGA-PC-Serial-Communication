import serial
import time
import threading
import tkinter as tk

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

# Function to receive and update the counters
def receive_and_update():
    global counter1, counter2
    while True:
        try:
            # Read exactly 2 bytes
            data = ser.read(2)
            if len(data) == 2:
                counter1 = data[0]
                counter2 = data[1]
                print(f"Received: Counter1 = {counter1}, Counter2 = {counter2}")

                # Update GUI
                update_gui()

        except serial.SerialException as e:
            print(f"Serial error: {e}")
            time.sleep(1)  # Wait before trying again
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)  # Wait before trying again

        #time.sleep(0.1)  # Small delay between reads

# Function to update the GUI
def update_gui():
    label_counter1.config(text=f"Counter 1: {counter1}")
    label_counter2.config(text=f"Counter 2: {counter2}")
    window.update_idletasks()  # Force update of the GUI

# Set up the GUI
window = tk.Tk()
window.geometry('500x200')
window.title("Counter Values")

label_counter1 = tk.Label(window, text="Counter 1: 0", font=("Helvetica", 16))
label_counter1.pack(pady=10)

label_counter2 = tk.Label(window, text="Counter 2: 0", font=("Helvetica", 16))
label_counter2.pack(pady=10)

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