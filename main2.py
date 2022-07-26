from __future__ import print_function
import numbers
import cv2
import numpy as np
from screeninfo import get_monitors
import random
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont
import datetime
from scipy.stats import truncnorm
import time
import json

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


starting_time = None
screenWidth = None
screenHeight = None
numberBoxWidth = None
numberBoxHeight = None
numbersSelected = None
boundingBoxes = None
result = {}
currentSet = None

def writeFile():
    global starting_time
    global result
    global currentSet
    global numbersSelected
    global boundingBoxes
    # print("called 2")
    now = time.time()*1000
    #f = open(str(int(time.time())) + '.txt', 'w')
    resultStr = ''
    ending_time = time.time()*1000
    time_diff = int(ending_time - starting_time)
    #print(ending_time)
    init = True

    resultStr += "Set One (Single Digit + Double Digit)\n"
    resultStr += "Numbers: " + result[1]["numbers"] + "\n"
    resultStr += "Outlier Truth: " + result[1]["outlier_truth"] + "\n"
    resultStr += "Outlier Selected: " + result[1]["outlier_selected"] + "\n\n"


    resultStr += "Set Two (Double Digit)\n"
    resultStr += "Numbers: " + result[2]["numbers"] + "\n"
    resultStr += "Outlier Truth: " + result[2]["outlier_truth"] + "\n"
    resultStr += "Outlier Selected: " + result[2]["outlier_selected"] + "\n\n"

    resultStr += "Set Three (Triple Digit)\n"
    resultStr += "Numbers: " + result[3]["numbers"] + "\n"
    resultStr += "Outlier Truth: " + result[3]["outlier_truth"] + "\n"
    resultStr += "Outlier Selected: " + result[3]["outlier_selected"] + "\n\n"


    resultStr += "Time taken: " + str(time_diff) + "ms\n"

    f = open(str( int(ending_time)) + ".txt", "w")
    f.write(resultStr)
    f.close()

    #result_dict = {}

    # for x in testNumbers:
    #     if init == False:
    #         result += ','
        
    #     result = result + str(x)
    #     init = False

    # result_dict['result'] = result;
    # result_dict['time'] = str(time_diff);
    # result_dict['selected'] = str(num)

    # result = f'Numbers: {result_dict["result"]}\nSelected: {result_dict["selected"]}\nTime: {result_dict["time"]}\n' 

    # f.write(result)
    # f.close()

    

def handleClick(event,x,y,flags,param):
    global boundingBoxes
    global starting_time
    global result
    global currentSet
    global numbersSelected
    global boundingBoxes

    if event == cv2.EVENT_LBUTTONDBLCLK:
        # print("called", x, y)
        
        for key, value in zip(numbersSelected, boundingBoxes):
            x0 = value[0][1]
            y0 = value[0][0]

            x1 = value[1][1]
            y1 = value[1][0]

            if x >= x0 and y >= y0 and x <= x1 and y <= y1:
                numbersStr = ''
                for x in numbersSelected:
                    numbersStr += str(x) + " ";
                result[currentSet] = {
                    'numbers' : numbersStr,
                    'outlier_truth' : str(numbersSelected[-1]),
                    'outlier_selected' : str(key)
                }
                # return;
        #   cv2.destroyAllWindows()
        
        if currentSet == 1:
        #cv2.destroyAllWindows()
            showSetTwo()
        elif currentSet == 2:
        #cv2.destroyAllWindows()
            showSetThree()
        else:
            writeFile()
            cv2.destroyAllWindows()
        # exit()

def showSetTwo():
    global currentSet
    currentSet = 2
    generator = get_truncated_normal(mean=55, sd = 10, low=10, upp=99)
    numbers = []
    print("ashche")
    for i in range(0, 5):
        numbers.append(np.round(generator.rvs()));
    
    # generate outlier
    q1 = np.percentile(numbers, 25, interpolation='midpoint')
    q3 = np.percentile(numbers, 75, interpolation='midpoint')
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    hi  = q3 + 1.5*iqr

    decision = random.randint(1, 2)

    if decision == 1:
        outlier = random.randint(10, max(10,np.round(low)))
    else:
        outlier = random.randint(min(99,np.round(hi)), 99);

    numbers.append(outlier)
    for i in range(0, len(numbers)):
        numbers[i] = int(numbers[i])
    drawNumbers(numbers)

def showSetOne():
    global currentSet
    currentSet = 1
    generator = get_truncated_normal(mean=4, sd = 0.8, low=0, upp=9)
    numbers = []

    for i in range(0, 5):
        numbers.append(np.round(generator.rvs()));
    
    generator = get_truncated_normal(mean=55, sd = 10, low=10, upp=99)
    
    for i in range(0, 3):
        numbers.append(np.round(generator.rvs()));
    
    # generate outlier
    q1 = np.percentile(numbers, 25, interpolation='midpoint')
    q3 = np.percentile(numbers, 75, interpolation='midpoint')
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    hi  = q3 + 1.5*iqr

    decision = random.randint(1, 2)

    if decision == 1:
        outlier = random.randint(1, max(1, np.round(low)))
    else:
        outlier = random.randint(min(99,np.round(hi)), 99);

    numbers.append(outlier)
    for i in range(0, len(numbers)):
        numbers[i] = int(numbers[i])
    print(len(numbers))
    drawNumbers(numbers)

def showSetThree():
    global currentSet
    currentSet = 3
    generator = get_truncated_normal(mean=550, sd = 110, low=100, upp=999)
    numbers = []

    for i in range(0, 3):
        numbers.append(np.round(generator.rvs()));
    
    # generate outlier
    q1 = np.percentile(numbers, 25, interpolation='midpoint')
    q3 = np.percentile(numbers, 75, interpolation='midpoint')
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    hi  = q3 + 1.5*iqr

    decision = random.randint(1, 2)

    if decision == 1:
        outlier = random.randint(111, max(111,np.round(low)))
    else:
        outlier = random.randint(min(999,np.round(hi)), 999);

    numbers.append(outlier)
    for i in range(0, len(numbers)):
        numbers[i] = int(numbers[i])
    drawNumbers(numbers)


def init():
    global screenWidth
    global screenHeight
    global numberBoxWidth
    global numberBoxHeight
    global starting_time

    for m in get_monitors():
        if m.is_primary == True:
            screenHeight = m.height
            screenWidth = m.width
            
    print(screenHeight)
    print(screenWidth)
    
    numberBoxWidth = 180
    numberBoxHeight = 60
    starting_time = time.time()*1000
    print('starting time', starting_time)

def getNumbers():
    digitCount = random.randint(1, 3)
    if digitCount == 1:
        low = 0
        high = 9
    elif digitCount == 2:
        low = 10
        high = 99
    else:
        low = 100
        high = 999

    
    mu, sigma = 0.5, 1
    lower, upper = mu - 0.1*sigma, mu + 0.1*sigma

    sizeList = [3, 5, 7]
    size = sizeList[random.randint(1,3)-1]

    samples = truncnorm.rvs(
          (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=size)
    
    lower, upper = -10000000, mu  -2.698*sigma
    outlier1 = truncnorm.rvs(
          (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=1)

    lower, upper = mu  + 2.698*sigma, 10000000
    outlier2 = truncnorm.rvs(
          (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=1)
    
    outlier = None
    if random.randint(1, 2) == 1:
        outlier = outlier1
    else:
        outlier = outlier2

    outlier = outlier * (high-low) + low
    outlier = int(np.ceil(outlier).item())

    samples = (samples * (high-low)) + low
    
    print(type(samples))   
    
    
    samples = np.ceil(samples)
    samples = samples.astype(np.uint16)

    samples = list(samples)
    samples.append(outlier)
    return samples


def drawNumbers(testNumbers):
    global screenWidth
    global screenHeight
    global numberBoxWidth
    global numberBoxHeight
    global boundingBoxes
    # global testNumbers
    global numbersSelected
    
    img = np.zeros((screenHeight, screenWidth, 3), dtype=np.uint8)
    img = 255 - img

    horizontalBoxCount = (screenWidth * 0.5) // numberBoxWidth
    verticalBoxCount = (screenHeight * 0.5) // numberBoxHeight

    totalBoxCount = int(horizontalBoxCount * verticalBoxCount)
    print(totalBoxCount)
    print(len(testNumbers))
    validIndices = []
    numbersSelected = []
    boundingBoxes = []
    for i in range(totalBoxCount):
        validIndices.append(i)
    

    
    for i in testNumbers:
        # print(i) 
        idx = validIndices[random.randint(0, len(validIndices)-1)]
        validIndices.remove(idx)
        gridRow = idx / horizontalBoxCount
        gridColumn = idx % horizontalBoxCount


        upperLeftCorner = (0.25 * screenHeight + gridRow * numberBoxHeight , 0.25 * screenWidth + gridColumn * numberBoxWidth )
        lowerRightCorner = (upperLeftCorner[0] + numberBoxHeight - 20, upperLeftCorner[1] + numberBoxWidth - 20)

        boundingBoxes.append((upperLeftCorner, lowerRightCorner))
        numbersSelected.append(i)

        assert(upperLeftCorner[0] >= 0 and upperLeftCorner[0] < screenHeight and upperLeftCorner[1] >= 0 and upperLeftCorner[1] < screenWidth)
    font = ImageFont.truetype("arial.ttf", 28)
    pilImage = Image.new('RGB', (screenWidth, screenHeight  ), 'black')
    pilImage.setim(img)

    draw = ImageDraw.Draw(pilImage)
    print(boundingBoxes)
    
    for key,value in zip(numbersSelected, boundingBoxes):
        text = str(key)
        draw.text((value[0][1], value[0][0]), text, font=font, fill=(1,1,1))
    
    mask = pilImage.getim()
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', handleClick)
    cv2.imshow('image', mask)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

def main():
    showSetOne()

if __name__ == '__main__':
    init()
    main()