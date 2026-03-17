from flask import Flask, jsonify, send_from_directory
import subprocess
import os
import sys

app = Flask(__name__, static_folder='')

# Route to trigger the Python script and fetch live rates
@app.route('/update-rates', methods=['GET'])
def update_rates():
    try:
        # Run the liverates.py script
        # Use the same Python interpreter that's running the server
        script_path = os.path.join(os.getcwd(), 'liverates.py')
        result = subprocess.run([
            sys.executable,
            script_path
        ], cwd=os.getcwd(), capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({
                "error": "liverates.py failed",
                "stdout": result.stdout,
                "stderr": result.stderr
            }), 500

        return jsonify({"message": "Rates updated successfully", "stdout": result.stdout}), 200
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