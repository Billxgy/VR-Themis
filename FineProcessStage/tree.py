import json
import os
from Edit_distance.TED import json_Tree_Distance
from prune import prune

def compareMono():
    pass

def load_hashes(hashes_file):
    hashes = {}
    meshSourceFile = {}
    with open(hashes_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                sourceFile, mesh_name, hash_value = parts
                meshSourceFile[mesh_name] = sourceFile
                hashes[mesh_name] = hash_value

    return meshSourceFile, hashes

def load_code_json(code_json_file):
    with open(code_json_file, 'r', encoding='utf-8', errors='ignore') as f:
        return json.load(f)

def process_node(node, meshSourceFile, hashes, code_json):
    if 'Name' not in node:
        return

    if 'Mesh' in node and node['Mesh'] is not None:
        node['Mesh'] = node['Mesh'].replace(':', '_')
        node['Mesh'] = node['Mesh'].replace(' ', '_')

        node['Mesh'] = hashes.get(node['Mesh'])

    elif 'Scripts' in node and node['Scripts'] is not None:
        scripts = node['Scripts'] 
        scripts = sorted(scripts)
        new_scripts = []
        for script in scripts:
            if script in code_json:
                code = code_json[script]
                new_scripts.append(code)
            # else:
            #     new_scripts.append(script)
        node['scripts'] = '||'.join(new_scripts)

    elif 'Components' in node and node['Components'] is not None:
        components = node['Components'] 
        new_components = sorted(components)
        node['Components'] = '||'.join(new_components)

    elif 'Children' in node and (('Mesh' not in node or node['Mesh'] is None) and ('Components' not in node or node['Components'] is None) and ('Scripts' not in node or node['Scripts'] is None)):
            children = node['Children']
            new_children = []
            for child in children:
                process_node(child, meshSourceFile, hashes, code_json)
                # if 'Name' in child and child['Name'] != 'No':
                new_children.append(child)
            node['Children'] = new_children

    elif 'Children' not in node and (('Mesh' not in node or node['Mesh'] is None) and ('Components' not in node or node['Components'] is None) and ('Scripts' not in node or node['Scripts'] is None)):
            node.clear()         

    elif 'Children' in node:
        for child in node['Children']:
            process_node(child, meshSourceFile, hashes, code_json)


def processTree(json_file_path, hashes_file, code_json_file):
    with open(json_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)

    meshSourceFile, hashes = load_hashes(hashes_file)
    code_json = load_code_json(code_json_file)

    for root_key in list(data.keys()):
        process_node(data[root_key], meshSourceFile, hashes, code_json)

    with open(json_file_path, 'w', encoding='utf-8', errors='ignore') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        

def compare_apps_in_cluster(apps_folder):

    # app_folders = [os.path.join(apps_folder, app) for app in os.listdir(apps_folder) if os.path.isdir(os.path.join(apps_folder, app))]
    comparisons = []
    
    comparisonsPairs = prune(apps_folder)
    for app_folder1, app_folder2 in comparisonsPairs:

        json_file1 = [f for f in os.listdir(app_folder1) if f.endswith('.json')][0]
        json_file1 = os.path.join(app_folder1, json_file1)

        json_file2 = [f for f in os.listdir(app_folder2) if f.endswith('.json')][0]
        json_file2 = os.path.join(app_folder2, json_file2)

        if os.path.exists(json_file1) and os.path.exists(json_file2):
            comparison_result = json_Tree_Distance(json_file1, json_file2, app_folder1, app_folder2)
            comparisons.append((os.path.basename(app_folder1), os.path.basename(app_folder2), comparison_result))
    
    return comparisons

def compareTrees(ClusterApks_folder, result_path):
    clusters = [os.path.join(ClusterApks_folder, cluster) for cluster in os.listdir(ClusterApks_folder) if os.path.isdir(os.path.join(ClusterApks_folder, cluster))]
    all_comparisons = {}
    
    for cluster in clusters:
        cluster_name = os.path.basename(cluster)
        print("Computing similarity within: ", cluster_name)
        comparisons = compare_apps_in_cluster(cluster)
        all_comparisons[cluster_name] = comparisons
    
    with open(result_path, 'w', encoding='utf-8', errors='ignore') as result_file:
        json.dump(all_comparisons, result_file, ensure_ascii=False, indent=4)

