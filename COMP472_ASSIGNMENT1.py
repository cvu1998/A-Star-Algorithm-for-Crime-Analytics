# -------------------------------------------------------
# Assignment 1
# Written by Cong-Vinh Vu, Student ID: 40061685
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------

import copy
import math

import matplotlib
from matplotlib import pyplot
import numpy
import shapefile
import time

import Line
import Square
import Vertex

# Heuristic function, uses Euclidean distance as it ensures admissibility for A algorithm (h(n) <= h*(n))
def heuristsicFunction(currentVertex, end, weight):
    distance = math.sqrt((currentVertex.x - end.x ) * (currentVertex.x - end.x) + (currentVertex.y - end.y ) * (currentVertex.y - end.y))
    return distance


def runProgram():
    EndProgram = False
    while not EndProgram:
        sf = shapefile.Reader("crime_dt.shp", encoding='ISO-8859-1')

        # Loop to ensure valid step for grid size. (Can not be negative) 
        isValid = False
        step = 0.002
        while not isValid:
            try:
                step = float(input("Enter the size of a grid: "))
            except:
                    print("Input [{}] is invalid!\n".format(step))
                    isValid = False
            else:
                if step <= 0:
                    print("Input [{}] is invalid!\n".format(step))
                    isValid = False
                else:
                    isValid = True

        # Loop to ensure valid threshold. (Can not be negative or over 100%) 
        isValid = False
        threshold = 0
        while not isValid:
            try:
                threshold = int(input("Enter a threshold between 0% and 100%: "))
            except:
                    print("Input [{}] is invalid!\n".format(threshold))
                    isValid = False
            else:
                if threshold < 0 or threshold > 100:
                    print("Input [{}] is invalid!\n".format(threshold))
                    isValid = False
                else:
                    isValid = True

        XAxis = numpy.arange(sf.bbox[0], sf.bbox[2] + step, step)
        YAxis = numpy.arange(sf.bbox[1], sf.bbox[3] + step, step)

        shapeRecords = sf.shapeRecords()
        XValues = numpy.zeros(shape=(len(shapeRecords)),)
        YValues = numpy.zeros(shape=(len(shapeRecords)),)

        for i in range(len(shapeRecords)):
            x = shapeRecords[i].shape.__geo_interface__["coordinates"][0]
            y = shapeRecords[i].shape.__geo_interface__["coordinates"][1]
            XValues[i] = x
            YValues[i] = y

        H, xedges, yedges = numpy.histogram2d(XValues, YValues, bins=(XAxis, YAxis))
        H = H.T

        print("Average: {}".format(numpy.average(H)))
        print("Standard Deviation: {}".format(numpy.std(H)))
        ThresholdValue = numpy.percentile(H, threshold)

        # Make an histogram with binary colors (blue and red), red being equal or over the threshold, blue being under the threshold
        bounds = [0., ThresholdValue, numpy.amax(H)]
        cmap = matplotlib.colors.ListedColormap([[0, 0.2, 0.6], [1, 0, 0]])
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        pyplot.figure()
        pyplot.imshow(H, cmap=cmap, norm=norm, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

        # Make a list of vertices for later use in creating a list of squares and lines
        lenX = len(xedges)
        lenY = len(yedges)
        vertices = []
        for i in range(lenX):
            for j in range(lenY):
                vertices.append(Vertex.Vertex(xedges[i], yedges[j]))

        # Make a list of squares to to compute the weight of each edge or line
        quads = []
        for i in range(lenX - 1):
            for j in range(lenY - 1):
                HighCrime = True
                if H[j][i] < ThresholdValue:
                    HighCrime = False
                quad = Square.Square(vertices[j + (i * lenX)], vertices[j + (i * lenX) + 1], 
                                     vertices[j + (i * lenX) + lenX], vertices[j + (i * lenX) + lenX + 1], HighCrime)
                quads.append(quad)

        BBXEdge0X = min(xedges)
        BBXEdge0Y = min(yedges)

        BBXEdge1X = max(xedges)
        BBXEdge1Y = min(yedges)

        BBXEdge2X = max(xedges)
        BBXEdge2Y = max(yedges)

        BBXEdge3X = min(xedges)
        BBXEdge3Y = max(yedges)

        # Remove edges on the boundary
        BoundariesLines = set()
        for i in range(len(xedges) - 1):
            v1 = Vertex.Vertex(xedges[i], BBXEdge0Y)
            v2 = Vertex.Vertex(xedges[i + 1], BBXEdge0Y)
            v3 = Vertex.Vertex(xedges[i], BBXEdge3Y)
            v4 = Vertex.Vertex(xedges[i + 1], BBXEdge3Y)
            BoundariesLines.add((v1, v2))
            BoundariesLines.add((v3, v4))

            v5 = Vertex.Vertex(BBXEdge1X, yedges[i])
            v6 = Vertex.Vertex(BBXEdge1X, yedges[i + 1])
            v7 = Vertex.Vertex(BBXEdge3X, yedges[i])
            v8 = Vertex.Vertex(BBXEdge3X, yedges[i + 1])
            BoundariesLines.add((v5, v6))
            BoundariesLines.add((v7, v8))

        # Initialize the edges or lines
        lines = {}
        for i in quads:
            for j in i.getLines():
                if (j.Vertex1, j.Vertex2) in lines:
                    lines[(j.Vertex1, j.Vertex2)].SecondSquare = j.FirstSquare
                elif (j.Vertex2, j.Vertex1) in lines:
                    lines[(j.Vertex2, j.Vertex1)].SecondSquare = j.FirstSquare
                else:
                    lines[(j.Vertex1, j.Vertex2)] = j

        # Set the children for each vertex
        isAChild = False
        for i in vertices:
            for j in lines:
                childIndex = -1
                index = 0
                for k in j:
                    index += 1
                    if i == k:
                        isAChild = True
                        childIndex = index - 1
                if isAChild:
                    if childIndex == 0:
                        i.children.add(list(j)[1])
                    elif childIndex == 1:
                        i.children.add(list(j)[0])
                isAChild = False

        # Loop to ensure valid input for starting and ending coordinates. (Inside the map)
        isValid = False
        while not isValid:
            try:
                x1 = float(input("Enter the X starting coordinate: "))
                y1 = float(input("Enter the Y starting coordinate: "))
                x2 = float(input("Enter the X ending coordinate: "))
                y2 = float(input("Enter the Y ending coordinate: "))
            except:
                    print("Inputs are invalid!\n")
                    isValid = False
            else:
                if (x1 < BBXEdge0X or x2 < BBXEdge0X or y1 < BBXEdge0Y or y2 < BBXEdge0Y or
                    x1 > BBXEdge2X or x2 > BBXEdge2X or y1 > BBXEdge2Y or y2 > BBXEdge2Y):
                    print("Inputs must be between ({0}, {1}), ({2}, {3}), ({4}, {5}), ({6}, {7})!\n"
                          .format(BBXEdge0X, BBXEdge0Y, BBXEdge1X, BBXEdge1Y, BBXEdge2X, BBXEdge2Y, BBXEdge3X, BBXEdge3Y))
                    isValid = False
                else:
                    isValid = True

        # Initialize the vertices using the input coordinates
        start = Vertex.Vertex(x1, y1)
        end = Vertex.Vertex(x2, y2)

        for i in quads:
            if i.isInside(start):
                start = i.Vertex1
            if i.isInside(end):
                end = i.Vertex1
    
        for i in vertices:
            if i == start:
                start.children = i.children
            if i == end:
                end.children = i.children

        # Compute the weight of every edge or line
        for i in lines.values():
            if not ((i.Vertex1, i.Vertex2) in BoundariesLines or (i.Vertex2, i.Vertex1) in BoundariesLines):
                i.ComputeWeight()

        # Start the timer for A* algorithm
        t0 = time.time()

        paths = {}
        open = {}
        closed = set()

        G = 0
        Gn = 0
        line = None

        # First vertex in open list is start, with f(n) of 9999
        open[9999] = [G, start]

        # A* algorithm, which uses a prioritized f(n) open queue and a closed set.
        # The algorithm also uses a path dictionnary, which stores the paths and as keys, g(n) of each path and the last node of the path
        while not (len(open) == 0):
            keys = list(open.keys())
            keys.sort()
            G = open[keys[0]][0]
            CurrentVertex = open[keys[0]][1]
            open.pop(keys[0])

            # If time to find path exceeds 10 seconds or is the end node, break
            TimeToFindPath = time.time() - t0
            if TimeToFindPath > 10:
                print("Time is up. An optimal path could not be found!\n")
                break

            if CurrentVertex == end:
                break

            # Add the current node to closed set and loop through the children
            closed.add(CurrentVertex)
            for i in CurrentVertex.children:
                if not(i in closed):
                    weight = -1
                    if (CurrentVertex, i) in lines:
                        line = lines[(CurrentVertex, i)]
                        weight = line.Weight
                    elif (i, CurrentVertex) in lines:
                        line = lines[(i, CurrentVertex)]
                        weight = line.Weight
                    # If the edge or line is crossable, get h(n) and g(n) and put the child with key f(n) in open list
                    if weight > 0:
                        H = heuristsicFunction(i, end, weight)
                        Gn = G + weight
                        F = H + Gn
                        open[F] = [Gn, i]
                        # Append the children node to a path
                        if (CurrentVertex, G) in paths:
                            paths[(i, Gn)] = copy.copy(paths[CurrentVertex, G])
                            paths[(i, Gn)].append(line)
                        else:
                            paths[(i, Gn)] = [line]

        # Find the optimal path to end node by finding smallest g(n)
        for i in paths:
            if end == list(i)[0]:
                if list(i)[1] < G:
                    G = list(i)[1]

        t1 = time.time()
        total = t1 - t0
        print("Time to find path: {} seconds.".format(total))

        # Each line is composed of 2 vertices, use them to plot a line
        print("Optimal path: {}".format(round(G * 10) / 10))
        if (end, G) in paths:
            print("Found a path!\n")
            for i in paths[(end, G)]:
                x = numpy.linspace(i.Vertex1.x, i.Vertex2.x)
                y = numpy.linspace(i.Vertex1.y, i.Vertex2.y)
                pyplot.plot(x, y, color=[0, 1, 0])
        else:
            print("Due to blocks, no path was found. Please change the map and try again.\n")

        pyplot.plot([start.x], [start.y], marker='o', markersize=5, color=[0, 1, 0])
        pyplot.plot([end.x], [end.y], marker='o', markersize=5, color=[0, 0, 0])

        t2 = time.time()
        total = t2 - t1
        print("Time to render path: {} seconds.".format(total))
        pyplot.show()

        answer = input("Do you want to end the application ([Y] or [N])? ")
        if answer == 'Y':
            EndProgram = True

    print("Application Done!\n")

if __name__ == "__main__":
    runProgram()