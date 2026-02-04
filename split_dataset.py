import os
import shutil
import random

SOURCE = "data"
DEST = "data"
SPLIT_SIZE = 0.8

def split_data():
    if not os.path.exists(SOURCE):
        print("Source folder not found!")
        return

    # Create destination folders
    for folder in ['train', 'val']:
        os.makedirs(os.path.join(DEST, folder), exist_ok=True)

    categories = os.listdir(SOURCE)
    
    for cat in categories:
        cat_path = os.path.join(SOURCE, cat)
        
        # skip files or metadata folders
        if not os.path.isdir(cat_path) or cat.startswith('.'):
            continue
            
        # Get list of images
        images = [f for f in os.listdir(cat_path) if os.path.isfile(os.path.join(cat_path, f))]
        
        if not images:
            print(f"Skipping {cat}: No images found inside.")
            continue

        print(f"Processing: {cat} ({len(images)} images)")
        
        os.makedirs(os.path.join(DEST, 'train', cat), exist_ok=True)
        os.makedirs(os.path.join(DEST, 'val', cat), exist_ok=True)
        
        random.shuffle(images)
        split_point = int(len(images) * SPLIT_SIZE)
        
        # Copying files
        for i, img in enumerate(images):
            src_file = os.path.join(cat_path, img)
            target_subfolder = 'train' if i < split_point else 'val'
            dst_file = os.path.join(DEST, target_subfolder, cat, img)
            shutil.copy(src_file, dst_file)

if __name__ == "__main__":
    split_data()
    print("\n✅ Done! Your 'data' folder is ready for training.")