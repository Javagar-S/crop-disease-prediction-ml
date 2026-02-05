import os

# ==========================================
# 1. PATH CONFIGURATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data Paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')       # Put your PlantVillage dataset here
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
VAL_DIR = os.path.join(DATA_DIR, 'val')

# Model Paths
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'efficientnet_best.h5')
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, 'class_indices.json')
DISEASE_INFO_PATH = os.path.join(MODELS_DIR, 'disease_info.json') # 🆕 Links to remedies

# ==========================================
# 2. MODEL HYPERPARAMETERS
# ==========================================
IMG_SIZE = (224, 224)   # Standard for EfficientNet
BATCH_SIZE = 32
EPOCHS = 25             # Increased for better convergence
LEARNING_RATE = 0.001   # Start fast
FINE_TUNE_LR = 1e-5     # Slow down for fine-tuning later

# ==========================================
# 3. PRO REQUIREMENTS (ROBUSTNESS)
# ==========================================
CONFIDENCE_THRESHOLD = 0.75  # 🛡️ If < 75%, tell user "Image Unclear"
BACKGROUND_CLASS = "Background_Noise" # 🛡️ Class name for random images (walls, sky)

# Dynamic Class Detection (Safe Mode)
def get_classes():
    if os.path.exists(TRAIN_DIR):
        # Only count directories, ignore .DS_Store or hidden files
        return sorted([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])
    return []