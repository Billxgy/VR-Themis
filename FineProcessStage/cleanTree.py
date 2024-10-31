import json
import re

def update_mesh_names(node):
    valid_components = {
        "Animator", "Animation", "3DObject", "Camera", "Light", "TextMesh", "Terrain", "Tree", "WindZone", 
        "ParticleSystem", "GUIText", "ParticleSystemForceField", "Trail", 
        "Line", "ReflectionProbe", "LightProbeGroup", "AudioSource", 
        "AudioReverbZone", "VideoPlayer", "Canvas", "Slider", "Sprite", 
        "Tilemap", "NavMeshAgent", "NavMeshObstacle"
    }

    if node.get('Name') != "3DObject" and not re.match(r'^level\d+$', node.get('Name', '')) and node.get('Name') != "data.unity3d":
        node['Name'] = "OtherObject"
        if 'Components' in node:
            for component in node['Components']:
                if component in valid_components:
                    node['Name'] = component
                    break  

    if 'Children' in node:
        children_to_keep = []
        for child in node['Children']:
            update_mesh_names(child)
            
            # pruning strategy (optional)
            if child.get('Name') == "OtherObject":
                if (not child.get('Components') and not child.get('Scripts')):
                    if 'Children' in child:
                        children_to_keep.extend(child['Children'])
                    continue            
            children_to_keep.append(child)

        node['Children'] = children_to_keep

def count_nodes(node):
    count = 1  
    if 'Children' in node:
        for child in node['Children']:
            count += count_nodes(child)  
    return count

def cleanTree(json_file_path, appName):
    # This version is only valid for LZ4 compression packaged
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_node_count = count_nodes(data.get('data.unity3d', {}))

    root = data.get('data.unity3d', {})
    update_mesh_names(root)

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    modified_node_count = count_nodes(root)

    print("Cleaning Tree for " + appName)

    print(f"Original node count: {original_node_count}")
    print(f"Modified node count: {modified_node_count}")


    return original_node_count, modified_node_count
