from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import pickle
import os

app = Flask(__name__)

# Load the model
model = pickle.load(open('weather_model.pkl', 'rb'))

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

@app.route('/api', methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    
    # Check that all required fields are present
    if not all(key in data for key in ['precipitation', 'temp_max', 'temp_min', 'wind']):
        return jsonify({'error': 'Missing required field'}), 400
    
    # Extract the input data from the JSON payload
    precipitation = data['precipitation']
    temp_max = data['temp_max']
    temp_min = data['temp_min']
    wind = data['wind']
    
    # Check that the input data are valid numerical values
    if not all(isinstance(value, (int, float)) for value in [precipitation, temp_max, temp_min, wind]):
        return jsonify({'error': 'Invalid input data'}), 400
    
    # Prepare the input data for the model
    input_data = np.array([[precipitation, temp_max, temp_min, wind]])
    
    # Make prediction using the loaded model
    prediction = model.predict(input_data)
    
    # Return the prediction as JSON
    output = {'weather': prediction[0]}
    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
