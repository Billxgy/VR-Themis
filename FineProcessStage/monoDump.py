import os
import json


def dumpMono(code_folder, code_json_file, mono_folder_path):
    class_definitions = {}

    for filename in os.listdir(mono_folder_path):
        if filename.endswith('.cs'):
            class_name = filename[:-3]
            file_path = os.path.join(mono_folder_path, filename)
            # class_name, match = extract_class_from_file(file_path)
            class_definitions[class_name] = file_path  


    if class_definitions:
        with open(code_json_file, 'w', encoding='utf-8') as json_file:
            json.dump(class_definitions, json_file, ensure_ascii=False, indent=4)
