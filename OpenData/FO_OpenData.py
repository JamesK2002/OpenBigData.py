import os
import shutil
import random

def get_folder_size(folder):
    total = 0
    for root, _, files in os.walk(folder):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total

def replicate_until_60(data_folder):
    for category in os.listdir(data_folder):
        category_path = os.path.join(data_folder, category)
        if not os.path.isdir(category_path):
            continue

        # make a cloned subfolder
        cloned_path = os.path.join(category_path, "cloned")
        os.makedirs(cloned_path, exist_ok=True)

        # collect csv files
        csv_files = [f for f in os.listdir(category_path) if f.endswith(".csv")]
        if not csv_files:
            print(f"No CSV files found in {category}")
            continue

        initial_size = get_folder_size(category_path)
        target_size = initial_size * 1.6

        print(f"\nCategory: {category}")
        print(f"Initial size: {initial_size / 1024:.2f} KB")

        # keep cloning until 60% growth
        while get_folder_size(category_path) < target_size:
            num_to_clone = min(50, len(csv_files))
            sample = random.sample(csv_files, num_to_clone)

            for name in sample:
                src = os.path.join(category_path, name)
                clone_name = f"clone_{random.randint(1000,9999)}_{name}"
                dst = os.path.join(cloned_path, clone_name)
                shutil.copy2(src, dst)

            # move cloned files back to main category folder
            for f in os.listdir(cloned_path):
                shutil.move(os.path.join(cloned_path, f), category_path)

            print(f"Replicated {num_to_clone} more files... current size: {get_folder_size(category_path)/1024:.2f} KB")

        # final count
        total_files = len([f for f in os.listdir(category_path) if f.endswith(".csv")])
        print(f"✅ Finished {category}: {total_files} total files, size: {get_folder_size(category_path)/1024:.2f} KB")

# Example usage
data_folder = r"C:\Users\ayomi\Documents\rawdata_spring2025\data\processed"
replicate_until_60(data_folder)
