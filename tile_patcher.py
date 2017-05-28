#!/usr/bin/python

# Spacing 4 and margin 4

import sys
from PIL import Image as PIL_Image
from math import ceil

if len(sys.argv) < 3:
    print "Usage : python tile_patcher.py [image file] [tile size]"
    exit(0)

filename = sys.argv[1]
tileSize = int(sys.argv[2])
newTileSize = tileSize + 2
TopPadding = 3
LeftPadding = 3
Spacing = 2

original = PIL_Image.open(filename)
originalWidth = original.size[0]
originalHeight = original.size[1]

xPos = TopPadding
yPos = LeftPadding

newImageWidth = int((ceil(originalWidth / tileSize) + 1) * (newTileSize + Spacing)) + LeftPadding
newImageHeight = int((ceil(originalHeight / tileSize)  + 1) * (newTileSize + Spacing)) + TopPadding
resultImage = PIL_Image.new("RGBA", (newImageWidth, newImageHeight)) 

def isEmpty(image):
    rgb = image.convert('RGBA')
    empty = True
    for ix in range(0, tileSize):
        for iy in range(0, tileSize):
            r, g, b, a = rgb.getpixel((ix, iy))
            if a != 0:
                empty = False
            if not empty:
                break
        if not empty:
            break

    return empty

for x in range(0, originalWidth, tileSize):
    for y in range(0, originalHeight, tileSize):

        image = original.crop((x, y, x + tileSize, y + tileSize))

        #if isEmpty(image):
        #    continue

        # top left 
        top_left_point = image.crop((0, 0, 1, 1))
        # top right
        top_right_point = image.crop((tileSize - 1, 0, tileSize, 1))
        # bottom right
        bottom_right_point = image.crop((tileSize - 1, tileSize - 1, tileSize, tileSize))
        # bottom left
        bottom_left_point = image.crop((0, tileSize - 1, 1, tileSize))
        
        # top
        top_edge = image.crop((0, 0, tileSize, 1))
        # bottom
        bottom_edge = image.crop((0, tileSize - 1, tileSize, tileSize))
        # left
        left_edge = image.crop((0, 0, 1, tileSize))
        # right
        right_edge = image.crop((tileSize - 1, 0, tileSize, tileSize))

        resultImage.paste(top_edge, (xPos + 1, yPos))
        resultImage.paste(left_edge, (xPos, yPos + 1))
        resultImage.paste(right_edge, (xPos + newTileSize - 1, yPos + 1))
        resultImage.paste(bottom_edge, (xPos + 1, yPos + newTileSize - 1))

        resultImage.paste(top_left_point, (xPos, yPos))
        resultImage.paste(top_right_point, (xPos + newTileSize - 1, yPos))
        resultImage.paste(bottom_right_point, (xPos + newTileSize - 1, yPos + newTileSize- 1))
        resultImage.paste(bottom_left_point, (xPos, yPos + newTileSize  - 1))

        resultImage.paste(image, (xPos + 1, yPos + 1))

        yPos += newTileSize + Spacing
        
    yPos = TopPadding
    xPos += newTileSize + Spacing


resultImage.save(filename[:-4] + "_patched" + filename[-4:])
