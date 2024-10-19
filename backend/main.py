from flask import Flask, send_from_directory, jsonify, request
import serial
import threading

# Initialize the Flask app and configure it to serve static files from /app/frontend
app = Flask(__name__, static_folder='frontend', static_url_path='')

# Global variables
serial_data = "Waiting for data..."
user_location = None

# Function to continuously read from the serial port
def read_from_serial():
    global serial_data
    ser = None
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        while True:
            if ser.in_waiting > 0:
                serial_data = ser.readline().decode('utf-8').rstrip()
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    finally:
        if ser:
            ser.close()

# Start the serial reading thread
serial_thread = threading.Thread(target=read_from_serial)
serial_thread.daemon = True
serial_thread.start()

# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (e.g., JS, CSS)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# API route to get serial data and capacity information
@app.route('/api/message') 
def send_message():
    try:
        capacity = int(serial_data)  # Assuming serial_data contains the current number of passengers
        max_capacity = 60  # Total number of spots
        percentage_full = (capacity / max_capacity) * 100
        spots_left = max_capacity - capacity
    except ValueError:
        capacity = 0  # Default value if parsing fails
        percentage_full = 0
        spots_left = 60

    over_capacity = capacity > max_capacity
    return jsonify({
        "message": f"Capacity at {capacity} of {max_capacity}",
        "over_capacity": over_capacity,
        "percentage_full": round(percentage_full, 2),
        "spots_left": spots_left
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
