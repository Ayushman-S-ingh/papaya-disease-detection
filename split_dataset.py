import os
import shutil
import random

# Source dataset path
source_dir = "Dataset copy/papaya main dataset"

# Target dataset path
train_dir = "dataset/train"
test_dir = "dataset/test"

# Create folders
classes = [cls for cls in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, cls))]

for cls in classes:
    os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
    os.makedirs(os.path.join(test_dir, cls), exist_ok=True)

    class_path = os.path.join(source_dir, cls)
    images = [img for img in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, img))]
    random.shuffle(images)

    split = int(0.8 * len(images))

    train_images = images[:split]
    test_images = images[split:]

    for img in train_images:
        src = os.path.join(source_dir, cls, img)
        dst = os.path.join(train_dir, cls, img)
        shutil.copy(src, dst)

    for img in test_images:
        src = os.path.join(source_dir, cls, img)
        dst = os.path.join(test_dir, cls, img)
        shutil.copy(src, dst)

print("✅ Dataset split complete!")