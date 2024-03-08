class Path:
    def __init__(self, id, name, points):
        self.id = id
        self.name = name
        self.points = points

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "points": [point.to_dict() for point in self.points],
        }

