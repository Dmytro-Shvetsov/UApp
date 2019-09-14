import re
from .color_classifier import ColorClassifier
from map.models import Region


def preprocess_coords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
        content = ''
        for l in all_lines:
            content += l

        p = re.compile('<name>([A-Za-z]+)</name>', re.IGNORECASE)
        regs_names = p.findall(content)
        # p = re.compile(r'<coordinates>(\s*([0-9]+.[0-9]+.*[0-9]+.[0-9]+\s*)+)</coordinates>', re.IGNORECASE)
        p = re.compile(r'<coordinates>(.*)</coordinates>', re.IGNORECASE)

        coords = p.findall(content)

        regs_info = {regs_names[i]: {'coords': coords[i], 'hex_color': ''} for i in range(len(regs_names))}
        all_regions_marker_counts = {region_name: 0 for region_name in regs_names}
        for region_name in regs_info:
            # cleaning each region's coordinates
            all_coords = regs_info[region_name]['coords'].strip()
            split_coords = [k.split(',') for k in all_coords.split(' ')]
            for i in range(len(split_coords)):
                split_coords[i].pop()
                formatted_coords = {'lng': float(split_coords[i][0].strip()), 'lat': float(split_coords[i][1].strip())}
                split_coords[i] = formatted_coords

            regs_info[region_name]['coords'] = split_coords
            # getting a total of all markers of each region
            current_region = Region.objects.get(name=region_name)
            current_region_markers_count = len(current_region.marker_set.all())
            all_regions_marker_counts[region_name] = current_region_markers_count

        clf = ColorClassifier()
        marker_counts_set = [all_regions_marker_counts[key] for key in all_regions_marker_counts]
        marker_counts_set = clf.scale_dataset(marker_counts_set)
        colors = clf.get_colors(marker_counts_set)
        i = 0
        for region_name in regs_info:
            regs_info[region_name]['hex_color'] = colors[i]
            i += 1
        return regs_info


