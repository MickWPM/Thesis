"""
Getter file for test data. This file can be changed for testing of different features and streams
Implements required methods for nav_localisation data getter:
    feature_available, feature = get_next_feature()
    frame = get_next_frame()
    ipm = get_inverse_perspective_matrix()    #Matrix for frame inverse perspective mapping
    ipm_mask = get_ipm_mask()                 #Mask for inverse perspective mapped image (for road surface detection masking)
"""

import glob     #Reading directory of test images
import cv2
import numpy as np

HISTOGRAM_WINDOW = ((120,140), (380,174))

TEST_FEATURES = []
FEATURE_POINT=(290,30)
BOTTOM_POINT=(285,110)
LEFT_POINT=(440,30) #RIGHT
RIGHT_POINT=(292,9) #TOP
feature_1 = (FEATURE_POINT, BOTTOM_POINT, LEFT_POINT, RIGHT_POINT)

def get_next_feature():
    """
    Get the next road feature (if available)
    returns feature (None if no feature found)
    """
    if not TEST_FEATURES:
        return False, None
    feature = TEST_FEATURES.pop(0)
    return feature

def get_next_frame():
    """Return the next frame for processing or
    None if it doesnt exist"""
    if TEST_IMAGES:
        return TEST_IMAGES.pop(0)
    return None

def get_next_IPMframe():
    """Return the next frame for processing or
    None if it doesnt exist"""
    if TEST_IMAGES_IPM:
        return TEST_IMAGES_IPM.pop(0)
    return None

def get_next_rsd(new_frame):
    road_surface = TEST_RSD_IMAGES.pop(0)
    #To visualise detected road
    # threshold and binary AND
    _, thresh = cv2.threshold(road_surface, 150, 255, 0)
    thresh = cv2.merge((thresh, thresh, thresh))
    #thresh = OpenClose(thresh,iterations=1,kernel=np.ones((3,3),np.uint8))
    if False:
        new_frame = cv2.cvtColor(new_frame, cv2.COLOR_HSV2BGR)
    road_surface_visualised = cv2.bitwise_and(new_frame, thresh)
    
    return road_surface, road_surface_visualised

IPM_PATH = ("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/near_demo_CameraInverseMatrix.npy")
            
def get_inverse_perspective_matrix():
    """Return the saved inverse perspective matrix"""
    ipm = np.load(IPM_PATH)
    return ipm

def get_ipm_mask():
    birds_eye = cv2.warpPerspective(TEST_IMAGES[0], get_inverse_perspective_matrix(), (TEST_IMAGES[0].shape[1],TEST_IMAGES[0].shape[0]))
    _, thresh = cv2.threshold(birds_eye, 1, 255, cv2.THRESH_BINARY)
    return thresh[:, :, 0]

def init_features():
    """Initialise features by loading them into TEST_FEATURES list"""
    TEST_FEATURES.append(feature_1)

TEST_IMAGE_PATH = ("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/dashcam")
                   
TEST_IMAGES = []
TEST_RSD_IMAGES = []
TEST_IMAGES_IPM = []
def init_frames():
    """Initialise the frames by loading them into TEST_IMAGES list"""
    files = glob.glob(TEST_IMAGE_PATH + '/*.png')
    if files:
        for file in files:
            TEST_IMAGES.append(cv2.imread(file))
    else:
        print("No files")
    files = glob.glob("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/dashrsd/*.png")
    if files:
        for file in files:
            TEST_RSD_IMAGES.append(cv2.imread(file, cv2.IMREAD_GRAYSCALE))
    else:
        print("No TEST_RSD_IMAGES files")
        
    files = glob.glob("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/dashipm/*.png")
    if files:
        for file in files:
            TEST_IMAGES_IPM.append(cv2.imread(file))
    else:
        print("No TEST_IMAGES_IPM files")

def init():
    """Setup initial vaules for features and frames"""
    print("Initialising")
    init_features()
    init_frames()
    print("Initialising completed")


def test():
    """Call all test functions"""
    #test_get_next_feature()
    test_get_next_frame()

def test_get_next_frame(show_all_images = False):
    """Test get next frame function
    Show first and last frame and frame count"""
    print(" *** TESTING get_next_frame()")
    img = get_next_frame()
    if img is None:
        print("NO IMAGES LOADED")
        return
    print("IPM MASK")
    ipm_mask = get_ipm_mask()
    cv2.imshow("IPM Mask", ipm_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("First Image")
    counter = 1
    cv2.imshow("First Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ipm = get_inverse_perspective_matrix()
    birds_eye = cv2.warpPerspective(img, ipm, (img.shape[1],img.shape[0]))
    print("First Image Warped"),
    counter = 1
    cv2.imshow("First Image birds_eye", birds_eye)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    while img is not None:
        counter += 1
        prev_img = img
        img = get_next_frame()
        if show_all_images:
            cv2.imshow("Last Image", prev_img)
            cv2.waitKey(50)
    print("Last Image")
    print(str(counter) + " images in total")
    cv2.imshow("Last Image", prev_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(" --- END TEST get_next_frame()")


def test_get_next_feature():
    """Test function for get_next_feature()"""
    print(" *** TESTING get_next_feature()")
    feature_available, feature = get_next_feature()
    while feature_available:
        print("FEATURE: " + str(feature))
        feature_available, feature = get_next_feature()
    print(" --- END TEST get_next_feature()")

if __name__ == "__main__":
    init()
    test()
