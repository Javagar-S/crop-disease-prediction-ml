<div align="center">
  
  # 🌱 CropGuard | AI-Powered Crop Disease Detection
  
  **An AI-powered web application for precision agriculture and real-time crop disease detection.**

  [![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
  [![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0%2B-orange.svg?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
  [![Flask](https://img.shields.io/badge/Flask-Microframework-lightgrey.svg?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg?style=for-the-badge&logo=bootstrap)](https://getbootstrap.com/)

</div>

<br>

## 📖 Overview

**CropGuard** is a deep-learning-based web application designed to help farmers and agricultural specialists quickly diagnose plant diseases. Built with a robust **EfficientNetB0** model, it currently identifies 15 distinct classes across Bell Peppers, Potatoes, and Tomatoes. 

Going beyond standard image classification, CropGuard integrates **Test-Time Augmentation (TTA)** for enhanced prediction stability, real-time local weather syncing via the **Open-Meteo API**, and a seamless, accessible UI featuring voice-assisted reports.

---

## ✨ Key Features

* 🧠 **Robust Deep Learning Pipeline:** Utilizes a custom-tuned EfficientNetB0 model optimized for leaf feature extraction.
* 🛡️ **Test-Time Augmentation (TTA):** The inference engine automatically generates augmented variations (flipped, rotated, brightened) of user uploads to establish a consensus prediction, dramatically reducing false positives.
* 🚫 **Confidence Guardrails:** Built-in safeguards reject unclear images or non-leaf photos (Background Noise class) if confidence falls below 75%.
* 🌦️ **Contextual Weather Integration:** Fetches real-time temperature and humidity data for the user's location via the Open-Meteo API to contextualize fungal and bacterial growth conditions.
* 🎙️ **Accessibility First:** Integrated Web Speech API reads out diagnostic reports and treatment plans for hands-free operation in the field.
* 📄 **Print-Ready Reporting:** Custom CSS ensures that diagnostic results format perfectly into a clean, physical A4 report for distribution.

---

## 📸 Screenshots
<div align="center">

**Home Page**<br>
<img src="https://github.com/Javagar-S/crop-disease-prediction-ml/blob/979e24edc361e1bc8c65656f788cd839d9aca743/images/home%20page.png?raw=true" width="80%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

<br><br>

**Result Page**<br>
<img src="https://github.com/Javagar-S/crop-disease-prediction-ml/blob/979e24edc361e1bc8c65656f788cd839d9aca743/images/result%20page.png?raw=true" width="80%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

<br><br>

**Diagnostic Report**<br>
<img src="https://github.com/Javagar-S/crop-disease-prediction-ml/blob/979e24edc361e1bc8c65656f788cd839d9aca743/images/report.png?raw=true" width="80%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">


</div>

## 🏗️ Model Architecture

CropGuard relies on Transfer Learning to achieve high accuracy without requiring massive computational resources. 

* **Base Model:** `EfficientNetB0` (Pre-trained on ImageNet). Chosen for its optimal balance of high accuracy and low parameter count, making it highly efficient for web and edge deployment.
* **Custom Classification Head:**
  * `GlobalAveragePooling2D`: Flattens spatial dimensions while minimizing overfitting.
  * `BatchNormalization`: Stabilizes the learning process and accelerates convergence.
  * `Dense (256 units) + ReLU`: Extracts complex, non-linear patterns specific to plant pathology.
  * `Dropout (0.2 & 0.3)`: Aggressive regularization to prevent the model from memorizing the training data.
  * `Dense (Softmax)`: Final output layer mapping to the 15 distinct agricultural classes.

* **Training Strategy:** The model is trained in two phases. Phase 1 freezes the EfficientNet base to train the custom classification head. Phase 2 unfreezes the top 30 layers of the base model with a highly reduced learning rate (`1e-5`) for fine-grained feature tuning.

---

## 📊 Model Performance & Data Strategy

The model was trained on a highly imbalanced subset of the **PlantVillage Dataset** (approx. 20,600 images). To ensure clinical reliability across all classes:

* **Class Weight Balancing:** Integrated `sklearn.utils.class_weight` to mathematically penalize the model for missing minority classes (like healthy potatoes) while preventing it from over-predicting majority classes (like Tomato Yellow Leaf Curl Virus).
* **Dynamic Data Augmentation:** Applied aggressive spatial and color transformations during training (rotation, shifting, shearing, zooming, and flipping) to force the model to learn invariant disease features rather than background artifacts.
* **Inference Consensus:** During production deployment, the model achieves a **peak predictive confidence of up to 98.5%** by utilizing Test-Time Augmentation (TTA), ensuring that single-frame artifacts do not derail a diagnosis.

---

## 🛠️ Tech Stack

### **Machine Learning**
* **TensorFlow / Keras:** Model building, Transfer Learning, and Image Augmentation.
* **NumPy & Scikit-Learn:** Data manipulation and class weight balancing.

### **Backend**
* **Flask (Python):** Routing, file handling, and serving the ML inference engine.
* **Werkzeug:** Secure file upload management.

### **Frontend**
* **HTML5 / CSS3 / JavaScript:** Core structure and interactivity.
* **Bootstrap 5 & Bootstrap Icons:** Responsive layout and iconography.

---

## 📂 Project Structure

```text
crop-disease-prediction-ml/
│
├── data/                   # (Ignored in Git) Training data directories
│   ├── raw/                # Original PlantVillage dataset
│   ├── train/              # Training split
│   └── val/                # Validation split
│
├── models/                 # Serialized models and metadata
│   ├── disease_info.py     # Verified agricultural treatment dictionary
│   └── efficientnet_best.h5 # (Ignored in Git) Trained model weights
│
├── src/                    # Core Machine Learning logic
│   ├── inference_pipeline.py # TTA prediction and guardrail logic
│   ├── model_builder.py    # EfficientNet architecture setup
│   └── train.py            # Automated training pipeline
│
├── web/                    # Flask Application
│   ├── static/             # CSS, JS, and user uploads
│   ├── templates/          # HTML templates (index.html, result.html)
│   └── app.py              # Main Flask server
│
├── config.py               # Global system paths and ML hyperparameters
├── split_dataset.py        # Utility to partition raw data
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 Installation & Setup

<p align="center">
  <img src="https://img.shields.io/badge/Setup-Easy-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Environment-Recommended-blue?style=for-the-badge"/>
</p>

Ensure you have **Python 3.9+** installed. Using a virtual environment is highly recommended.

---

### 📥 1. Clone the Repository

```bash
git clone https://github.com/Javagar-S/crop-disease-prediction-ml.git
cd crop-disease-prediction-ml
```

---

### ⚙️ 2. Create & Activate Virtual Environment

<details>
<summary>🪟 <b>Windows</b></summary>

```bash
python -m venv crop
crop\Scripts\activate
```

</details>

<details>
<summary>🐧 <b>Linux / macOS</b></summary>

```bash
python3 -m venv crop
source crop/bin/activate
```

</details>

---

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

<p align="center">
  <img src="https://img.shields.io/badge/Run-App-Now-green?style=for-the-badge"/>
</p>

### ▶️ Run the Web Application

```bash
python web/app.py
```

🌐 Open in your browser:

```
http://localhost:5000
```

---

## 🧠 Model Training (Optional)

<p align="center">
  <img src="https://img.shields.io/badge/Training-Advanced-orange?style=for-the-badge"/>
</p>

### 📁 Step 1: Prepare Dataset

Place your dataset inside:

```
data/raw/
```

---

### 🔀 Step 2: Split Dataset

```bash
python split_dataset.py
```

---

### 🏋️ Step 3: Train Model

```bash
python src/train.py
```

---
