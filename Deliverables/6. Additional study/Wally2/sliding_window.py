import cv2
import numpy as np

#Should we show the current inspected bounding box and for how long
VISUALISE = True
VISUALISE_PAUSE = 5

#How much does the sliding window shrink by each iteration
SLIDE_SHRINK_PERCENT = 0.75

#What is our original sliding window target pixels
TARGET_X_PIXELS = 60
TARGET_Y_PIXELS = 60

#Do we save the 'found' ROIs?
SAVE_FOUND_ROI = True
FOUND_ROI_SAVE_PATH = "D:/Programming/PythonTests/Wally2/ROI_Found/"

#Helper function to draw a rectangle on an image and COPY it
def draw_rect_img_copy(image, point1, point2, thickness=3, col=(0, 255, 0)):
    img = image.copy()
    rtn_img = cv2.rectangle(img, point1, point2, col, thickness)
    return rtn_img

#Helper function to draw a region of interest on a cloned image. 
#Just transforms arguments into those required for draw_rect_img_copy
def draw_region_of_interest(image, window_dimensions, coord_top_left):
    pt1 = (coord_top_left[0], coord_top_left[1])
    pt2 = (pt1[0] + window_dimensions[0], (pt1[1] + window_dimensions[1]))
    return draw_rect_img_copy(image, pt1, pt2)

#Iterates an ROI defined by window_dimensions over the image with a stride
#At each step, the sub image is passed to the process_roi_func
#If that function returns TRUE, the bounding box representing that sub image is added
#to the list of locations to be returned
def iterate_roi(image, window_dimensions, stride, process_roi_func):
    locations = []
    x_size = image.shape[0]
    y_size = image.shape[1]
    x_steps = int((x_size - window_dimensions[0]) / stride)
    y_steps = int((y_size - window_dimensions[1]) / stride)
    for y in range(0, y_steps+1):
        for x in range(0, x_steps+1):
            base_img = image.copy()
            sub_img = base_img[y*stride:y*stride+window_dimensions[1], x*stride:x*stride+window_dimensions[0]]
            sub_img = resize_sub_img(sub_img, TARGET_X_PIXELS, TARGET_Y_PIXELS)
            if VISUALISE:
                IMG_A = draw_region_of_interest(base_img, window_dimensions, (x*stride, y*stride))
                cv2.imshow('Test image', IMG_A)
                key = cv2.waitKey(VISUALISE_PAUSE) #pauses for 0.001 * x seconds before fetching next image
            found = process_roi(np.array(sub_img), process_roi_func=process_roi_func)
            if found:
                point1 = (x*stride, y*stride)
                point2 = (x*stride+window_dimensions[0], y*stride+window_dimensions[1])
                points = (point1, point2)
                locations.append(points)
                if SAVE_FOUND_ROI:
                    file_name = FOUND_ROI_SAVE_PATH + "ROI-" + str(x) + "-" + str(y) + ".bmp"
                    cv2.imwrite(file_name, sub_img)
                    print("Saved " + file_name)
    cv2.destroyAllWindows()
    return locations

#Sub function to process the ROI. This just passes off the image to the function provided
#RETURNS TRUE if the object is found
#Possibly can be removed.
def process_roi(sub_img, process_roi_func):
    if VISUALISE:
        cv2.imshow('Sub image', sub_img)

    # Found logic
    return process_roi_func(sub_img)

#Placeholder function to do analysis of sub images.
#In reality a function that will analyse the sub image will be passed instead of this one
#This is ONLY for testing 
#RETURNS TRUE IF WE WANT TO KEEP THIS IMAGE AS A POSITIVE LOCATION
def analyse_roi(sub_img):
    if VISUALISE:
        cv2.imshow('Sub image', sub_img)
    return False

#Helper function to resize images
def resize_sub_img(sub_img, target_x_pixels, target_y_pixels):
    resized_sub_img = cv2.resize(sub_img,(int(target_x_pixels),int(target_y_pixels)))
    return resized_sub_img

#--------- MAIN FUNCTION ----------
#Search all ROI, starting with the full image size, using progressively smaller windows 
#(shrinkage definde by SLIDE_SHRINK_PERCENT) until the window searched is the same size
#or smaller than the original window dimensions passed to this function
#---TODO:----
#* Update TARGET_X_PIXELS and TARGET_Y_PIXELS with the window dimensions passed to this function
#* Change the approach to maintain the aspect ratio of the window_dimensions passed instead of original image
#Currently it will scale the full original image and maintain that aspect ratio. A better way is to identify the
#largest size window of the correct window_dimensions aspect ratio that will fit in the image and use that to start
#iterating through the ROI
#* Currently the edge pixels outside a window multiple are ignored. Consider adding an additional ROI at the far edge
#of the image inset as required (and an additional row at the bottom offset)
def do_all_roi(image, window_dimensions, stride, process_roi_func):
    TARGET_X_PIXELS = window_dimensions[0]
    TARGET_Y_PIXELS = window_dimensions[1]
    locations = []
    stride_as_window_percent = stride/window_dimensions[0]
    #print("stride_as_window_percent="+str(stride_as_window_percent) )
    x_size = image.shape[0]
    y_size = image.shape[1]
    x_steps = int((x_size - window_dimensions[0]) / stride)
    y_steps = int((y_size - window_dimensions[1]) / stride)

    cur_x_size = x_size
    cur_y_size = y_size
    while cur_x_size >= window_dimensions[0]:
        cur_x_size = int(cur_x_size * SLIDE_SHRINK_PERCENT)
        cur_y_size = int(cur_y_size * SLIDE_SHRINK_PERCENT)
        print("Sliding window " + str(cur_x_size) + "x" + str(cur_y_size))
        #slide window over image at this size
        #append results to list
        #shrink window
        this_window_dimensions = (cur_x_size, cur_y_size)
        this_stride = int(this_window_dimensions[0] * stride_as_window_percent)
        new_locations = iterate_roi(image, this_window_dimensions, this_stride, process_roi_func)
        if len(new_locations) > 0:
            locations = locations + new_locations
            print(str(len(new_locations)) + " locations found at this level")
        else:
            print("No new locations found at this level")
        #print("cur_x_size="+str(cur_x_size) )
    print("Finished sliding all windows")
    return locations


if __name__ == "__main__": 
    #TESTING ONLY
    IMG = cv2.imread('1.bmp')
    do_all_roi(IMG, (60,60), 20, analyse_roi)
    print("DONE!")
