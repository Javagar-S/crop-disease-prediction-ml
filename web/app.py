import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.inference_pipeline import predictor  # The Robust Brain

app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages" # Needed for safety

# Configure Upload Folder
UPLOAD_FOLDER = os.path.join(config.BASE_DIR, 'web', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Validation: Check if file exists
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # 2. Save File Securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 3. call the ROBUST PIPELINE (The Brain)
        # This uses TTA (Test Time Augmentation) and Confidence Checks
        result = predictor.predict_robust(filepath)

        # 4. Handle different outcomes
        if result['status'] == 'Success':
            return render_template('result.html', 
                                   img_filename=filename, 
                                   data=result)
        
        elif result['status'] == 'Unsure':
            flash(f"⚠️ {result['message']} (Confidence: {result['confidence']})")
            return redirect(url_for('index'))
            
        elif result['status'] == 'Invalid':
            flash(f"⛔ {result['message']}")
            return redirect(url_for('index'))

    flash('Invalid file type. Please upload JPG or PNG.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run on all interfaces for local network testing
    app.run(host='0.0.0.0', port=5000, debug=True)