import mmh3

def hash1(input_path):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    vertice_ori = []
    face_ori = []
    index_mapping = {}

    for line in lines:
        if line.startswith('v '):
            parts = line.split()
            if len(parts) >= 4: 
                x, y, z = map(float, parts[1:4])
                vertice_ori.append((x, y, z))
    
        if line.startswith('f '):
            parts = line.split()
            if len(parts) >= 4:  
                face_indices = []
                for part in parts[1:]: 
                    vertex_index = int(part.split('/')[0]) - 1  
                    face_indices.append(vertex_index)
                face_ori.append(face_indices)


    vertice_sorted = sorted(vertice_ori, key=lambda p: (p[0], p[1], p[2]))

    for i, point in enumerate(vertice_sorted):
        original_index = vertice_ori.index(point)

        index_mapping[original_index] = i


    face_sorted = []


    for face_indices in face_ori:
        sorted_indices = []
        for original_index in face_indices:
            try:
                sorted_indices.append(index_mapping[original_index] + 1)
            except KeyError:
                pass
        sorted_indices = sorted(sorted_indices)
        face_sorted.append(sorted_indices)

    face_sorted.sort()
    face_sorted_str = str(face_sorted)

    hash_value = mmh3.hash(face_sorted_str)

    return hash_value



