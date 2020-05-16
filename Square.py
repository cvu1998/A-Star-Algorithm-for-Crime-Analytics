import Line
import Vertex

class Square(object):

    def __init__(self, v1, v2, v3, v4, OverThreshold):
        self.Vertex1 = v1
        self.Vertex2 = v2
        self.Vertex3 = v3
        self.Vertex4 = v4

        self.OverThreshold = OverThreshold

        self.Line1 = Line.Line(self.Vertex1, self.Vertex2, self.OverThreshold, False)
        self.Line2 = Line.Line(self.Vertex2, self.Vertex4, self.OverThreshold, False)
        self.Line3 = Line.Line(self.Vertex4, self.Vertex3, self.OverThreshold, False)
        self.Line4 = Line.Line(self.Vertex3, self.Vertex1, self.OverThreshold, False)
        self.Line5 = Line.Line(self.Vertex1, self.Vertex4, self.OverThreshold, True)
        self.Line6 = Line.Line(self.Vertex2, self.Vertex3, self.OverThreshold, True)
        
    def getLines(self):
        return [self.Line1, self.Line2, self.Line3, self.Line4, self.Line5, self.Line6]


