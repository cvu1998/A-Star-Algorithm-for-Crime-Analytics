# -------------------------------------------------------
# Assignment 1
# Written by Cong-Vinh Vu, Student ID: 40061685
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------

import Line
import Vertex

class Square(object):

    # A square contains 4 vertices and 6 lines
    def __init__(self, v1, v2, v3, v4, OverThreshold):
        self.Vertex1 = v1
        self.Vertex2 = v2
        self.Vertex3 = v3
        self.Vertex4 = v4

        self.OverThreshold = OverThreshold

        self.Line1 = Line.Line(self.Vertex1, self.Vertex2, self.OverThreshold, False)
        self.Line2 = Line.Line(self.Vertex2, self.Vertex4, self.OverThreshold, False)
        self.Line3 = Line.Line(self.Vertex3, self.Vertex4, self.OverThreshold, False)
        self.Line4 = Line.Line(self.Vertex3, self.Vertex1, self.OverThreshold, False)
        self.Line5 = Line.Line(self.Vertex1, self.Vertex4, self.OverThreshold, True)
        self.Line6 = Line.Line(self.Vertex2, self.Vertex3, self.OverThreshold, True)
        
    def getLines(self):
        return [self.Line1, self.Line2, self.Line3, self.Line4, self.Line5, self.Line6]

    def isInside(self, vertex):
        if (self.Vertex1 == vertex or
            self.Vertex2 == vertex or
            self.Vertex3 == vertex or
            self.Vertex4 == vertex):
            return False
        elif (vertex.x < self.Vertex4.x and vertex.y < self.Vertex4.y and
       vertex.x > self.Vertex1.x and vertex.y > self.Vertex1.y):
            return True
        return False