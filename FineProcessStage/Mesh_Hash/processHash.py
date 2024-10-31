import os
import shutil
from Mesh_Hash.hash import hash1
from Mesh_Hash.decimate import decimate
 

def processHash(meshes_folder, hash_file_path):
    input_folder = meshes_folder
    ratio1 = 0.4
    ratio2 = 0.1
    temp_folder = os.path.abspath('FineProcessStage\\Mesh_Hash\\temp')
    mesh_hash_path = hash_file_path

    with open(mesh_hash_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.write('')


    folder_path = os.path.join(os.getcwd(), temp_folder)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    os.mkdir(folder_path)



    for root, dirs, files in os.walk(input_folder):

        for file in files:
            if file.endswith(".obj"):
                input_file_path = os.path.join(input_folder, file)
                file_size = get_file_size(input_file_path)
                if file_size < 200 * 1024:  
                    shutil.copy(input_file_path, temp_folder)
                elif file_size < 1000 * 1024: 
                    decimate(input_file_path, temp_folder, ratio1)
                else:  
                    decimate(input_file_path, temp_folder, ratio2)


    for root, dirs, files in os.walk(temp_folder):

        for file in files:
            if file.endswith('.obj'):
                temp_file_path = os.path.join(root, file)
                hash_value = hash1(temp_file_path)

                file_name = os.path.splitext(file)[0]

                parts = file_name.split('&')
                if len(parts) == 2:
                    sourceFile = parts[0]
                    meshName = parts[1]
                meshName_with_underscores = meshName.replace(" ", "_")
                sourceFile_with_underscores = sourceFile.replace(" ", "_")

                with open(mesh_hash_path, 'a', encoding='utf-8', errors='ignore') as hash_file:
                    hash_file.write(f"{sourceFile_with_underscores} {meshName_with_underscores} {hash_value}\n")

def get_file_size(file_path):
    return os.path.getsize(file_path)




