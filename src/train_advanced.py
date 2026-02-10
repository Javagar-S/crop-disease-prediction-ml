import os
import json
import sys
import numpy as np
import tensorflow as tf
from sklearn.utils import class_weight
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Connect to config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.model_builder import build_model

def get_class_weights(train_generator):
    """
    Calculates weights to balance the dataset.
    """
    weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_generator.classes),
        y=train_generator.classes
    )
    return dict(enumerate(weights))

def create_auxiliary_files(class_indices):
    """
    NEW FUNCTION: Generates the necessary Python files for the 'models' package.
    """
    print("📝 Generating System Files...")

    # 1. Create __init__.py so Python treats 'models' as a package
    init_path = os.path.join(config.MODELS_DIR, '__init__.py')
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write("# This file makes the directory a Python package\n")
        print(f"   Created: {init_path}")

    # 2. Generate disease_info.py automatically
    # We create a template based on the classes we found in the folders.
    info_path = os.path.join(config.MODELS_DIR, 'disease_info.py')
    
    # We only create this if it doesn't exist, so we don't overwrite your manual edits later!
    if not os.path.exists(info_path):
        print(f"   Generating template for: {info_path}")
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write("# Auto-generated Disease Dictionary\n")
            f.write("# EDIT THIS FILE with real medical advice!\n\n")
            f.write("plant_disease_info = {\n")
            
            for class_name, index in class_indices.items():
                # formatting the key name to be pretty (Tomato___Blight -> Tomato Blight)
                readable_name = class_name.replace("_", " ").replace("  ", " ").strip()
                
                f.write(f'    "{class_name}": {{\n')
                f.write(f'        "name": "{readable_name}",\n')
                f.write(f'        "description": "Auto-generated description for {readable_name}. Please update.",\n')
                f.write(f'        "symptoms": ["Symptom 1", "Symptom 2"],\n')
                f.write(f'        "treatment_plan": ["Use Fungicide X", "Rotate Crops"],\n')
                f.write(f'        "prevention": ["Keep leaves dry", "Use resistant varieties"]\n')
                f.write('    },\n')
            
            f.write("}\n")
        print("✅ disease_info.py created successfully.")
    else:
        print("ℹ️  disease_info.py already exists. Skipping generation to protect your data.")

def train_robust_model():
    print("🔥 Starting AUTOMATED Training Pipeline...")

    # 1. Setup Generators
    train_datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.3,
        height_shift_range=0.3,
        shear_range=0.3,
        zoom_range=0.3,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator()

    print(f"   Loading Data from: {config.TRAIN_DIR}")
    
    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        config.VAL_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='categorical'
    )

    # 2. Save Class Map (JSON)
    if not os.path.exists(config.MODELS_DIR): os.makedirs(config.MODELS_DIR)
    
    # Invert the map: {'Tomato': 0} -> {0: 'Tomato'}
    indices_to_class = {v: k for k, v in train_generator.class_indices.items()}
    with open(config.CLASS_INDICES_PATH, 'w') as f:
        json.dump(indices_to_class, f)

    # ============================================================
    # 3. NEW STEP: Auto-Generate Python Helper Files
    # ============================================================
    create_auxiliary_files(train_generator.class_indices)
    # ============================================================

    # 4. Calculate Weights
    weights = get_class_weights(train_generator)
    
    # 5. Build Model
    model = build_model(num_classes=train_generator.num_classes, 
                        img_size=config.IMG_SIZE, 
                        fine_tune=False)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    callbacks = [
        ModelCheckpoint(config.MODEL_PATH, save_best_only=True, monitor='val_loss', mode='min'),
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    ]

    # 6. Train
    print("\n🧠 Phase 1: Training Head...")
    model.fit(
        train_generator,
        epochs=10,
        validation_data=val_generator,
        class_weight=weights,
        callbacks=callbacks
    )

    print("\n🧠 Phase 2: Fine-Tuning...")
    base_model = model.layers[1]
    base_model.trainable = True
    for layer in base_model.layers[:-30]: layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        train_generator,
        epochs=config.EPOCHS,
        validation_data=val_generator,
        class_weight=weights,
        callbacks=callbacks
    )

    print("✅ Training Complete. All system files generated.")

if __name__ == "__main__":
    train_robust_model()