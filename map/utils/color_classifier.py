import numpy as np
import matplotlib.colors as mcolors
from sklearn.preprocessing import minmax_scale


class ColorClassifier:

    def __init__(self):
        self.clf = None
        converter = mcolors.ColorConverter().to_rgb
        cmap = self.make_colormap(
            [converter('#98FB98'), converter('green'), 0.33, converter('#ffffe0'), converter('yellow'), 0.66,
             converter('#ffcccc'), converter('red')]
        )
        self.cmap = cmap

    def make_colormap(self, seq):
        """Return a LinearSegmentedColormap
        seq: a sequence of floats and RGB-tuples. The floats should be increasing
        and in the interval (0,1).
        """
        seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
        cdict = {'red': [], 'green': [], 'blue': []}
        for i, item in enumerate(seq):
            if isinstance(item, float):
                r1, g1, b1 = seq[i - 1]
                r2, g2, b2 = seq[i + 1]
                cdict['red'].append([item, r1, r2])
                cdict['green'].append([item, g1, g2])
                cdict['blue'].append([item, b1, b2])
        return mcolors.LinearSegmentedColormap('CustomMap', cdict)

    @staticmethod
    def scale_dataset(data):
        data = np.array(data, dtype=np.float64)
        scaled_data = minmax_scale(data)
        scaled_data = np.array([x*250 for x in scaled_data], dtype=np.float64)
        return scaled_data

    def get_colors(self, data):
        scaled_data = self.scale_dataset(data)
        colors = [mcolors.to_hex(self.cmap(int(x))) for x in scaled_data]
        return colors
