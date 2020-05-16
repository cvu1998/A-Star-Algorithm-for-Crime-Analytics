import Vertex

class Line:
    
    def __init__(self, v1, v2, FirstSquare, Diagonal):
        self.Vertex1 = v1
        self.Vertex2 = v2
        self.Weight = 0
        self.FirstSquare = FirstSquare
        self.SecondSquare = False
        self.Diagonal = Diagonal

    def ComputeWeight(self):
        if not self.FirstSquare and not self.SecondSquare:
            if not self.Diagonal:
                self.Weight = 1
            else:
                self.Weight = 1.5
        elif (not self.FirstSquare and self.SecondSquare) or (self.FirstSquare and not self.SecondSquare):
            if not self.Diagonal:
                self.Weight = 1.3