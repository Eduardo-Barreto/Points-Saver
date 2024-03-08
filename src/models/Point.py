class Point:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z, "r": self.r}

