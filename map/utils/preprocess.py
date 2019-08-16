import re


def preprocess_coords(file_path):
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
        content = ''
        for l in all_lines:
            content += l

        p = re.compile('<name>([A-Za-z\-]+)</name>', re.IGNORECASE)
        regions = p.findall(content)

        p = re.compile('<coordinates>(.*)</coordinates>', re.IGNORECASE)
        coords = p.findall(content)
        reg_coords = {regions[i]: coords[i] for i in range(len(regions))}

        for key in reg_coords:
            all_coords = reg_coords[key]
            split_coords = [k.split(',') for k in all_coords.split(' ')]

            for i in range(len(split_coords)):
                split_coords[i].pop()
                formatted_coords = {'lng': float(split_coords[i][0]), 'lat': float(split_coords[i][1])}
                split_coords[i] = formatted_coords

            reg_coords[key] = split_coords

        return reg_coords
