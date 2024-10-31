import os
import shutil
import Studio
import time

def clear_and_recreate_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    os.mkdir(folder_path)

def clear_file_content(file_path):
    with open(file_path, 'w') as file:
        pass

if __name__ == "__main__":
    start_time = time.time()

    # ----------File path----------
    input_apps_folder = os.path.abspath("C:\\_Research\\Dataset\\11\\40")  

    # Don't change any paths below
    current_directory = os.getcwd()
    feature_File_Path = os.path.join(current_directory, "Data\\statisticalFeaturesUnity.txt")
    after_apktool_path = os.path.join(current_directory, "Data\\after_apktool_reverse")
    meshes_folder = os.path.join(current_directory, "Data\\meshes")
    try:
    # ----------Call functions----------
        clear_and_recreate_folder(meshes_folder)
        clear_file_content(feature_File_Path)
        clear_and_recreate_folder(after_apktool_path)

        Studio.coarseProcess(input_apps_folder, meshes_folder, after_apktool_path, feature_File_Path)

        end_time = time.time()

        elapsed_time = end_time - start_time
        print(f"Program completed in {elapsed_time:.2f} seconds")
        print("success!")
    except Exception as e:
        print(f"Error Info: {e}")
