import tensorflow as tf
import numpy as np
import json
import os
import sys

# Connect to config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# --- FIXED IMPORT: Pointing to 'disease_info.py' ---
from models.disease_info import plant_disease_info

class DiseasePredictor:
    def __init__(self):
        print("⚙️ Loading Robust Model...")
        self.model = tf.keras.models.load_model(config.MODEL_PATH)
        
        # --- FIXED SECTION START: Loading Class Labels ---
        with open(config.CLASS_INDICES_PATH, 'r') as f:
            raw_indices = json.load(f)
            
            # Auto-detect format:
            # Check the first key. Is it a number like "0" or a word like "Tomato"?
            first_key = list(raw_indices.keys())[0]
            
            if first_key.isdigit():
                # Format is {"0": "Tomato"}. We just convert "0" -> 0.
                self.labels = {int(k): v for k, v in raw_indices.items()}
            else:
                # Format is {"Tomato": 0}. We must SWAP keys and values.
                self.labels = {v: k for k, v in raw_indices.items()}
        
        print(f"✅ Class Labels Loaded: {len(self.labels)} classes found.")
        # --- FIXED SECTION END ---
            
        # --- NEW: Link directly to the imported Python dictionary ---
        # No json.load() needed anymore!
        self.knowledge_base = plant_disease_info

    def preprocess(self, img_array):
        # EfficientNet expects raw 0-255 inputs, but we standardize size
        img = tf.image.resize(img_array, config.IMG_SIZE)
        return tf.expand_dims(img, axis=0)

    def predict_robust(self, img_path):
        """
        Uses Test-Time Augmentation (TTA).
        """
        original_img = tf.keras.utils.load_img(img_path)
        img_arr = tf.keras.utils.img_to_array(original_img)
        
        # 1. Create Batch of Augmented Images
        batch = []
        batch.append(tf.image.resize(img_arr, config.IMG_SIZE)) # Original
        batch.append(tf.image.resize(tf.image.flip_left_right(img_arr), config.IMG_SIZE)) # Flipped
        batch.append(tf.image.resize(tf.image.rot90(img_arr), config.IMG_SIZE)) # Rotated
        batch.append(tf.image.resize(tf.image.adjust_brightness(img_arr, 1.2), config.IMG_SIZE)) # Bright
        
        batch = np.array(batch)

        # 2. Predict on all of them
        predictions = self.model.predict(batch)
        
        # 3. Average the results (Consensus)
        avg_pred = np.mean(predictions, axis=0)
        
        # 4. Analysis
        class_idx = np.argmax(avg_pred)
        confidence = np.max(avg_pred)
        
        # The dictionary is now guaranteed to be {Int: Name}, so this works safely
        class_key = self.labels.get(int(class_idx), "Unknown") 
        
        # 5. Guardrails
        if confidence < config.CONFIDENCE_THRESHOLD:
            return {
                "status": "Unsure",
                "message": f"Low confidence ({confidence:.0%}). Please upload a clearer image.",
                "confidence": f"{confidence:.2f}"
            }
        
        bg_class = getattr(config, 'BACKGROUND_CLASS', 'Background_Noise')
        if class_key == bg_class:
            return {
                "status": "Invalid",
                "message": "No leaf detected. Please upload a clear plant image.",
                "confidence": f"{confidence:.2f}"
            }

        # 6. Fetch Knowledge (Dynamic)
        # We get the info matching the class_key (e.g. "Tomato_Early_blight")
        # .get() returns an empty dict {} if the disease isn't found, preventing crashes
        info = self.knowledge_base.get(class_key, {})
        
        # 7. Return the RICH structure required by result.html
        return {
            "status": "Success",
            "prediction": info.get("name", class_key.replace("_", " ")),
            "scientific_name": info.get("scientific_name", "N/A"),
            "description": info.get("description", "No description available."),
            "confidence": f"{confidence:.1%}",
            "severity": info.get("severity", "Unknown"),
            "symptoms": info.get("symptoms", []),
            "treatment_plan": info.get("treatment_plan", []),
            "prevention": info.get("prevention", [])
        }

# Singleton instance
predictor = DiseasePredictor()