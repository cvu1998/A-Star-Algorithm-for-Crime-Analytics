import matplotlib
from matplotlib import pyplot
import numpy
import shapefile

import Line
import Square
import Vertex

sf = shapefile.Reader("crime_dt.shp", encoding='ISO-8859-1')
#print(sf.bbox)

step = 0.002
XAxis = numpy.arange(sf.bbox[0], sf.bbox[2] + 0.002, step)
YAxis = numpy.arange(sf.bbox[1], sf.bbox[3] + 0.002, step)
#print(XAxis)
#print(YAxis)

#XValues = []
#YValues = []

shapeRecords = sf.shapeRecords()
XValues = numpy.zeros(shape=(len(shapeRecords)),)
YValues = numpy.zeros(shape=(len(shapeRecords)),)

for i in range(len(shapeRecords)):
    x = shapeRecords[i].shape.__geo_interface__["coordinates"][0]
    y = shapeRecords[i].shape.__geo_interface__["coordinates"][1]
    XValues[i] = x
    YValues[i] = y
    #XValues.append(x)
    #YValues.append(y)

#print("XValues:\n")
#print(XValues)
#print("YValues:\n")
#print(YValues)

H, xedges, yedges = numpy.histogram2d(XValues, YValues, bins=(XAxis, YAxis))
H = H.T
#print("H")
#print(H)

#max = numpy.amax(H)
#print("Max")
#print(max)
#normalized = H / max
#print("Normalized")
#print(normalized)
#normalized[normalized < 0.75] = 0
#print("Output")
#print(normalized)

print("Average: {}".format(numpy.average(H)))
print("Standard Deviation: {}".format(numpy.std(H)))
H[H < numpy.percentile(H, 0)] = 0
#print("H")
#print(H)


bounds = [0., 0.5, 1.]
cmap = matplotlib.colors.ListedColormap([[1, 0, 1], [1, 1, 0]])
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
pyplot.figure()
pyplot.imshow(H, cmap=cmap, norm=norm, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

#array = numpy.array([[[x,y] for x in xedges] for y in yedges])
##print(array)
##print(H[8][16])
##print(array[0][0])
##print(array[8][16])
##print(array[8][17])
##print(array[9][16])
##print(array[9][17])
#
#quads = []

#for i in range(20):
#    for j in range(20):
#        v1 = Vertex.Vertex(array[i][j][0], array[i][j][1])
#        v2 = Vertex.Vertex(array[i + 1][j][0], array[i + 1][j][1])
#        v3 = Vertex.Vertex(array[i][j + 1][0], array[i][j + 1][1])
#        v4 = Vertex.Vertex(array[i + 1][j + 1][0], array[i + 1][j + 1][1])
#        #v1 = Vertex.Vertex(array[j + (i * 20)][1], array[j + (i * 20)][0])
#        #v2 = Vertex.Vertex(array[j + (i * 20) + 20][1], array[j + (i * 20) + 20][0])
#        #v3 = Vertex.Vertex(array[j + (i * 20) + 1][1], array[j + (i * 20) + 1][0])
#        #v4 = Vertex.Vertex(array[j + (i * 20) + 21][1], array[j + (i * 20) + 21][0])
#        if H[i][j] == 0:
#            quad = Square.Square(v1, v2, v3, v4, False)
#        else:
#            quad = Square.Square(v1, v2, v3, v4, True)
#        quads.append(quad)
#        print(i, j)
#        print(H[i][j])

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
        #v1 = Vertex.Vertex(array[j + (i * 20)][1], array[j + (i * 20)][0])
        #v2 = Vertex.Vertex(array[j + (i * 20) + 20][1], array[j + (i * 20) + 20][0])
        #v3 = Vertex.Vertex(array[j + (i * 20) + 1][1], array[j + (i * 20) + 1][0])
        #v4 = Vertex.Vertex(array[j + (i * 20) + 21][1], array[j + (i * 20) + 21][0])
        if H[j][i] == 0:
            quad = Square.Square(v1, v2, v3, v4, False)
        else:
            quad = Square.Square(v1, v2, v3, v4, True)
        quads.append(quad)
        print(j + (i * lenX), j + (i * lenY) + lenY, j + (i * lenX) + 1, j + (i * lenY) + lenY + 1)
        print(H[j][i])
        #x = numpy.linspace(array[j + (i * 20)][0], array[j + (i * 20) + 20][0])
        #y = numpy.linspace(array[j + (i * 20)][1], array[j + (i * 20) + 20][1])
        #pyplot.plot(x, y, color=[1, 0, 0])

#lines = {}
#for x in quads:
#    for y in x.getLines():
#        if (y.Vertex1, y.Vertex2) in lines or (y.Vertex2, y.Vertex1) in lines:
#            if (y.Vertex1, y.Vertex2) in lines:
#                lines[(y.Vertex1, y.Vertex2)].SecondSquare = y.FirstSquare
#            elif (y.Vertex2, y.Vertex1) in lines:
#                lines[(y.Vertex2, y.Vertex1)].SecondSquare = y.FirstSquare
#        else:
#            lines[(y.Vertex1, y.Vertex2)] = y

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
        #print("Diagonal: {}".format(i.Diagonal))
        #print(i.Weight)
        pyplot.plot(x, y, color=[0, 0, 1])
    else:
        #print("Diagonal: {}".format(i.Diagonal))
        #print(i.Weight)
        pyplot.plot(x, y, color=[1, 0, 0])

#for i in range(len(xedges) - 1):
#    x = numpy.linspace(xedges[i], xedges[i + 1])
#    for j in range(len(yedges) - 1):
#        y = numpy.linspace(yedges[j], yedges[j])
#        pyplot.plot(x, y, color=[1, 0, 0])
#        
#for i in range(len(xedges) - 1):
#    x = numpy.linspace(xedges[i], xedges[i])
#    for j in range(len(yedges) - 1):
#        y = numpy.linspace(yedges[j], yedges[j + 1])
#        pyplot.plot(x, y, color=[1, 0, 0])

#x = numpy.linspace(-73.57,-73.57)
#y = numpy.linspace(45.510,45.525)
#pyplot.plot(x, y, color=[1, 0, 0])
#
#x = numpy.linspace(-73.58,-73.57)
#y = numpy.linspace(45.525,45.525)
#pyplot.plot(x, y, color=[1, 0, 0])

#pyplot.imshow(normalized, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
pyplot.show()
print("Done\n")