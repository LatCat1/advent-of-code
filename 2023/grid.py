

class FiniteGrid:
    def __init__(self, data, default=None):
        if type(data) is str:
            data = data.split('\n')
        # otherwise, assume its something with len
        # and can be indexed twice
        self.height = len(data)
        self.width = len(data[0])

        self.default = default

        self.underlying_data = [ [c for c in row] for row in data ]

        self.transposed = False
        self.flip_hor   = False
        self.flip_ver   = False

    def transpose(self):
        self.transposed = not self.transposed
        self.flip_hor, self.flip_ver = self.flip_ver, self.flip_hor
        self.height, self.width = self.width, self.height

    def in_bounds(self, loc: tuple[int, int]) -> bool:
        return 0 <= loc[0] < self.height and 0 <= loc[1] < self.width

    def unsafe_get(self, loc):
        y, x = loc
        if self.transposed:
            y, x = x, y
        if self.flip_hor:
            x = self.width - x - 1
        if self.flip_ver:
            y = self.height - y - 1

        return self.underlying_data[y][x]
    
    # def rotate_right(self):
    #     self.transposed = not self.transposed
    #     self.flip_ver = not self.flip_ver
    #     self.height, self.width = self.width, self.height

    # def rotate_left(self):
    #     self.transposed = not self.transposed
    #     self.flip_ver = not self.flip_ver
    #     self.height, self.width = self.width, self.height

    # def rotate_180(self):
    #     self.flip_hor = not self.flip_hor
    #     self.flip_ver = not self.flip_ver

    def get(self, loc, default=None):
        if self.in_bounds(loc):
            return self.unsafe_get(loc)
        # prioritize the 'new' default
        if default is not None:
            return default
        if self.default is not None:
            return self.default
        assert False, f"Out of bounds at {loc} in finite grid"

    def __getitem__(self, key):
        if len(key) == 2:
            return self.get(key)
        return self.underlying_data[key]
    
    def __str__(self):
        return '\n'.join(
            ''.join(
                self[(r,c)] for c in range(self.width)
            ) for r in range(self.height)
        )