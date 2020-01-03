import random
import svgwrite
import os
from svgpathtools import parse_path
from random import randint
from xml.dom import minidom
from shapely.geometry import Polygon, Point

# writes a shape at the given x, y coordinate
def writeSVGPathAtPoint(x, y):
    sColor = random.choice(lColors);
    sDString = random.choice(lDStrings) # randomly select syntax character path
    iRotation = randint(0, 360);
    return '<path d="' + sDString + '" style="fill:' + sColor + '" transform="translate(' + str(x) + ',' + str(y) + ')"/>\n'

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
    
def get_random_point_in_polygon(poly):
     (minx, miny, maxx, maxy) = poly.bounds
     while True:
         p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
         if poly.contains(p):
             return p

p = Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 1), (0, 0)])
point_in_poly = get_random_point_in_polygon(mypoly)

lColors = ["#ffeeaa", "#ff8080", "#80ffe6"];
lDStrings = []
xmldoc = minidom.parse('paths/syntax/all.svg') # read in all syntax stings
itemlist = xmldoc.getElementsByTagName('path')
for s in itemlist:
    lDStrings.append(s.attributes['d'].value)

# x y nodes to use as pattern to print shapes on
with open('paths/shapes/tree.txt', 'r') as oFile:
    sPathData=oFile.read().replace('\n', '')
oFile.close()
        
lPaths = parse_path(sPathData)
print str(len(lPaths)) + " nodes found..."
# dwg = svgwrite.Drawing(filename="new_code_tree.svg", debug=True)

sBuildString = '<svg xmlns="http://www.w3.org/2000/svg">\n'
iCount = 0;
# do outline of shape
lXPoints = []
lYPoints = []
lPoints = []

for segment in lPaths:
    x_start = segment.start.real
    y_start = segment.start.imag
    x_end = segment.end.real
    y_end = segment.end.imag
    print "Writing syntax character at: (" + str(x_start) + ", " + str(y_start) + ") (" + str(iCount) + " of " + str(len(lPaths)) + ")..."    
    sBuildString = sBuildString + writeSVGPathAtPoint(x_start, y_start) 
    iCount = iCount + 1
    lXPoints.append(x_start)
    lYPoints.append(y_start)
    lPoints.append((x_start,y_start))
    

# fill in shape  (loop a rectangle from xmin, ymin to xmax, ymax) and if point intersects
x_max = int(max(lXPoints))
x_min = int(min(lXPoints))
y_max = int(max(lYPoints))
y_min = int(min(lYPoints))
iTotal = int((x_max-x_min)*(y_max-y_min))
iCount = 0
for x in range(x_min, x_max):
    for y in range(y_min, y_max):
        if point_inside_polygon(x, y, lPoints):
            print "Writing syntax character at: (" + str(x) + ", " + str(y) + ") (" + str(iCount) + " of " + str(iTotal) + ")..."        
            sBuildString = sBuildString + writeSVGPathAtPoint(x, y) 
        iCount = iCount + 1

sBuildString = sBuildString + "</svg>\n"
with open("new_code_tree_python_style_yo.svg", "w") as w:
    w.write(sBuildString);
    
w.close()

# beep
print "\a"
