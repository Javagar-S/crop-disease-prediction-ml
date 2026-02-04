import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0

def build_model(num_classes, img_size=(224, 224), learning_rate=0.001):
    inputs = layers.Input(shape=(img_size[0], img_size[1], 3))

    # Load pre-trained EfficientNetB0
    base_model = EfficientNetB0(include_top=False, input_tensor=inputs, weights="imagenet")
    base_model.trainable = False  # Freeze base model

    # Rebuild top
    x = layers.GlobalAveragePooling2D()(base_model.output)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)
    
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    # Compile
    model = models.Model(inputs, outputs)
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    return model