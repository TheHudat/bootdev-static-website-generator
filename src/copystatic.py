import os
import shutil

def copy_dir_content(target_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)
    
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        destination_path = os.path.join(destination_dir, item)
        print(f" * {item_path} -> {destination_path}")
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination_dir)
        else:
            copy_dir_content(item_path, destination_path)