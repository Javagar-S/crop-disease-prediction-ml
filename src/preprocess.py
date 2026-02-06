import os
import shutil
import random
import sys

# Add parent directory to path to see config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def split_dataset(split_ratio=0.8):
    print(f"🚀 Starting Data Split from {config.RAW_DATA_DIR}...")
    
    if not os.path.exists(config.RAW_DATA_DIR):
        print(f"❌ Error: '{config.RAW_DATA_DIR}' not found. Please create it and add your class folders.")
        return

    # Clean existing train/val to prevent duplication
    if os.path.exists(config.TRAIN_DIR): shutil.rmtree(config.TRAIN_DIR)
    if os.path.exists(config.VAL_DIR): shutil.rmtree(config.VAL_DIR)

    classes = [d for d in os.listdir(config.RAW_DATA_DIR) if os.path.isdir(os.path.join(config.RAW_DATA_DIR, d))]
    
    print(f"📊 Found {len(classes)} classes: {classes}")

    for class_name in classes:
        src_path = os.path.join(config.RAW_DATA_DIR, class_name)
        images = [f for f in os.listdir(src_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Shuffle for randomness
        random.shuffle(images)
        split_point = int(len(images) * split_ratio)
        
        train_imgs = images[:split_point]
        val_imgs = images[split_point:]

        # Create subdirectories
        os.makedirs(os.path.join(config.TRAIN_DIR, class_name), exist_ok=True)
        os.makedirs(os.path.join(config.VAL_DIR, class_name), exist_ok=True)

        # Copy files
        print(f"   Processing {class_name}: {len(train_imgs)} Train, {len(val_imgs)} Val")
        for img in train_imgs:
            shutil.copy(os.path.join(src_path, img), os.path.join(config.TRAIN_DIR, class_name, img))
        for img in val_imgs:
            shutil.copy(os.path.join(src_path, img), os.path.join(config.VAL_DIR, class_name, img))

    print("✅ Data Splitting Complete!")

if __name__ == "__main__":
    split_dataset()