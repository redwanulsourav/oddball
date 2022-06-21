from __future__ import print_function
import cv2
import numpy as np
from screeninfo import get_monitors
import random
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont
import datetime

screenWidth = None
screenHeight = None
numberBoxWidth = None
numberBoxHeight = None
boundingBoxes = None
testNumbers = None

def writeFile(num):
    print("called 2")
    now = datetime.datetime.now()
    f = open(str(now) + '.txt', 'w')
    result = ''
    init = True
    for x in testNumbers:
        if init == False:
            result += ','
        
        result = result + str(x)
        init = False
    
    result = result + '\n' + str(num)
    f.write(result)
    f.close()

def handleClick(event,x,y,flags,param):
    global boundingBoxes
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # print("called", x, y)
        
        for key, value in boundingBoxes.items():
            x0 = value[0][1]
            y0 = value[0][0]

            x1 = value[1][1]
            y1 = value[1][0]

            if x >= x0 and y >= y0 and x <= x1 and y <= y1:
                writeFile(key)
                # return;
        cv2.destroyAllWindows()
        exit()


def init():
    global screenWidth
    global screenHeight
    global numberBoxWidth
    global numberBoxHeight

    for m in get_monitors():
        if m.is_primary == True:
            screenHeight = m.height -200
            screenWidth = m.width - 200
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
    global boundingBoxes
    global testNumbers

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
        idx = validIndices[random.randint(0, len(validIndices)-1)]
        
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
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', handleClick)
    cv2.imshow('image', mask)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

def main():
    drawNumbers()

if __name__ == '__main__':
    init()
    main()