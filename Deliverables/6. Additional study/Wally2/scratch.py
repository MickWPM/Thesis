import sliding_window as slide
import cv2
import numpy as np
import wally_nn

#Searches for wally using a dynamic sliding window. 
#Window starts at full image size (resized to target wally size) and gets iteratively smaller
#until reaching the original window size (or smaller) as defined in sliding_window


slide.VISUALISE = False
IMG = cv2.imread('2.bmp')
#IMG = cv2.imread('6.bmp')

locs = np.array(slide.do_all_roi(IMG, (60,60), 15, wally_nn.analyse_sub_img))

num_found = locs.shape[0]

print("Num locs found = " + str(num_found))

if num_found > 0:
    for loc in locs:
        point1 = (loc[0][0], loc[0][1])
        point2 = (loc[1][0], loc[1][1])
        sub_img = slide.draw_rect_img_copy(IMG, point1, point2)
        
        resized_sub_img = cv2.resize(sub_img,(int(256),int(256)))
        cv2.imshow('Sub image', sub_img)
        cv2.waitKey(0)
else:
    print("Wally not found")