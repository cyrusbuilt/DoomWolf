class Resolution:

    def __init__(self, width: int = 0, height: int = 0):
        self.width: int = width
        self.height: int = height

    def to_tuple(self) -> tuple[int, int]:
        return self.width, self.height

    def __eq__(self, other):
        return (isinstance(other, Resolution) and
                other.width == self.width and
                other.height == self.height)

    @staticmethod
    def from_dict(res_dict: dict):
        width = res_dict.get('width', 0)
        height = res_dict.get('height', 0)
        return Resolution(width, height)

    @staticmethod
    def from_tuple(res: tuple[int, int]):
        return Resolution(res[0], res[1])

    @staticmethod
    def zero():
        return Resolution()
