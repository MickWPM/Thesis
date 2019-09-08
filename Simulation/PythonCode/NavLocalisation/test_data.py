"""
Getter file for test data. This file can be changed for testing of different features and streams
Implements required methods for nav_localisation data getter:
    feature_available, feature = get_next_feature()
    frame = get_next_frame()
    ipm = get_inverse_perspective_matrix()    #Matrix for frame inverse perspective mapping
"""

import glob     #Reading directory of test images
import cv2

TEST_FEATURES = []
def get_next_feature():
    """
    Get the next road feature (if available)
    returns feature_available, feature
    """
    if not TEST_FEATURES:
        return False, None
    feature = TEST_FEATURES.pop(0)
    return True, feature

def get_next_frame():
    """Return the next frame for processing or
    None if it doesnt exist"""
    if TEST_IMAGES:
        return TEST_IMAGES.pop(0)
    return None

def get_inverse_perspective_matrix():
    print("TODO: ADD IN IPM HERE!!!! ADD DOCSTRING ONLY WHEN THIS IS IMPLEMENTED")
    return None

def init_features():
    """Initialise features by loading them into TEST_FEATURES list"""
    TEST_FEATURES.append("Feature1")
    TEST_FEATURES.append("Feature1")
    TEST_FEATURES.append("Feature1")

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
    counter = 1
    print("First Image")
    cv2.imshow("First Image", img)
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
