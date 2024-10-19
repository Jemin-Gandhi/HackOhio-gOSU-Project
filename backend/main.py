from flask import Flask, send_from_directory, jsonify

# Initialize the Flask app and configure it to serve static files from /app/frontend
app = Flask(__name__, static_folder='frontend', static_url_path='')

# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (e.g., JS, CSS)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# New route that responds to a button click with a JSON message
@app.route('/api/message') 
def send_message():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
