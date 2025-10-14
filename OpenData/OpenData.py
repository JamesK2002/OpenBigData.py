import os
import shutil
import random
import time

def get_folder_size(folder):
    total = 0
    for root, _, files in os.walk(folder):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total

def shift_file_timestamps(folder, years=10):
    """Shift file modification and access times forward by N years."""
    seconds_in_year = 365 * 24 * 60 * 60 * years
    for root, _, files in os.walk(folder):
        for f in files:
            file_path = os.path.join(root, f)
            try:
                atime = os.path.getatime(file_path)
                mtime = os.path.getmtime(file_path)
                os.utime(file_path, (atime + seconds_in_year, mtime + seconds_in_year))
            except Exception as e:
                print(f" Could not change timestamp for {file_path}: {e}")

def replicate_until_60(original_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for category in os.listdir(original_folder):
        category_path = os.path.join(original_folder, category)
        if not os.path.isdir(category_path):
            continue

        print(f"\n Working on category: {category}")

        # Make a full copy of the category into the output folder (work here)
        new_category_path = os.path.join(output_folder, category)
        if os.path.exists(new_category_path):
            shutil.rmtree(new_category_path)
        shutil.copytree(category_path, new_category_path)

        # Create a temporary "cloned" folder inside the copy
        cloned_path = os.path.join(new_category_path, "cloned")
        os.makedirs(cloned_path, exist_ok=True)

        # Collect CSV files in the working copy
        csv_files = [
            f for f in os.listdir(new_category_path)
            if f.endswith(".csv") and not os.path.isdir(os.path.join(new_category_path, f))
        ]

        if not csv_files:
            print(f"  No CSV files found in {category}")
            continue

        initial_size = get_folder_size(new_category_path)
        target_size = initial_size * 1.6
        initial_count = len(csv_files)

        print(f"  Initial size: {initial_size / (1024*1024):.2f} MB")
        print(f"  Initial files: {initial_count}")

        cloned_count = 0

        # Replicate until at least 60% increase
        first_batch_done = False
        cloned_in_batch = 0

        while get_folder_size(new_category_path) < target_size:
            num_to_clone = min(50, len(csv_files))
            sample = random.sample(csv_files, num_to_clone)

            for name in sample:
                src = os.path.join(new_category_path, name)
                clone_name = f"clone_{random.randint(1000,9999)}_{name}"
                dst = os.path.join(cloned_path, clone_name)
                shutil.copy2(src, dst)
                cloned_count += 1
                cloned_in_batch += 1

                #  Stop immediately if we hit 60%
                if get_folder_size(new_category_path) >= target_size:
                    break

            # Move cloned files back to main category folder
            for f in os.listdir(cloned_path):
                shutil.move(os.path.join(cloned_path, f), new_category_path)

            current_size_mb = get_folder_size(new_category_path) / (1024 * 1024)


            cloned_in_batch = 0  # reset count for next loop



        final_size = get_folder_size(new_category_path)
        size_increase = ((final_size - initial_size) / initial_size) * 100
        total_files = len([f for f in os.listdir(new_category_path) if f.endswith(".csv")])

        # Shift all timestamps by +10 years
        shift_file_timestamps(new_category_path, years=10)

        print(f"\n Summary for {category}:")
        print(f"   Original files: {initial_count}")
        print(f"   Cloned files: {cloned_count}")
        print(f"   Total files (original + cloned): {total_files}")
        print(f"   Final size: {final_size / (1024*1024):.2f} MB")
        print(f"   Size increased by: {size_increase:.1f}%")
        print(f"   Saved safely in: {new_category_path}")
        print("+---------------------------------------------------------------------------+")

# Example usage
original_folder = r"C:\Users\ayomi\Documents\rawdata_spring2025-20251004T004727Z-1-001\processed"
output_folder = r"C:\Users\ayomi\Documents\file-opendata\brainwaves"
replicate_until_60(original_folder, output_folder)
