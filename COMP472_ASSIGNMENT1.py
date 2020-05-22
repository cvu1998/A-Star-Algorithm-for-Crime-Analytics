import copy

import matplotlib
from matplotlib import pyplot
import numpy
import shapefile
import time

import Line
import Square
import Vertex

def heuristsicFunction(currentVertex, end, weight):
    distance = (currentVertex.x - end.x ) * (currentVertex.x - end.x) + (currentVertex.y - end.y ) * (currentVertex.y - end.y)
    return distance

EndProgram = False
while not EndProgram:
    sf = shapefile.Reader("crime_dt.shp", encoding='ISO-8859-1')

    isValid = False
    step = 0.002
    while not isValid:
        try:
            step = float(input("Enter the size of a grid: "))
        except:
                print("Input [{}] is invalid!\n".format(step))
                isValid = False
        else:
            if step <= 0 or step > 0.01:
                print("Input [{}] is invalid!\n".format(step))
                isValid = False
            else:
                isValid = True

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
    #print("H")
    #print(H)

    print("Average: {}".format(numpy.average(H)))
    print("Standard Deviation: {}".format(numpy.std(H)))
    H[H < numpy.percentile(H, threshold)] = 0
    #print("H")
    #print(H)

    bounds = [0., 0.5, 1.]
    cmap = matplotlib.colors.ListedColormap([[0.5, 0, 0.5], [1, 1, 0]])
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    pyplot.figure()
    pyplot.imshow(H, cmap=cmap, norm=norm, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

    lenX = len(xedges)
    lenY = len(yedges)
    vertices = []
    for i in range(lenX):
        for j in range(lenY):
            vertices.append(Vertex.Vertex(xedges[i], yedges[j]))

    quads = []
    for i in range(lenX - 1):
        for j in range(lenY - 1):
            HighCrime = True
            if H[j][i] == 0:
                HighCrime = False
            quad = Square.Square(vertices[j + (i * lenX)], vertices[j + (i * lenX) + 1], 
                                 vertices[j + (i * lenX) + lenX], vertices[j + (i * lenX) + lenX + 1], HighCrime)
            quads.append(quad)
            #print(j + (i * lenX), j + (i * lenY) + lenY, j + (i * lenX) + 1, j + (i * lenY) + lenY + 1)
            #print(H[j][i])

    BBXEdge0X = min(xedges)
    BBXEdge0Y = min(yedges)

    BBXEdge1X = max(xedges)
    BBXEdge1Y = min(yedges)

    BBXEdge2X = max(xedges)
    BBXEdge2Y = max(yedges)

    BBXEdge3X = min(xedges)
    BBXEdge3Y = max(yedges)

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

    lines = {}
    for i in quads:
        for j in i.getLines():
            if (j.Vertex1, j.Vertex2) in lines:
                lines[(j.Vertex1, j.Vertex2)].SecondSquare = j.FirstSquare
            elif (j.Vertex2, j.Vertex1) in lines:
                lines[(j.Vertex2, j.Vertex1)].SecondSquare = j.FirstSquare
            else:
                lines[(j.Vertex1, j.Vertex2)] = j

    areChildren = False
    children = set()
    for i in vertices:
        for j in lines:
            for k in j:
                if i == k:
                    areChildren = True
                else:
                    children.add(k)
            if areChildren:
                i.children = i.children.union(children)
            areChildren = False
            children.clear()

    isValid = False
    x1 = vertices[0].x
    y1 = vertices[0].y
    #x2 = vertices[22].x
    #y2 = vertices[22].y    
    #x2 = vertices[32].x
    #y2 = vertices[32].y
    #x2 = vertices[154].x
    #y2 = vertices[176].y
    #x2 = vertices[440].x
    #y2 = vertices[176].y
    x2 = -73.5571
    y2 = 45.517
    #x2 = -73.5614
    #y2 = 45.5185
    #Path cannot be found
    #x2 = -73.5597
    #y2 = 45.5167
    ##########
    #x2 = -73.5536
    #y2 = 45.5206
    #x2 = -73.57373
    #y2 = 45.49569
    #while not isValid:
    #    try:
    #        x1 = float(input("Enter the X starting coordinate: "))
    #        y1 = float(input("Enter the Y starting coordinate: "))
    #        x2 = float(input("Enter the X ending coordinate: "))
    #        y2 = float(input("Enter the Y ending coordinate: "))
    #    except:
    #            print("Inputs are invalid!\n")
    #            isValid = False
    #    else:
    #        if (x1 < BBXEdge0X or x2 < BBXEdge0X or y1 < BBXEdge0Y or y2 < BBXEdge0Y or
    #            x1 > BBXEdge2X or x2 > BBXEdge2X or y1 > BBXEdge2Y or y2 > BBXEdge2Y):
    #            print("Inputs must be between ({0}, {1}), ({2}, {3}), ({4}, {5}), ({6}, {7})!\n"
    #                  .format(BBXEdge0X, BBXEdge0Y, BBXEdge1X, BBXEdge1Y, BBXEdge2X, BBXEdge2Y, BBXEdge3X, BBXEdge3Y))
    #            isValid = False
    #        else:
    #            isValid = True

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

    #f = open("log.txt", "a")
    #f.truncate(0)

    #f.write("Start: " + str(start) + "\n")
    #f.write("end: " + str(end) + "\n")

    for i in lines.values():
        if not ((i.Vertex1, i.Vertex2) in BoundariesLines or (i.Vertex2, i.Vertex1) in BoundariesLines):
            i.ComputeWeight()

    t0 = time.time()

    paths = {}
    open = {}
    closed = set()

    G = 0
    Gn = 0
    line = None

    open[9999] = [G, start]

    while not (len(open) == 0):
        keys = list(open.keys())
        keys.sort()
        G = open[keys[0]][0]
        CurrentVertex = open[keys[0]][1]
        open.pop(keys[0])

        #f.write(str(CurrentVertex) + "\n")
        if CurrentVertex == end:
            break

        closed.add(CurrentVertex)
        for i in CurrentVertex.children:
            if not(i in closed):
                #f.write("Child: " + str(i) + "\n")
                weight = -1
                if (CurrentVertex, i) in lines:
                    line = lines[(CurrentVertex, i)]
                    weight = line.Weight
                elif (i, CurrentVertex) in lines:
                    line = lines[(i, CurrentVertex)]
                    weight = line.Weight
                if weight > 0:
                    H = heuristsicFunction(i, end, weight)
                    Gn = G + weight
                    F = H + Gn
                    open[F] = [Gn, i]
                    if (CurrentVertex, G) in paths:
                        paths[(i, Gn)] = copy.copy(paths[CurrentVertex, G])
                        paths[(i, Gn)].append(line)
                    else:
                        paths[(i, Gn)] = [line]
                    #f.write("H: " + str(H) + "\n")
                    #f.write("F: " + str(F) + "\n")

    #f.close()
    for i in paths:
        if end == list(i)[0]:
            print(list(i)[1])
            if list(i)[1] < G:
                G = list(i)[1]

    t1 = time.time()
    total = t1 - t0
    print("Time to find path: {} seconds.".format(total))

    for i in lines.values():
        x = numpy.linspace(i.Vertex1.x, i.Vertex2.x)
        y = numpy.linspace(i.Vertex1.y, i.Vertex2.y)
        if i.Weight == -1:
            pyplot.plot(x, y, color=[1, 0, 0])

    print("Optimal path: {}".format(G))
    if (end, G) in paths:
        print("Found a path!\n")
        for i in paths[(end, G)]:
            x = numpy.linspace(i.Vertex1.x, i.Vertex2.x)
            y = numpy.linspace(i.Vertex1.y, i.Vertex2.y)
            pyplot.plot(x, y, color=[0, 1, 0])
    else:
        print("Could not find a path!\n")

    pyplot.plot([end.x], [end.y], marker='o', markersize=3, color=[0, 1, 1])

    t2 = time.time()
    total = t2 - t1
    print("Time to render path: {} seconds.".format(total))
    pyplot.show()

    answer = input("Do you want to end the application ([Y] or [N])? ")
    if answer == 'Y':
        EndProgram = True

print("Application Done!\n")