import glob
import cv2
import numpy as np

Y_AS_ARRAY = True
#V1_OUTPUT = np.array([0,1,0,0])
#V2_OUTPUT = np.array([0,0,1,0])
#E_OUTPUT = np.array([0,0,0,1])
#FAIL_OUTPUT = np.array([1,0,0,0])
V1_OUTPUT = np.array([1,0,0])
V2_OUTPUT = np.array([0,1,0])
E_OUTPUT = np.array([0,0,1])
FAIL_OUTPUT = np.array([0,0,0])

def GetImage(file):
    #ret,img = cv2.threshold(cv2.imread(file, cv2.IMREAD_GRAYSCALE),127,255,cv2.THRESH_BINARY)
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    return img

#TODO: Randomly split between train and test
def GetImages():
    images_x = []
    values_y = []
    images_x_val = []
    values_y_val = []
    test_images = []

    for file in glob.glob("SpellTraining/Fail/*.png"):
        img = GetImage(file)
        images_x.append(np.array(img))
        values_y.append(FAIL_OUTPUT)

    for file in glob.glob("SpellTraining/V1/*.png"):
        img = GetImage(file)
        images_x.append(np.array(img))
        if Y_AS_ARRAY:
            values_y.append(V1_OUTPUT)
        else:
            values_y.append(0)
        
    for file in glob.glob("SpellTraining/V2/*.png"):
        img = GetImage(file)
        images_x.append(np.array(img))
        if Y_AS_ARRAY:
            values_y.append(V2_OUTPUT)
        else:
            values_y.append(1)
        
    for file in glob.glob("SpellTraining/E/*.png"):
        img = GetImage(file)
        images_x.append(np.array(img))
        if Y_AS_ARRAY:
            values_y.append(E_OUTPUT)
        else:
            values_y.append(2)
        
    for file in glob.glob("SpellTraining/ValFail/*.png"):
        img = GetImage(file)
        images_x_val.append(np.array(img))
        values_y_val.append(FAIL_OUTPUT)

    for file in glob.glob("SpellTraining/ValV1/*.png"):
        img = GetImage(file)
        images_x_val.append(np.array(img))
        if Y_AS_ARRAY:
            values_y_val.append(V1_OUTPUT)
        else:
            values_y_val.append(0)
        
    for file in glob.glob("SpellTraining/ValV2/*.png"):
        img = GetImage(file)
        images_x_val.append(np.array(img))
        if Y_AS_ARRAY:
            values_y_val.append(V2_OUTPUT)
        else:
            values_y_val.append(1)
        
    for file in glob.glob("SpellTraining/ValE/*.png"):
        img = GetImage(file)
        images_x_val.append(np.array(img))
        if Y_AS_ARRAY:
            values_y_val.append(E_OUTPUT)
        else:
            values_y_val.append(2)

    for file in glob.glob("SpellTraining/Tests/*.png"):
        img = GetImage(file)
        test_images.append(np.array(img))
        
        
    return np.array(images_x), np.array(values_y), np.array(images_x_val), np.array(values_y_val), np.array(test_images)
