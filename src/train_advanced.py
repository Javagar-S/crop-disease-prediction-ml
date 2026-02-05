import os
import json
import sys
import numpy as np
import tensorflow as tf
from sklearn.utils import class_weight
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard

# Connect to config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.model_builder import build_model

def get_class_weights(train_generator):
    """
    DYNAMICALLY calculates weights.
    If 'Tomato_Healthy' has 1000 pics and 'Tomato_Blight' has 100,
    it tells the model to treat 1 Blight error as equal to 10 Healthy errors.
    """
    class_indices = train_generator.class_indices
    class_counts = np.unique(train_generator.classes, return_counts=True)[1]
    
    weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_generator.classes),
        y=train_generator.classes
    )
    return dict(enumerate(weights))

def train_robust_model():
    print("🔥 Starting ADVANCED Training Pipeline...")

    # 1. Dynamic Data Augmentation (Harder training = Smarter model)
    train_datagen = ImageDataGenerator(
        rotation_range=40,      # High rotation
        width_shift_range=0.3,
        height_shift_range=0.3,
        shear_range=0.3,
        zoom_range=0.3,
        horizontal_flip=True,
        vertical_flip=True,     # Leaves can be upside down
        brightness_range=[0.7, 1.3], # Handle sunny/dark photos
        fill_mode='nearest'
    )

    # Validation data should NOT be augmented
    val_datagen = ImageDataGenerator()

    print(f"   Loading Data from: {config.TRAIN_DIR}")
    
    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )

    val_generator = val_datagen.flow_from_directory(
        config.VAL_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='categorical'
    )

    # 2. Calculate Robust Class Weights
    weights = get_class_weights(train_generator)
    print(f"⚖️  Class Weights Calculated: {weights}")

    # 3. Save the Brain Map (Classes)
    if not os.path.exists(config.MODELS_DIR): os.makedirs(config.MODELS_DIR)
    
    indices_to_class = {v: k for k, v in train_generator.class_indices.items()}
    with open(config.CLASS_INDICES_PATH, 'w') as f:
        json.dump(indices_to_class, f)

    # 4. Build Model (Start Frozen)
    model = build_model(num_classes=train_generator.num_classes, 
                        img_size=config.IMG_SIZE, 
                        fine_tune=False)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )

    # 5. Callbacks (The Safety Nets)
    callbacks = [
        ModelCheckpoint(config.MODEL_PATH, save_best_only=True, monitor='val_loss', mode='min', verbose=1),
        EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-7, verbose=1)
    ]

    # 6. Phase 1: Train the Head (Fast)
    print("\n🧠 Phase 1: Training Classifier Head...")
    model.fit(
        train_generator,
        epochs=10, # Short run for head
        validation_data=val_generator,
        class_weight=weights, # Apply dynamic weights
        callbacks=callbacks
    )

    # 7. Phase 2: Fine-Tuning (Deep Learning)
    print("\n🧠 Phase 2: Unfreezing & Fine-Tuning...")
    
    # Rebuild model with unfreezing enabled
    # Note: Keras models need re-compiling after changing trainable status, 
    # but since we wrapped it in a function, we can just set layers trainable here.
    base_model = model.layers[1] # Access the EfficientNet part
    base_model.trainable = True
    
    # Freeze the bottom N layers (keep core features, retrain texture features)
    for layer in base_model.layers[:-30]: 
        layer.trainable = False

    # Re-compile with VERY low learning rate to not break what we learned
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), # 100x slower learning
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )

    model.fit(
        train_generator,
        epochs=config.EPOCHS, # Long run
        validation_data=val_generator,
        class_weight=weights,
        callbacks=callbacks
    )

    print("✅ Robust Training Complete.")

if __name__ == "__main__":
    train_robust_model()