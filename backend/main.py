from flask import Flask, send_from_directory

# Initialize the Flask application
app = Flask(__name__, static_folder='../frontend')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

def main():
    # This is where you would add any additional functionality to run in your main function
    print("Starting Flask server...")
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    app.run(debug=True)
