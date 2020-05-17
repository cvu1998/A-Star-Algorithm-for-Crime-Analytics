import matplotlib
from matplotlib import pyplot
import numpy
import shapefile
import time

import Line
import Square
import Vertex

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

    t0 = time.time()
    print("Average: {}".format(numpy.average(H)))
    print("Standard Deviation: {}".format(numpy.std(H)))
    H[H < numpy.percentile(H, threshold)] = 0
    #print("H")
    #print(H)


    bounds = [0., 0.5, 1.]
    cmap = matplotlib.colors.ListedColormap([[1, 0, 1], [1, 1, 0]])
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    pyplot.figure()
    pyplot.imshow(H, cmap=cmap, norm=norm, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

    array = numpy.zeros(shape=(len(xedges) * len(yedges), 2))
    counter = 0
    for i in range(len(xedges)):
        for j in range(len(yedges)):
            array[counter] = [xedges[i], yedges[j]]
            counter = counter + 1

    quads = []
    lenX = len(xedges)
    lenY = len(yedges)
    for i in range(len(xedges) - 1):
        for j in range(len(yedges) - 1):
            v1 = Vertex.Vertex(array[j + (i * lenX)][0], array[j + (i * lenY)][1])
            v2 = Vertex.Vertex(array[j + (i * lenX) + lenX][0], array[j + (i * lenY) + lenY][1])
            v3 = Vertex.Vertex(array[j + (i * lenX) + 1][0], array[j + (i * lenY) + 1][1])
            v4 = Vertex.Vertex(array[j + (i * lenX) + lenX + 1][0], array[j + (i * lenY) + lenY + 1][1])
            if H[j][i] == 0:
                quad = Square.Square(v1, v2, v3, v4, False)
            else:
                quad = Square.Square(v1, v2, v3, v4, True)
            quads.append(quad)
            #print(j + (i * lenX), j + (i * lenY) + lenY, j + (i * lenX) + 1, j + (i * lenY) + lenY + 1)
            #print(H[j][i])

    lines = {}
    for i in quads:
        for j in i.getLines():
            if (j.Vertex1, j.Vertex2) in lines or (j.Vertex2, j.Vertex1) in lines:
                if (j.Vertex1, j.Vertex2) in lines:
                    lines[(j.Vertex1, j.Vertex2)].SecondSquare = j.FirstSquare
                elif (j.Vertex2, j.Vertex1) in lines:
                    lines[(j.Vertex2, j.Vertex1)].SecondSquare = j.FirstSquare
            else:
                lines[(j.Vertex1, j.Vertex2)] = j

    for i in lines.values():
        i.ComputeWeight()
        x = numpy.linspace(i.Vertex1.x, i.Vertex2.x)
        y = numpy.linspace(i.Vertex1.y, i.Vertex2.y)
        if i.Weight == 1:
            pyplot.plot(x, y, color=[0, 1, 0])
        elif i.Weight == 1.3 or i.Weight == 1.5:
            pyplot.plot(x, y, color=[0, 0, 1])
        else:
            pyplot.plot(x, y, color=[1, 0, 0])

    t1 = time.time()
    total = t1 - t0
    print("Time to find path: {} seconds.".format(total))
    pyplot.show()

    answer = input("Do you want to end the application ([Y] or [N])? ")
    if answer == 'Y':
        EndProgram = True

print("Application Done!\n")