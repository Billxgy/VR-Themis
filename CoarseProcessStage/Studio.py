import os
import shutil
import subprocess

def apktoolReverseApk(apk_file, after_apktool_path_apk):
    command = f'apktool d "{apk_file}" -o "{after_apktool_path_apk}"'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    process.communicate(input=b'\n')
    print("Finish apktool reverse")

def statisticalFeaturesAll(after_apktool_path, apk_name, feature_File_Path):
    app_path = os.path.join(after_apktool_path, apk_name)
    if os.path.isdir(app_path):
        manifest_path = os.path.join(app_path, 'AndroidManifest.xml')
        uses_permission_count = 0
        uses_feature_count = 0
        
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
                manifest_content = manifest_file.read()
                uses_permission_count = manifest_content.count("<uses-permission")
                uses_feature_count = manifest_content.count("<uses-feature")
        
        with open(feature_File_Path, 'a') as file:
            file.write(f"{uses_permission_count}" + " ")
            file.write(f"{uses_feature_count}" + " ")
            # file.write(f"{int(avg_image_count)}" + " ")

        print(f"App: {os.path.basename(apk_name)}")
        
        shutil.rmtree(app_path)


def process_apk(apk_file, meshes_folder, after_apktool_path, feature_File_Path):
    # Change working directory to 'AssetStudio.Coarse'
    current_file_dir = os.path.dirname(__file__)
    assetstudio_coarse_path = os.path.join(current_file_dir, 'AssetStudio.Coarse')
    os.chdir(assetstudio_coarse_path)

    # Execute the command using subprocess
    command = f"AssetStudio.Coarse {apk_file} {os.path.dirname(feature_File_Path)} --game Normal"
    
    subprocess.run(command, shell=True)

    file_name = os.path.basename(apk_file)

    apk_name = os.path.splitext(file_name)[0]
    after_apktool_path_apk = os.path.join(after_apktool_path, apk_name)
    apktoolReverseApk(apk_file, after_apktool_path_apk)
    statisticalFeaturesAll(after_apktool_path, apk_name, feature_File_Path)

def coarseProcess(apks_folder, meshes_folder, after_apktool_path, feature_File_Path):
    # Ensure 'meshes' folder exists
    os.makedirs(meshes_folder, exist_ok=True)

    # Traverse each APK file, get hashes
    for root, dirs, files in os.walk(apks_folder):
        for file in files:
            if file.endswith(".apk"):
                apk_file_path = os.path.join(root, file)
                process_apk(apk_file_path, meshes_folder, after_apktool_path, feature_File_Path)

def getHashes(meshes_folder, hash_file_path, Hashing_folder):

    # Change working directory to 'Mesh_Hash'
    current_file_dir = os.path.dirname(__file__)
    mesh_hash_path = os.path.join(current_file_dir, Hashing_folder)
    os.chdir(mesh_hash_path)

    # Execute main.py with meshes_folder and hash_path as arguments
    command = f"python main.py {meshes_folder} {hash_file_path} {Hashing_folder}"
    print(command)
    subprocess.run(command, shell=True)