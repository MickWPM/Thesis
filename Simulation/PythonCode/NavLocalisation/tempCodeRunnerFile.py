import feature_tracker
import glob
import cv2
import numpy as np

TEST_IMAGE_PATH = ("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/"
                   "NavLocalisation/TestData/RouteImages")
TEST_IMAGES = []
def init_frames():
    """Initialise the frames by loading them into TEST_IMAGES list"""
    files = glob.glob(TEST_IMAGE_PATH + '/*.png')
    if files:
        for file in files:
            TEST_IMAGES.append(cv2.imread(file, 0))
    else:
        print("No files")

def TestOpticalFlow(show_flow_points=False):
    feature_coord=(64,77)
    for i in range(1, (len(TEST_IMAGES))):
        feature_coord, optical_features = feature_tracker.GetUpdatedRoadFeatureLocation(TEST_IMAGES[i-1], TEST_IMAGES[i], feature_coord)
        im = TEST_IMAGES[i].copy()
        if show_flow_points:
            for point in optical_features:
                cv2.circle(im, tuple(point[0]), 3, (125, 125, 125))
        cv2.circle(im, feature_coord, 5, (0,0,0))
        cv2.imshow("Flow IMG", im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()




init_frames()
TestOpticalFlow(True)

