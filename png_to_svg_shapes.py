import sys
import os
import random
from PIL import Image
from xml.dom import minidom
from random import randint
from svgpathtools import parse_path

SPREAD_FACTOR = 1; # for 1:1, or expand to 2 for 2:1 in x y space, 3:1 for 3, 4:1 etc
SKIP_FACTOR = 100; # skip every 'n' of these pixels (2 for every other, 3 for every third etc)
SCALE_FACTOR = 1; #size to shrink/grow the shapes by
SHAPE_TYPE = "syntax";  # ["syntax", "hatch", "alphabetsoup", "asterisk"]

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f
            
def writeSVGPathAtPoint(x, y, r, g, b):
    # sColor = random.choice(lColors);
    sDString = random.choice(lDStrings) # randomly select syntax character path
    iRotation = randint(0, 360); # random rotation
    oPath = parse_path(sDString);
    oPath = oPath.rotated(iRotation); # rotate path randomly
    # print oPath.d()
    sR = str(r);
    sG = str(g);
    sB = str(b);
    # print ','.join([sR, sG, sB])
    return '<path d="' + oPath.d() + '" style="fill:rgb(' + ','.join([sR, sG, sB]) + ')" transform="translate(' + str(x*SPREAD_FACTOR) + ',' + str(y*SPREAD_FACTOR) + ') scale(' + str(SCALE_FACTOR) + ')"/>\n'

def isPNGProperFormat(oImage):
    print("Scanning PNG for proper format...")
    oRGBAImage = oImage.convert('RGBA')
    iWidth = oImage.size[0]
    iHeight = oImage.size[1]
    for y in range(0, iHeight): # y
        for x in range(0, iWidth): # x
            iR, iG, iB, iA = oRGBAImage.getpixel((x,y))
            if not (iR == iG == iB == 255 or iR == iG == iB == 0):
                # ignore white pixels
                print("This .png must have only white and black pixels in it!")
                return False
    return True

def writeSVG(oImage, oRGBAImage):
    # begin writing of svg
    iWidth = oImage.size[0]
    iHeight = oImage.size[1]
    iTotal = iWidth*iHeight
    lStrings = []
    count = 0
    for y in range(0, iHeight): # y
        for x in range(0, iWidth): # x
            # skip every nth draw (faster completion and probably ultimately doesn't make a visible difference)
            if count % SKIP_FACTOR != 0:
                count = 0
                continue
            iR, iG, iB, iA = oRGBAImage.getpixel((x,y))
            if iR == iG == iB == 255:
                # ignore white pixels
                continue 
            # if iR == iG == iB == 0:
            #     # black pixel; write a random path
            lStrings.append(writeSVGPathAtPoint(x, y, iR, iG, iB))
            count = count + 1 
        print("Done with row " + str(y) + " of " + str(iHeight) + "...")
    # write SVG
    oFile.write('<svg xmlns="http://www.w3.org/2000/svg" width="'+ str(iPixelSize*iWidth*SCALE_FACTOR) +'" height="' + str(iPixelSize*iHeight*SCALE_FACTOR) + '">\n')
    oFile.write('\n'.join([str(x) for x in lStrings]))
    oFile.write('</svg>')
    oFile.close()
        
# lColors = ["#ffeeaa", "#ff8080", "#80ffe6"];
# lColors = ["#ebe25a"];
# lColors = ["white", "gray", "black"]
lDStrings = []
xmldoc = minidom.parse('paths/' + SHAPE_TYPE + '/all.svg') # read in all hatch strings
itemlist = xmldoc.getElementsByTagName('path')
for s in itemlist:
    lDStrings.append(s.attributes['d'].value)
sCWD = os.getcwd()
sFolderName = sCWD + "/" 
sPNGFileName = sys.argv[1]
lFileNames = listdir_nohidden(sFolderName)
iPixelSize = 1
oImage = Image.open(sFolderName + sPNGFileName)
sPNGFileNameNoExtension = os.path.splitext(oImage.filename)[0]
sFileExtension = os.path.splitext(oImage.filename)[1]
sFileToWrite = sPNGFileNameNoExtension + ".svg"
oFile = open(sFileToWrite,"w")    
oRGBAImage = oImage.convert('RGBA')
writeSVG(oImage, oRGBAImage);

print('\007')
print('\007')
print('\007')
print('\007')
print('\007')
print("Done! SVG was written to " + sFileToWrite + "!")