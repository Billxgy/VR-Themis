import json
import os
import re
from collections import defaultdict
import numpy as np

def extract_members_of_Mono_code(class_code):
    # Regex patterns for fields, properties, and methods
    field_pattern = (
        r'(?P<modifiers>\s*(public|private|protected|internal|static|readonly|volatile|new)\s+)'
        r'(?P<type>(?:global::)?(?:\w+\.)*\w+(\s*<[^>]+>)?)\s+(?P<name>\w+)\s*(=\s*[^;]*)?\s*;'
    )
    property_pattern = (
        r'(?P<modifiers>public|private|protected|internal|static)\s*'
        r'(?P<type>\w+(\s*<[^>]+>)?)\s+(?P<name>\w+)\s*{[^}]*?(get\s*({[^}]*}|;))[^}]*?(set\s*({[^}]*}|;))?[^}]*}'
    )
    method_pattern = (
        r'(?P<modifiers>public|private|protected|internal|static|virtual|override|new)\s*'
        r'(?P<returnType>\w+(\s*<[^>]+>)?)\s+(?P<name>\w+)\s*\([^\)]*\)'
    )

    members = {
        'fields': defaultdict(int),
        'properties': defaultdict(int),
        'methods': defaultdict(int),
    }

    # Extract fields
    for match in re.finditer(field_pattern, class_code):
        type_ = re.sub(r'global::(?:\w+\.)*', '', match.group("type"))
        modifiers = match.group("modifiers").strip() if match.group("modifiers") else ""
        key = f"{modifiers} {type_}".strip()
        members['fields'][key] += 1

    # Extract properties
    for match in re.finditer(property_pattern, class_code, re.DOTALL):
        modifiers = match.group("modifiers").strip() if match.group("modifiers") else ""
        type_ = match.group("type").strip()
        key = f"{modifiers} {type_}".strip()
        members['properties'][key] += 1

    # Extract methods
    for match in re.finditer(method_pattern, class_code):
        modifiers = match.group("modifiers").strip() if match.group("modifiers") else ""
        return_type = match.group("returnType").strip()
        key = f"{modifiers} {return_type}".strip()
        members['methods'][key] += 1

    return members

def extract_members_of_IL2CPP_code(class_code):
    # Regex patterns for fields, properties, and methods
    field_pattern = r'(?P<modifiers>public|private|protected|internal|static|readonly|volatile|new)\s*(?P<type>\w+(\s*<[^>]+>)?)\s+(?P<name>\w+)\s*;'
    property_pattern = r'(?P<modifiers>public|private|protected|internal|static)\s*(?P<type>\w+(\s*<[^>]+>)?)\s+(?P<name>\w+)\s*{.*?}'
    method_pattern = r'(?P<modifiers>public|private|protected|internal|static|virtual|override|new)\s*(?P<returnType>\w+(\s*<[^>]+>)?)\s+(?P<name>\w+)\s*\([^\)]*\)'

    members = {
        'fields': defaultdict(int),
        'properties': defaultdict(int),
        'methods': defaultdict(int),
    }

    # Extract fields
    for match in re.finditer(field_pattern, class_code):
        modifiers = match.group("modifiers").strip() if match.group("modifiers") else ""
        type_ = match.group("type").strip()
        key = f"{modifiers} {type_}".strip()
        members['fields'][key] += 1

    # Extract properties
    for match in re.finditer(property_pattern, class_code):
        modifiers = match.group("modifiers").strip() if match.group("modifiers") else ""
        type_ = match.group("type").strip()
        key = f"{modifiers} {type_}".strip()
        members['properties'][key] += 1

    # Extract methods
    for match in re.finditer(method_pattern, class_code):
        modifiers = match.group("modifiers").strip() if match.group("modifiers") else ""
        return_type = match.group("returnType").strip()
        key = f"{modifiers} {return_type}".strip()
        members['methods'][key] += 1

    return members

def read_code_from_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()

def process_code(code_path):
    code = read_code_from_file(code_path)
    if 'Mono' in code_path:
        return extract_members_of_Mono_code(code)
    elif 'IL2CPP' in code_path:
        return extract_members_of_IL2CPP_code(code)
    else:
        return None

def getCodeompletePath(code, app_folder):
    json_file_path = os.path.join(app_folder, "compare", "code.json")

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    if code in data:
        code_new = data[code]
    else:
        code_new = None 

    return code_new

def compare_code_structures(code1, code2, app_folder1, app_folder2):
    code1_new = getCodeompletePath(code1, app_folder1)
    code2_new = getCodeompletePath(code2, app_folder2)
    if code1_new is None and code2_new is None:
        return 1
    elif code1_new is None:
        return 0
    elif code2_new is None:
        return 0
    else:
        members1 = process_code(code1_new)
        members2 = process_code(code2_new)


        comparison_result = {
            'fields': {},
            'properties': {},
            'methods': {},
        }
        if members1 is not None and members2 is not None:
            # Compare fields
            if members1['fields'] is not None and members2['fields'] is not None:
                for name in set(members1['fields'].keys()).union(members2['fields'].keys()):
                    count1 = members1['fields'].get(name, 0)
                    count2 = members2['fields'].get(name, 0)
                    comparison_result['fields'][name] = (count1, count2)

            # Compare properties
            if members1['properties'] is not None and members2['properties'] is not None:
                for name in set(members1['properties'].keys()).union(members2['properties'].keys()):
                    count1 = members1['properties'].get(name, 0)
                    count2 = members2['properties'].get(name, 0)
                    comparison_result['properties'][name] = (count1, count2)

            # Compare methods
            if members1['methods'] is not None and members2['methods'] is not None:
                for name in set(members1['methods'].keys()).union(members2['methods'].keys()):
                    count1 = members1['methods'].get(name, 0)
                    count2 = members2['methods'].get(name, 0)
                    comparison_result['methods'][name] = (count1, count2)

            return print_comparison_results(comparison_result)
    return 0

def calculate_cosine_similarity(counts1, counts2):
    if all(value == 0 for value in counts1.values()) or all(value == 0 for value in counts2.values()):
        return 0.0
    
    # Create vectors for cosine similarity calculation
    all_keys = set(counts1.keys()).union(set(counts2.keys()))
    vector1 = np.array([counts1.get(key, 0) for key in all_keys])
    vector2 = np.array([counts2.get(key, 0) for key in all_keys])
    
    # Calculate cosine similarity
    cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cosine_similarity

def print_comparison_results(comparison):
    # Aggregate counts for overall cosine similarity
    total_counts1 = defaultdict(int)
    total_counts2 = defaultdict(int)

    for name, counts in comparison['fields'].items():
        total_counts1[name] = counts[0]
        total_counts2[name] = counts[1]

    for name, counts in comparison['properties'].items():
        total_counts1[name] = counts[0]
        total_counts2[name] = counts[1]

    for name, counts in comparison['methods'].items():
        total_counts1[name] = counts[0]
        total_counts2[name] = counts[1]

    # Calculate overall cosine similarity
    overall_similarity = calculate_cosine_similarity(total_counts1, total_counts2)

    # print(f"\nOverall Cosine Similarity: {overall_similarity:.4f}")

    return overall_similarity
