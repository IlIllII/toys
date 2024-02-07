class ColorMaps:
    def __init__(self) -> None:
        self.current_map = 0
        self.possible_colormaps = [
            "viridis",
            "plasma",
            "inferno",
            "magma",
            "cividis",
            "twilight",
            "twilight_shifted",
            "hsv",
            "Pastel1",
            "Pastel2",
            "Paired",
            "Accent",
            "Dark2",
            "Set1",
            "Set2",
            "Set3",
            "tab10",
            "tab20",
            "tab20b",
            "tab20c",
            "flag",
            "prism",
            "ocean",
            "gist_earth",
            "terrain",
            "gist_stern",
            "gnuplot",
            "gnuplot2",
            "CMRmap",
            "cubehelix",
            "brg",
            "gist_rainbow",
            "rainbow",
            "jet",
            "nipy_spectral",
            "gist_ncar",
            "viridis_r",
            "plasma_r",
        ]

    def get_map(self):
        return self.possible_colormaps[self.current_map % len(self.possible_colormaps)]

    def next_map(self):
        self.current_map += 1

    def previous_map(self):
        self.current_map -= 1
