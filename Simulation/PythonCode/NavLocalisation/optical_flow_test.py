import feature_tracker
import test_data
import glob
import cv2
import numpy as np

useLk = False
OUTPUT_IMAGES = []
def GetUpdatedRoadFeatureLocation(prev_im, cur_im, feature_coord, flow=None):
    if useLk:
        return GetUpdatedRoadFeatureLocationLK(prev_im, cur_im, feature_coord)

    return GetUpdatedRoadFeatureLocationFarneback(prev_im, cur_im, feature_coord, flow)


def GetUpdatedRoadFeatureLocationFarneback(prev_im, cur_im, feature_coord, flow):
    pyr_scale=0.5
    levels	= 3
    winsize = 15
    iterations	= 3
    poly_n	= 5
    poly_sigma = 1.2
    flags = 0
    flow = cv2.calcOpticalFlowFarneback(prev_im, cur_im, flow, 0.5, 3, winsize, iterations, poly_n, poly_sigma, flags )

    #ave_x = np.average(flow[:, :, 0], weights=(np.absolute(flow[:, :, 0]) > 0.2))
    #ave_y = np.average(flow[:, :, 1], weights=(np.absolute(flow[:, :, 0]) > 0.2))

    ave_x = np.mean(flow[400:500, 240:276, 0])
    ave_y = np.mean(flow[400:500, 240:276, 1])

    #print("Ave flow = (" , ave_x, ", ", ave_y, ")")
    feature_coord = (feature_coord[0]+ave_x, feature_coord[1]+ave_y)
    optical_features = None
    return feature_coord, optical_features

def GetUpdatedRoadFeatureLocationLK(prev_im, cur_im, feature_coord):
    feature_coord, optical_features = feature_tracker.GetUpdatedRoadFeatureLocation(prev_im, cur_im, feature_coord)
    return feature_coord, optical_features

TEST_IMAGE_PATH = ("D:/GitRepos/Uni/Thesis/Simulation/PythonCode/"
                   "NavLocalisation/TestData/RouteImages")
TEST_IMAGES = []
def init_frames():
    """Initialise the frames by loading them into TEST_IMAGES list"""
    
    ipm = test_data.get_inverse_perspective_matrix()
    
    files = glob.glob(TEST_IMAGE_PATH + '/*.png')
    if files:
        for file in files:
            img = cv2.imread(file, 0)
            birds_eye = cv2.warpPerspective(img, ipm, (img.shape[0],img.shape[1]))
            #TEST_IMAGES.append(cv2.imread(file, 0))
            TEST_IMAGES.append(birds_eye)
    else:
        print("No files")


VID_FPS = 20
def save_output():
    DIMS = (OUTPUT_IMAGES[0].shape[1], OUTPUT_IMAGES[0].shape[0])
    print(DIMS)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vid_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/Output/Videos/optical_flow.avi'
    out = cv2.VideoWriter(vid_path, 
                            fourcc, VID_FPS, DIMS, True)
    for vid_frame in OUTPUT_IMAGES:
        vid_frame_3 = cv2.merge((vid_frame, vid_frame, vid_frame))
        out.write(vid_frame_3)
    out.release()
    print("VIDEO SAVED")

def TestOpticalFlow(show_flow_points=False):
    global OUTPUT_IMAGES
    start_frame = 150
    end_frame = 290
    feature_coord=(256,300)
    #for i in range(1, (len(TEST_IMAGES))):
    for i in range(start_frame, end_frame):
        feature_coord, optical_features = GetUpdatedRoadFeatureLocation(TEST_IMAGES[i-1], TEST_IMAGES[i], feature_coord)
        #Demo tracking a feature coordinate - if it goes off screen, reset to track a new point
        if feature_coord[1] > 512:
                feature_coord=(256,300)

        im = TEST_IMAGES[i].copy()
        if show_flow_points and optical_features is not None:
            for point in optical_features:
                cv2.circle(im, tuple(point[0]), 4, (125, 125, 125), thickness=-1)
        cv2.circle(im, (int(feature_coord[0]), int(feature_coord[1])), 5, (0,0,255), thickness=3)
        cv2.imshow("Flow IMG", im)
        OUTPUT_IMAGES.append(im)
        cv2.waitKey(10)
        
    save_output()


init_frames()
TestOpticalFlow(True)
cv2.destroyAllWindows()
