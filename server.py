from flask import Flask, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__, static_folder='')

# Route to trigger the Python script and fetch live rates
@app.route('/update-rates', methods=['GET'])
def update_rates():
    try:
        # Run the liverates.py script
        subprocess.run(['python', 'liverates.py'], check=True)
        return jsonify({"message": "Rates updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve the rates.json file
@app.route('/rates.json', methods=['GET'])
def get_rates():
    return send_from_directory(os.getcwd(), 'rates.json')

# Route to serve the index.html file
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# Route to serve static files (CSS, JS, Images)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)