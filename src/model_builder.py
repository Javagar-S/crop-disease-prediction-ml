import tensorflow as tf
from tensorflow.keras import layers, models, applications

def build_model(num_classes, img_size=(224, 224), fine_tune=False):
    inputs = layers.Input(shape=(img_size[0], img_size[1], 3))

    # 1. The Pre-trained Brain (Transfer Learning)
    # EfficientNet includes internal rescaling, so no need for x / 255.0
    base_model = applications.EfficientNetB0(
        include_top=False, 
        weights="imagenet", 
        input_tensor=inputs
    )

    # 2. Freeze/Unfreeze Logic
    if fine_tune:
        base_model.trainable = True
        # Unfreeze only the top 20 layers for safety
        for layer in base_model.layers[:-20]:
            layer.trainable = False
    else:
        base_model.trainable = False

    # 3. The Classifier Head (Custom for your leaves)
    x = layers.GlobalAveragePooling2D()(base_model.output)
    x = layers.BatchNormalization()(x)  # Stabilizes training
    x = layers.Dropout(0.3)(x)          # Prevents overfitting
    x = layers.Dense(256, activation='relu')(x) # Extra dense layer for better feature mapping
    x = layers.Dropout(0.2)(x)
    
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs)
    
    return model