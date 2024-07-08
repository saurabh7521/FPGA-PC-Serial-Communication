import serial
import time
import threading

# Configure the serial connection
ser = serial.Serial(
    port='COM5',  # Replace with your COM port
    baudrate=9600,  # Baud rate
    timeout=1  # Read timeout
)

# Function to receive and display the number
def receive_and_display():
    while True:
        # Clear the input buffer to discard all old data
        ser.reset_input_buffer()

        # Read the latest data point
        received_data = ser.read(1)
        if received_data:
            # Convert the byte to an integer
            number = int.from_bytes(received_data, byteorder='big')
            print(f"Received number is: {number}")

        # Wait for 1 second before the next read
        #time.sleep(0.01)

if __name__ == "__main__":
    try:
        # Start the receiving function in a background thread
        receiver_thread = threading.Thread(target=receive_and_display)
        receiver_thread.daemon = True
        receiver_thread.start()

        # Keep the main thread alive to allow the receiving thread to run
        while True:
            pass

    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        ser.close()
