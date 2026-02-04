import os
import json
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request, jsonify

# Add parent dir to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

app = Flask(__name__)

# Load Model Once
print("Loading model...")
model = load_model(config.MODEL_PATH)
with open(config.CLASS_INDICES_PATH, 'r') as f:
    class_indices = json.load(f)

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=config.IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    # Save temp file
    upload_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    filepath = os.path.join(upload_path, file.filename)
    file.save(filepath)

    # Predict
    try:
        processed_img = prepare_image(filepath)
        prediction = model.predict(processed_img)
        
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        confidence = np.max(prediction)
        
        result_class = class_indices.get(str(predicted_class_index), "Unknown")
        
        return jsonify({
            'class': result_class,
            'confidence': f"{confidence * 100:.2f}%",
            'image_url': filepath
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)