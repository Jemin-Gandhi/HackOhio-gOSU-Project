from flask import Flask, send_from_directory, jsonify
import serial
import threading

# Initialize the Flask app and configure it to serve static files from /app/frontend
app = Flask(__name__, static_folder='frontend', static_url_path='')

# Global variable to store the serial data
serial_data = "Waiting for data..."

# Function to continuously read from the serial port
def read_from_serial():
    global serial_data
    ser = None
    try:
        # Use /dev/ttyUSB0 instead of COM3 (Linux-style path)
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

# New route that responds with the latest serial data
@app.route('/api/message') 
def send_message():
    return jsonify({"message": serial_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
