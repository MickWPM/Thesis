"""
Getter file for test data. This file can be changed for testing of different features and streams
Implements required methods for nav_localisation data getter. These are:
    feature = get_next_feature()			  #Return next feature or None if no more available
    frame = get_next_frame()				  #Next image frame (either from video stream or saved images)
    ipm = get_inverse_perspective_matrix()    #Matrix for frame inverse perspective mapping
    ipm_mask = get_ipm_mask()                 #Mask for inverse perspective mapped image (for road surface detection masking)
"""

import glob     #Reading directory of test images
import cv2
import numpy as np

#ROI for histogram backprojection
HISTOGRAM_WINDOW = ((245, 440), (267, 504))

#Example single test feature in pixel coordinates
TEST_FEATURES = []
FEATURE_POINT=(255,333-100)
BOTTOM_POINT=(255,413-100)
LEFT_POINT=(175, 333-100)
RIGHT_POINT=(335, 333-100)
feature_1 = (FEATURE_POINT, BOTTOM_POINT, LEFT_POINT, RIGHT_POINT)

def get_next_feature():
    """
    Get the next road feature (if available)
    returns feature (None if no feature found)
    """
    if not TEST_FEATURES:
        return None
    feature = TEST_FEATURES.pop(0)
    return feature

def get_next_frame():
    """Return the next frame for processing or
    None if it doesnt exist"""
    if TEST_IMAGES:
        return TEST_IMAGES.pop(0)
    return None

#Path to saved inverse perspective matrix
IPM_PATH = ("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/"
            "NavLocalisation/TestData/inverse_perspective_matrix.npy")
def get_inverse_perspective_matrix():
    """Return the saved inverse perspective matrix"""
    ipm = np.load(IPM_PATH)
    return ipm

def get_ipm_mask():
	"""Return a mask representing the area of information in the IPM transformed image"""
    birds_eye = cv2.warpPerspective(TEST_IMAGES[0], get_inverse_perspective_matrix(), (TEST_IMAGES[0].shape[0],TEST_IMAGES[0].shape[1]))
    _, thresh = cv2.threshold(birds_eye, 1, 255, cv2.THRESH_BINARY)
    return thresh[:, :, 0]

def init_features():
    """Initialise features by loading them into TEST_FEATURES list"""
    TEST_FEATURES.append(feature_1)

TEST_IMAGE_PATH = ("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/"
                   "NavLocalisation/TestData/RouteImages")
TEST_IMAGES = []
def init_frames():
    """Initialise the frames by loading them into TEST_IMAGES list"""
    files = glob.glob(TEST_IMAGE_PATH + '/*.png')
    if files:
        for file in files:
            TEST_IMAGES.append(cv2.imread(file))
    else:
        print("No files")

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
    birds_eye = cv2.warpPerspective(img, ipm, (img.shape[0],img.shape[1]))
	
    print("First Image Warped"),
    counter = 1
    cv2.imshow("First Image birds_eye", birds_eye)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
	
	#Run through all images:
	#Maintain count and show if flag is true
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

#We can run this file to test out the data
if __name__ == "__main__":
    init()
    test()
