import cv2
import numpy as np


#https://github.com/opencv/opencv/blob/master/samples/python/lk_track.py
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

MAX_OPTICAL_FEATURES = 30
def GetUpdatedRoadFeatureLocation(prev_image, this_frame_image, prev_road_feature_coord, optical_features=None, flow_mask=None):
    if optical_features is None:
        if flow_mask is None:
            flow_mask = np.zeros(this_image.shape, dtype=np.uint8)
        optical_features = cv2.goodFeaturesToTrack(prev_image, MAX_OPTICAL_FEATURES, 0.01, 0.01, mask=flow_mask)
    new_optical_features, _, _ = cv2.calcOpticalFlowPyrLK(prev_image, this_frame_image, optical_features, None, **lk_params)
    mean = [0, 0]
    for p in range(0, len(optical_features)):
        delta_0 = (optical_features[p][0][0] - new_optical_features[p][0][0])
        delta_1 = (optical_features[p][0][1] - new_optical_features[p][0][1])
        mean[0] = mean[0] + delta_0
        mean[1] = mean[1] + delta_1
    mean[0] = int(mean[0] / len(new_optical_features))
    mean[1] = int(mean[1] / len(new_optical_features))
    print("Mean Normalised = " + str(mean))
    feature_coord = (prev_road_feature_coord[0] + int(mean[1]), prev_road_feature_coord[1] + int(mean[0]))
    return feature_coord, new_optical_features