import cv2
from screeninfo import get_monitors
import random
from __future__ import print_function
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont

def init():
    global screenWidth
    global screenHeight
    global numberBoxWidth
    global numberBoxHeight

    for m in get_monitors():
        if m.is_primary == True:
            screenHeight = m.height
            screenwidth = m.width

def getNumbers():
    return [1, 333, 2, 99, 100, 4]


def drawNumbers():
    img = np.zeros(screenWidth, screenHeight)
    img = 1 - img

    horizontalBoxCount = screenWidth / numberBoxWidth
    verticalBoxCount = screenHeight / numberBoxHeight

    totalBoxCount = horizontalBoxCount * verticalBoxCount

    validIndices = []

    for i in ranges(totalBoxCount):
        validIndices.append(i)
    
    testNumbers = getNumbers()

    boundingBoxes = {

    }

    for i in testNumbers: 
        idx = validIndices[random.randint(0, len(validIndices))]
        
        gridRow = idx / horizontalBoxCount
        gridColumn = idx % horizontalBoxCount


        upperLeftCorner = (gridRow * numberBoxHeight + 20, gridColumn * numberBoxWidth + 20)
        lowerRightCorner = (upperLeftCorner[0] + numberBoxHeight - 20, upperLeftCorner[1] + numberBoxWidth - 20)

        boundingBoxes[i] = (upperLeftCorner, lowerRightCorner)
    
    font = ImageFont.truetype("arial.ttf", 24)
    pilImage = Image.fromarray(np.uint8(numpy_image))

    for key,value in boundingBoxes:
        text = str(key)
        draw.text((value[0][1], value[0][0]), text, font=font, fill=(0, 0, 0))
    


