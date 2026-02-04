import os

# Base Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Model Settings
MODEL_PATH = os.path.join(MODELS_DIR, 'efficientnet_model.h5')
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, 'class_indices.json')

# Hyperparameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001

# Dynamic: Auto-detect classes if data folder exists
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
if os.path.exists(TRAIN_DIR):
    CLASSES = sorted(os.listdir(TRAIN_DIR))
    NUM_CLASSES = len(CLASSES)
else:
    CLASSES = []
    NUM_CLASSES = 0