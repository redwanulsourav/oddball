from __future__ import print_function
import cv2
import numpy as np
from screeninfo import get_monitors
import random
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont

screenWidth = None
screenHeight = None
numberBoxWidth = None
numberBoxHeight = None

def init():
    global screenWidth
    global screenHeight
    global numberBoxWidth
    global numberBoxHeight

    for m in get_monitors():
        if m.is_primary == True:
            screenHeight = m.height -100
            screenWidth = m.width - 100
            print("dhukse")
    print(screenHeight)
    print(screenWidth)
    numberBoxWidth = 180
    numberBoxHeight = 60

def getNumbers():
    return [1, 333, 2, 99, 100, 4]


def drawNumbers():
    global screenWidth
    global screenHeight
    global numberBoxWidth
    global numberBoxHeight

    img = np.zeros((screenHeight, screenWidth, 3), dtype=np.uint8)
    img = 255 - img

    horizontalBoxCount = screenWidth // numberBoxWidth
    verticalBoxCount = screenHeight // numberBoxHeight

    totalBoxCount = horizontalBoxCount * verticalBoxCount

    validIndices = []

    for i in range(totalBoxCount):
        validIndices.append(i)
    
    testNumbers = getNumbers()

    boundingBoxes = {

    }

    for i in testNumbers: 
        idx = validIndices[random.randint(0, len(validIndices))]
        
        gridRow = idx / horizontalBoxCount
        gridColumn = idx % horizontalBoxCount


        upperLeftCorner = (gridRow * numberBoxHeight , gridColumn * numberBoxWidth )
        lowerRightCorner = (upperLeftCorner[0] + numberBoxHeight - 20, upperLeftCorner[1] + numberBoxWidth - 20)

        boundingBoxes[i] = (upperLeftCorner, lowerRightCorner)
        assert(upperLeftCorner[0] >= 0 and upperLeftCorner[0] < screenHeight and upperLeftCorner[1] >= 0 and upperLeftCorner[1] < screenWidth)
    font = ImageFont.truetype("arial.ttf", 28)
    pilImage = Image.new('RGB', (screenWidth, screenHeight  ), 'black')
    pilImage.setim(img)

    draw = ImageDraw.Draw(pilImage)
    print(boundingBoxes)
    
    for key,value in boundingBoxes.items():
        text = str(key)
        draw.text((value[0][1], value[0][0]), text, font=font, fill=(1,1,1))
    
    mask = pilImage.getim()
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    drawNumbers()

if __name__ == '__main__':
    init()
    main()