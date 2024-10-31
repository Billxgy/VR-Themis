import json
import os
import zss
import numpy as np
from functools import partial
from Edit_distance.compareMonoBehaviour import compare_code_structures


def build_weird_tree(json_node):
    name = json_node.get("Name", "_null_")
    mesh = json_node.get("Mesh", "_null_")
    if name is None:
        name = "_null_"
    if mesh is None:
        mesh = "_null_"

    components = json_node.get("Components", [])
    if len(components) == 0:
        components = "_null_"
    else:
        components = "||".join(components)

    scripts = json_node.get("Scripts", [])
    if len(scripts) == 0:
        scripts = "_null_"
    else:
        scripts = "||".join(scripts)
    
    label = name + "?" + mesh + "?" + components + "?" + scripts

    root = WeirdNode(label)
    children = json_node.get("Children", [])
    for child in children:
        child_node = build_weird_tree(child)
        root.addkid(child_node)
    return root
    
    

def json_Tree_Distance(json1, json2, app_folder1, app_folder2):
    with open(json1, 'r', encoding='utf-8', errors='ignore') as f1, open(json2, 'r', encoding='utf-8', errors='ignore') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    root_key1 = list(data1.keys())[0]
    root_key2 = list(data2.keys())[0]
    
    tree1 = build_weird_tree(data1[root_key1])
    tree2 = build_weird_tree(data2[root_key2])
    
    distance = TreeEditDistance_All(tree1, tree2, app_folder1, app_folder2)
    return distance

def read_code_from_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    return ""

def compareCodes(scripts1, scripts2, app_folder1, app_folder2):

    paths1 = scripts1.split('||')
    paths2 = scripts2.split('||')

    if scripts1 == "_null_": paths1 = []
    if scripts2 == "_null_": paths2 = []

    intersection_scripts, union_scripts = 0, 0

    if len(paths1) == 0 and len(paths2) == 0:
        return 0, 0
    elif len(paths1) == 0:
        return 0, len(paths1)
    elif len(paths2) == 0:
        return 0, len(paths2)
    else:
        if len(paths1) < len(paths2):
            shorter_paths = paths1
            longer_paths = paths2
        else:
            shorter_paths = paths2
            longer_paths = paths1
        
        intersection_scripts = 0
        union_scripts = 0

        for short_path in shorter_paths:
            max_similarity = 0.0
            
            for long_path in longer_paths:
                if short_path and long_path:  
                    similarity = compare_code_structures(short_path, long_path, app_folder1, app_folder2)
                    if similarity > max_similarity:
                        max_similarity = similarity

            if max_similarity > 0.8:
                intersection_scripts += 1
    union_scripts = intersection_scripts + (len(shorter_paths) - intersection_scripts) + (len(longer_paths) - intersection_scripts)

    return intersection_scripts, union_scripts


def components_Jaccard_distance (string1, string2):
    set1 = set(filter(bool, string1.split("||")))
    set2 = set(filter(bool, string2.split("||")))

    if string1 == "_null_": set1 = set()
    if string2 == "_null_": set2 = set()
    
    if len(set1) == 0 and len(set2) == 0:
        return 0, 0
    else:
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection, union


def custom_distance(node1, node2, param1, param2):

    value1 = node1
    value2 = node2

    if ((value1 == "" or value1 is None) and (value2 == "" or value2 is None)):
        return 0
    elif (value1 == "" or value1 is None or value2 == "" or value2 is None):
        return 1

    parts1 = value1.split('?')
    parts2 = value2.split('?')
    
    if len(parts1) == 4:
        name1 = parts1[0]
        mesh1 = parts1[1]
        components1 = parts1[2]
        scripts1 = parts1[3]
    else:
        print(len(parts1), name1,mesh1,components1,scripts1)
        print("[Wrong]: Lack of Information, not exact 4 parts")

    if len(parts2) == 4:
        name2 = parts2[0]
        mesh2 = parts2[1]
        components2 = parts2[2]
        scripts2 = parts2[3]
    else:
        print(len(parts2), name2,mesh2,components2,scripts2)
        print("[Wrong]: Lack of Information, not exact 4 parts")

    distance = 0
    if name1 == name2:
        if not ((mesh1 != "_null_" and mesh2 != "_null_" and mesh1 == mesh2) or (mesh1 == "_null_" and mesh2 == "_null_")):
            distance = 1.0

        else:
            intersection_components, union_components = components_Jaccard_distance(components1, components2)
            intersection_scripts, union_scripts = compareCodes(scripts1, scripts2, param1, param2)
            distance = 1 - ((intersection_components + intersection_scripts) / (union_components + union_scripts)) if union_components + union_scripts > 0 else 0
    else:
        distance = 1.0

    return distance


class WeirdNode(object):

    def __init__(self, label):
        self.my_label = label
        self.my_children = list()

    @staticmethod
    def get_children(node):
        return node.my_children

    @staticmethod
    def get_label(node):
        return node.my_label

    def addkid(self, node, before=False):
        if before:  self.my_children.insert(0, node)
        else:   self.my_children.append(node)
        return self
    
    def size(self):
        return 1 + sum(child.size() for child in self.my_children)
    
    

def TreeEditDistance_All(Tree1, Tree2, app_folder1, app_folder2):
    param1, param2 = app_folder1, app_folder2
    custom_distance_with_param = partial(custom_distance, param1=param1, param2=param2)
    try:
        dist = zss.simple_distance(
            Tree1, Tree2, WeirdNode.get_children, WeirdNode.get_label, custom_distance_with_param
        )
        
        num_nodes_tree1 = Tree1.size()
        num_nodes_tree2 = Tree2.size()
    
        max_nodes = max(num_nodes_tree1, num_nodes_tree2)
        
        sim = 1 - (dist / max_nodes) if max_nodes > 0 else 0 

        app_folder1_name = os.path.basename(app_folder1)
        app_folder2_name = os.path.basename(app_folder2)
        
        if (sim >= 0.6):
            print(f"Distance between {app_folder1_name} and {app_folder2_name}: {dist}, Max Nodes: {max_nodes}, Similarity: {sim}")
        return sim
    except np.core._exceptions._ArrayMemoryError as e:
        print(f"Memory allocation error: {e}")