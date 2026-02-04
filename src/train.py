import os
import json
import sys
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.model_builder import build_model

def train():
    # 1. Setup Generators
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator()

    print(f"Loading data from {config.TRAIN_DIR}...")
    
    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        os.path.join(config.DATA_DIR, 'val'),
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='categorical'
    )

    # 2. Save Class Indices
    if not os.path.exists(config.MODELS_DIR):
        os.makedirs(config.MODELS_DIR)

    indices_to_class = {v: k for k, v in train_generator.class_indices.items()}
    with open(config.CLASS_INDICES_PATH, 'w') as f:
        json.dump(indices_to_class, f)

    # 3. Build Model
    model = build_model(num_classes=train_generator.num_classes, 
                        img_size=config.IMG_SIZE, 
                        learning_rate=config.LEARNING_RATE)

    # 4. Callbacks
    callbacks = [
        ModelCheckpoint(config.MODEL_PATH, save_best_only=True, monitor='val_loss', mode='min'),
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    ]

    # 5. Train
    print("Starting training...")
    model.fit(
        train_generator,
        epochs=config.EPOCHS,
        validation_data=val_generator,
        callbacks=callbacks
    )
    print("Training complete. Model saved.")

if __name__ == "__main__":
    train()