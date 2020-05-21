class Vertex:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = set()

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __str__(self):
        return "Vertex {0}, {1} ".format(self.x, self.y)
