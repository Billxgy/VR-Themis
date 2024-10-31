import json

def sort_nodes(node):
    if isinstance(node, list):
        dict_items = [item for item in node if isinstance(item, dict)]
        non_dict_items = [item for item in node if not isinstance(item, dict)]
        
        dict_items.sort(key=lambda x: x.get('Name', ''))

        sorted_node = dict_items + non_dict_items
        node[:] = sorted_node  

        for item in dict_items:
            if 'Children' in item:
                sort_nodes(item['Children'])

def read_and_sort_json(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    sort_nodes(data)
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def alignJson(jsonPath):
    read_and_sort_json(jsonPath, jsonPath)
