from __future__ import print_function
import cv2
import numpy as np
from screeninfo import get_monitors
import random
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont
import datetime
from scipy.stats import truncnorm
import pandas as pd
import statistics
import os
import pprint 

screenWidth = None
screenHeight = None
numberBoxWidth = None
numberBoxHeight = None
boundingBoxes = None
testNumbers = None

dataset = None

"""
    Dataset format: 
        {
            "highoutLow": [
                nums: []
                interquartile range
            ]
        }
"""
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
    # print(boundingBoxes)
    
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

def format_data(single_column):
    # print(single_column)
    set_nums = single_column.iloc[2:36].iloc[0:8].to_list()
    
    set_nums = [int(x) for x in set_nums]
    high_outlier = int(single_column.iloc[2:36].iloc[-1])
    low_outlier = int(single_column.iloc[2:36].iloc[-6])

    iqr = float(single_column.iloc[2:36].iloc[-14])
    
    mean_wo_outlier = statistics.mean(set_nums)
    std_wo_outlier = statistics.stdev(set_nums)

    mean_w_outlier = statistics.mean(set_nums + [high_outlier, low_outlier])
    std_w_outlier = statistics.stdev(set_nums + [high_outlier, low_outlier])


    data_dict = {
        "set_nums" : set_nums,
        "mean_wo_outlier" : mean_wo_outlier,
        "mean_w_outlier" : mean_w_outlier,
        "std_wo_outlier" : std_wo_outlier,
        "std_w_outlier": std_w_outlier,
        "iqr" : iqr,
        "high_outlier" : high_outlier,
        "low_outlier" : low_outlier
    }

    return data_dict

def load_dataset():
    global dataset
    dataset = {}

    filenames = os.listdir('dataset/')
    
    for data_file in filenames:
        df = pd.read_csv(f'dataset/{data_file}')
        dataset[data_file] = []
        print(data_file)    
        for column in range(1, 100, 4):
            print(column)
            try:
                single_set = df.iloc[:, column]
            except:
                break
            try:
                dataset[data_file].append(format_data(single_set))
            except:
                break

if __name__ == '__main__':
    #init()
    #main()

    load_dataset()
    # pprint.pprint(dataset)