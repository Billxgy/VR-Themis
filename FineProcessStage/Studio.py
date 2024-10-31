import os
import json
import shutil
import subprocess
import re
import zipfile
from Mesh_Hash.processHash import processHash as hash
from monoDump import dumpMono as dMono
from tree import processTree
from tree import compareTrees
from alignJson import alignJson
from cleanTree import cleanTree

def getApksOfClusters(input_apps_folder, Clusters_path, ClusterApks_folder, asset_studio_path, il2cppdumper_path, dnSpy_path, unzip_temp_folder):
    with open(Clusters_path, 'r', encoding='utf-8', errors='ignore') as f:
        clusters = json.load(f)

    response = ""
    
    for cluster_name, apk_names in clusters.items():

        cluster_folder_path = os.path.join(ClusterApks_folder, cluster_name)
        if not os.path.exists(cluster_folder_path):
            os.makedirs(cluster_folder_path)
        

        for apk_name in apk_names:
            apk_file_name = f"{apk_name}.apk"
            apk_source_path = os.path.join(input_apps_folder, apk_file_name)
            

            if os.path.exists(apk_source_path):
                output_path = cluster_folder_path 
                command = f'"{asset_studio_path}" "{apk_source_path}" "{output_path}"'
                
                try:
                    subprocess.run(command, shell=True, check=True)
        
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {apk_file_name}: {e}")

                apk_info_path = os.path.join(output_path, apk_name)

                response1 = getCodes(apk_source_path, apk_info_path, il2cppdumper_path, dnSpy_path, unzip_temp_folder)
                response += response1
            else:
                print(f"APK file {apk_file_name} not found in {input_apps_folder}")

    print("All clusters have been processed.")
    return response


def getCodes(apk_source_path, apk_info_path, il2cppdumper_path, dnSpy_path, unzip_temp_folder):
    original_path = os.getcwd()

    response = ""

    apk_name = os.path.basename(apk_source_path)
    unzip_dir = os.path.join(unzip_temp_folder, apk_name.replace('.apk', ''))

    with zipfile.ZipFile(apk_source_path, 'r') as apk_zip:
        apk_zip.extractall(unzip_dir)


    global_metadata_path = os.path.join(unzip_dir, 'assets', 'bin', 'Data', 'Managed', 'Metadata', 'global-metadata.dat')
    libil2cpp_path = None
    lib_dir = os.path.join(unzip_dir, 'lib')

    for root, dirs, files in os.walk(lib_dir):
        for file in files:
            if file == 'libil2cpp.so':
                libil2cpp_path = os.path.join(root, file)
                break
        if libil2cpp_path:
            break


    if os.path.exists(global_metadata_path) and libil2cpp_path:
        os.chdir(il2cppdumper_path)

        temp_output_dir = os.path.join(il2cppdumper_path, 'temp_output')
        os.makedirs(temp_output_dir, exist_ok=True)

        command = f'Il2CppDumper.exe "{libil2cpp_path}" "{global_metadata_path}" "{temp_output_dir}"'
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(input=b'\n')

        dump_cs_path = os.path.join(temp_output_dir, 'dump.cs')
        code_output_path = os.path.join(apk_info_path, 'Code')
        os.makedirs(code_output_path, exist_ok=True)

        if os.path.exists(dump_cs_path):
            shutil.move(dump_cs_path, code_output_path)
        else:
            print(f"[Wrong]: dump.cs file not found")
            response += ("[Wrong] il2cppDumper failed in " + apk_name)

        shutil.rmtree(temp_output_dir)

    else:
        assembly_csharp_path = os.path.join(unzip_dir, 'assets', 'bin', 'Data', 'Managed', 'Assembly-CSharp.dll')

        code_output_path = os.path.join(apk_info_path, 'Code')
        os.makedirs(code_output_path, exist_ok=True)  

        if os.path.exists(assembly_csharp_path):

            os.chdir(dnSpy_path)

            command = f'dnSpy.Console.exe "{assembly_csharp_path}" -o "{code_output_path}"'
            subprocess.run(command)

            for root, dirs, files in os.walk(code_output_path):
                for file in files:
                    if file.endswith('.cs'):
                        source_file = os.path.join(root, file)
                        
                        if file not in os.listdir(code_output_path):
                            shutil.move(source_file, code_output_path)
                        else:
                            print(f"File '{file}' already in '{code_output_path}' , pass it! ")         

            for root, dirs, files in os.walk(code_output_path, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        os.rmdir(dir_path)
                    except OSError:
                        pass
            
            if not any(file.endswith('.cs') for file in os.listdir(code_output_path)):
                response += ("[Wrong] Something wrong of Mono Reverse found in " + apk_name)

        else:
            print(f"[Wrong]: In APK {apk_name}, cannot found global-metadata.dat, libil2cpp.so and Assembly-CSharp.dll")
            response += ("[Wrong] Non of global-metadata.dat, libil2cpp.so and Assembly-CSharp.dll are found in " + apk_name)

            os.makedirs(code_output_path, exist_ok=True)

            no_code_path = os.path.join(code_output_path, 'NoCode')
            os.makedirs(no_code_path, exist_ok=True)

    shutil.rmtree(unzip_dir)

    os.chdir(original_path)

    return response


def compareClusters(ClusterApks_folder):
    response2 = "\n"
    for cluster in os.listdir(ClusterApks_folder):
        cluster_path = os.path.join(ClusterApks_folder, cluster)
        
        if os.path.isdir(cluster_path):

            for app_folder in os.listdir(cluster_path):
                print("In Progress: ", os.path.basename(app_folder))
                app_folder_path = os.path.join(cluster_path, app_folder)
                
                if os.path.isdir(app_folder_path):

                    compare_folder = os.path.join(app_folder_path, 'compare')
                    os.makedirs(compare_folder, exist_ok=True)

                    code_folder = os.path.join(app_folder_path, 'Code')
                    mesh_folder = os.path.join(app_folder_path, 'Mesh')
                    json_file = next((f for f in os.listdir(app_folder_path) if f.endswith('.json')), None)
                    json_file_path = os.path.join(app_folder_path, json_file) if json_file else None
                    alignJson(json_file_path)


                    if os.path.isdir(mesh_folder):
                        hashes_file = os.path.join(compare_folder, 'hashes.txt')
                        getHash(mesh_folder, hashes_file)


                    if os.path.isdir(code_folder):
                        code_json_file = os.path.join(compare_folder, 'code.json')
                        codeHead(code_folder, code_json_file)
 
                    if json_file_path:
                        original_node_count, modified_node_count = cleanTree(json_file_path, os.path.basename(app_folder))
                        folderName = os.path.basename(app_folder)
                        response2 += folderName + " has " + str(original_node_count) + " / " + str(modified_node_count) + " nodes! \n"
                        if (modified_node_count > 1500):

                            if os.path.exists(app_folder):
                                shutil.rmtree(app_folder)
                                
                        else:
                            processTree(json_file_path, hashes_file, code_json_file)

    result_path = "results.txt"
    compareTrees(ClusterApks_folder, result_path)
    return response2


def getHash(mesh_folder, hashes_file):
    hash(mesh_folder, hashes_file)

def codeHead(code_folder, code_json_file):

    no_code_folder_count = 0
    dump_file_count = 0
    dump_file_path = ""


    for root, dirs, files in os.walk(code_folder):

        if "NoCode" in dirs:
            no_code_folder_count += 1
        

        dump_files = [file for file in files if file == "dump.cs"]
        dump_file_count += len(dump_files)
        if dump_files:
            dump_file_path = os.path.join(root, "dump.cs")


    if no_code_folder_count == 1:
        data = {"NoCode": "NoCode"}

        with open(code_json_file, 'w', encoding='utf-8', errors='ignore') as f:
            json.dump(data, f)

    elif dump_file_count == 1:
        il2cpp_folder_path = os.path.join(code_folder, 'IL2CPP')
        os.makedirs(il2cpp_folder_path, exist_ok=True) 
        dumpIL2CPP(dump_file_path, code_json_file, il2cpp_folder_path)
    elif dump_file_count >= 1:
        print("[Wrong] More than one dump.cs file!")
    else:

        mono_folder_path = os.path.join(code_folder, 'Mono')
        os.makedirs(mono_folder_path, exist_ok=True)  

        for filename in os.listdir(code_folder):
            if filename.endswith('.cs'):
               
                source_file_path = os.path.join(code_folder, filename)

                shutil.move(source_file_path, mono_folder_path)
        dMono(code_folder, code_json_file, mono_folder_path)

def extract_classes(content):
    content += '\n'
    pattern = r'(\w+)\sclass\s(\w+)\s:\s' 
    matches = {}

    for match in re.finditer(pattern, content):
        class_name = match.group(2) 

        line_start = content.rfind('\n', 0, match.start()) + 1
        if line_start == -1:
            line_start = 0

        end_index = match.end()
        while True:
            end_index = content.find('}', end_index)
            if end_index == -1:
                break
            if content[end_index + 1] in {'\n', '\r'} and content[end_index - 1] in {'\n', '\r'}:
                break
            end_index += 1

        result = content[line_start:end_index + 1].strip()
        matches[class_name] = result

    return matches

def dumpIL2CPP(dump_file_path, code_json_file, il2cpp_folder_path):
    class_definitions = {}

    with open(dump_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        matches = extract_classes(content)
        
        for class_name, match in matches.items(): 
            cs_file_path = os.path.join(il2cpp_folder_path, f"{class_name}.cs")
            
            with open(cs_file_path, 'w', encoding='utf-8', errors='ignore') as class_file:
                class_file.write(match)
                
            class_definitions[class_name] = cs_file_path

    if class_definitions:
        with open(code_json_file, 'w', encoding='utf-8', errors='ignore') as json_file:
            json.dump(class_definitions, json_file, ensure_ascii=False, indent=4)


