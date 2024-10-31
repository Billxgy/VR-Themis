import os

def read_hashes(file_path):
    hashes = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if (len(parts) == 3):
                    file, name, _hash = parts[0], parts[1], parts[2]
                    if file != "unity_default_resources":
                        hashes[name] = _hash
    except FileNotFoundError:
        return None
    
    return list(hashes.values())

def compare_hashes(hashes1, hashes2):
    if not hashes1 or not hashes2:
        return False
    
    # Convert lists to sets for comparison
    set1 = set(hashes1)
    set2 = set(hashes2)
    
    # Calculate intersection
    common_values = set1 & set2
    union_values = set1.union(set2)
    if len(common_values) >= len(union_values) * 0.7 or len(union_values) <= 5:
        return True
    else:
        return False

def prune(apps_folder):
    app_folders = [os.path.join(apps_folder, app) for app in os.listdir(apps_folder) if os.path.isdir(os.path.join(apps_folder, app))]
    comparisons = []
    
    for i, app_folder1 in enumerate(app_folders):
        hashes1 = read_hashes(os.path.join(app_folder1, 'compare', 'hashes.txt'))
        if not hashes1:
            continue
        
        for app_folder2 in app_folders[i+1:]:
            hashes2 = read_hashes(os.path.join(app_folder2, 'compare', 'hashes.txt'))
            if not hashes2:
                continue
            
            if compare_hashes(hashes1, hashes2):
                comparisons.append((app_folder1, app_folder2))
    
    return comparisons