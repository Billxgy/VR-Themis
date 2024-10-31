import os
import shutil
import sys
import time
import Studio

def clear_and_recreate_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    os.mkdir(folder_path)

def clear_file_content(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        pass

if __name__ == "__main__":
    # ----------File paths----------
    current_directory = os.getcwd()
    
    # Check if the user provided an argument
    if len(sys.argv) < 2:
        print("Usage: python FineProcessStage/fineStage.py APK_OR_DIRECTORY_PATH")
        sys.exit(1)  # Exit if no argument is provided
    
    # Get the input apps folder from the first argument
    input_apps_folder = os.path.abspath(sys.argv[1])
    
    Clusters_path = os.path.join(current_directory, "CoarseProcessStage\\Clustering\\clusters.json")
    meshes_folder = os.path.join(current_directory, "Data\\meshes")
    Hashing_folder = os.path.join(current_directory, "FineProcessStage\\Mesh_Hash")
    ClusterApks_folder = os.path.join(current_directory, "Data\\ClusterApks")
    asset_studio_path = os.path.join(current_directory, "FineProcessStage\\AssetStudio.Fine\\AssetStudio.GUI.exe")
    il2cppdumper_path = os.path.join(current_directory, "FineProcessStage\\IL2CPPDumper")
    dnSpy_path = os.path.join(current_directory, "FineProcessStage\\dnSpy")
    unzip_temp_folder = os.path.join(current_directory, "Data\\temp")

    # ----------Function calls----------
    try:
        clear_and_recreate_folder(ClusterApks_folder)
        clear_and_recreate_folder(unzip_temp_folder)
        start_time = time.time()
        response = Studio.getApksOfClusters(input_apps_folder, Clusters_path, ClusterApks_folder, asset_studio_path, il2cppdumper_path, dnSpy_path, unzip_temp_folder)
        response2 = Studio.compareClusters(ClusterApks_folder)

        if response is not None:
            print("Exception in Code Reversing: " + response)
        if response2 is not None:
            print("Exception in Extreme Tree: " + response2)


    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Program executed in {elapsed_time:.2f} seconds.")




