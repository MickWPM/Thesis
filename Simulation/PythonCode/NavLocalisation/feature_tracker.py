"""
Handle road feature management
Includes generating a feature mask based off an input feature
and testing against this mask
Feature uses meters as scale
"""
import numpy as np
import cv2
import bezier

#TODO: Where is feature set for initial matching?
#TODO: scale feature based on distance of IPM image? #TODO: Add distance scaling based off ipm image total distance
#CURRENTLY IT IS PASSED AS IMAGE COORDINATES WHICH IS NOT THE PROPER WAY!!!
def get_feature_masks(feature, mask_dimension, road_width_px, include_bezier=True, driving_line_road_px=5, bezier_offset=(0,0)):
    """
    Get the raw feature masks for the approach. 
    """
    np_mask_dim = (mask_dimension[1], mask_dimension[0])
    feature_masks = []
    to_feature = np.zeros(np_mask_dim)
    col = (255,255,255)
    feature_point = feature[0]
    approach_point = feature[1]
    exit_point = feature[2]
    cv2.line(to_feature, approach_point, feature_point, col, thickness=road_width_px)
    feature_masks.append(to_feature.astype(np.uint8))
    print("road_width_px=",road_width_px)
        
    n = len(feature)
    print(n)
    if len(feature) > 2:
        for i in range(2, n):
            mask = np.zeros(np_mask_dim)
            cv2.line(mask, feature_point, feature[i], col, thickness=road_width_px)
            feature_masks.append(mask.astype(np.uint8))
    
    
    p1 = np.add(feature_point, bezier_offset)
    p2 = np.add(approach_point, bezier_offset)
    p3 = np.add(exit_point, bezier_offset)
    print("driving_line_road_px=",driving_line_road_px)
    curve_mask=bezier.get_curve_mask(p1, p2, p3, width=driving_line_road_px, img_dimensions=mask_dimension)[:,:,0]
    
    print("TEST")
    print(mask_dimension)
    print(curve_mask.shape)

    if include_bezier:
        feature_masks.append(curve_mask)

    combined_mask = np.sum(feature_masks, axis=0).astype(np.uint8)

    cv2.imshow("curve_mask",curve_mask)
    cv2.imshow("combined_mask",combined_mask)
    cv2.waitKey(0)

    return feature_masks, combined_mask, curve_mask



def update_feature_masks(distance_from_feature, feature, mask_resolution, ipm_distance_range=20):
    """
    As per get_feature_masks however feature distance is less than the initial tracking distance
    """
    pass

def shift_mask(mask, coord_shift, ipm_mask=None):    
    if  np.absolute(coord_shift[0]) > 0 and  np.absolute(coord_shift[1]) > 0:
        #Move X to the right
        if coord_shift[0] < 0:
            #Move X to the right and Y UP
            if coord_shift[1] < 0:
                mask[0:coord_shift[1], -coord_shift[0]:] = mask[-coord_shift[1]:, 0:coord_shift[0]]
                mask[coord_shift[1]:, :-coord_shift[0]] = 0
                

            #Move X to the right and Y Down
            elif coord_shift[1] > 0:
                mask[coord_shift[1]:, -coord_shift[0]:] = mask[:-coord_shift[1], 0:coord_shift[0]]
                mask[0:coord_shift[1], :-coord_shift[0]] = 0
                


        #Move X to the left
        elif coord_shift[0] > 0:
            #Move X to the left and y UP
            if coord_shift[1] < 0:
                mask[0:coord_shift[1], 0:-coord_shift[0]] = mask[-coord_shift[1]:, coord_shift[0]:]
                mask[coord_shift[1]:, -coord_shift[0]:] = 0
                

            #Move X to the left and y DOWN
            elif coord_shift[1] > 0:
                mask[coord_shift[1]:, 0:-coord_shift[0]] = mask[:-coord_shift[1], coord_shift[0]:]
                mask[0:coord_shift[1], -coord_shift[0]:] = 0
                


    elif np.absolute(coord_shift[0]) > 0:
        #At this point, Y is zero, so just move X
        #Move X RIGHT
        if coord_shift[0] < 0:
            mask[:, -coord_shift[0]:] = mask[:, 0:coord_shift[0]]
            mask[:, :-coord_shift[0]] = 0
        #Move X LEFT
        else:
            mask[:, 0:-coord_shift[0]] = mask[:, coord_shift[0]:]
            mask[:, -coord_shift[0]:] = 0


    elif np.absolute(coord_shift[1]) > 0:
        #At this point, X is zero, so just move Y
        #Move UP
        if coord_shift[1] < 0:
            mask[0:coord_shift[1], :] = mask[-coord_shift[1]:, :]
            mask[coord_shift[1]:, :] = 0

        #Move DOWN
        elif coord_shift[1] > 0:    
            mask[coord_shift[1]:, :] = mask[:-coord_shift[1], :]
            mask[0:coord_shift[1], :] = 0

    if ipm_mask is not None:
        mask = cv2.bitwise_and(mask, mask, mask=ipm_mask)
    return mask

def check_feature(feature_mask, road_surface, coord_shift=(0,0), probability_threshold=0.7, ipm_mask=None):
    """
    Considers features elementwise
    """
    coord_shift = (int(coord_shift[0]), int(coord_shift[1]))
    mask_probabilities = []
    masked_image = np.zeros(road_surface.shape, dtype=np.uint8)
    shifted = np.absolute(coord_shift[0]) > 0 or  np.absolute(coord_shift[1]) > 0
    
    #TMP
    #mask_unshifted = np.zeros(road_surface.shape, dtype=np.uint8)

    for mask in feature_mask:
        #TODO: GET RID OF THIS threshold??
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        
        #TMP
        #mask_unshifted = np.add(mask_unshifted, mask )

        if shifted:
            mask = shift_mask(mask, coord_shift, ipm_mask=ipm_mask)

        _, _, feature_masked_image = mask_image(road_surface, mask)
        
        #im = np.swapaxes(im, 0, 1)
        if masked_image.shape[0] != feature_masked_image.shape[0]:
            masked_image = np.swapaxes(masked_image, 0, 1)

        masked_image = np.add(masked_image, feature_masked_image )
        mask_probabilities.append(np.sum(feature_masked_image ) / np.sum(mask))
    #masked_image for visualisation only
    
    #Visualise movement of mask
    #if shifted:
    #    cv2.imshow("Pre shift", mask_unshifted)
    #    cv2.waitKey(0)
    #    cv2.imshow("Post shift", masked_image)
    #    cv2.waitKey(0)

    min_probability = np.amin(mask_probabilities)
    print("min_probability = ", min_probability)
    detected = min_probability>probability_threshold
    return detected,  mask_probabilities
    #return lowestProbability>probability_threshold, individualProbabilities


def mask_image(im, im_mask, resize_dim=None):
    
    if resize_dim is None:
        im_raw = im.copy()
    else:
        im_raw = cv2.resize(im, resize_dim)
    ###TODO: THIS THRESHOLD HERE SHOULD BE ALREADY DONE AT THIS STAGE!!!
    _, im_thresh = cv2.threshold(im_raw, 200, 255, cv2.THRESH_BINARY)
    im_thresh = np.array(im_thresh)
    
    im_masked = cv2.bitwise_and(im_thresh, im_thresh, mask=im_mask)
    return im_thresh, im_raw, im_masked

def CheckMasksProbability(image, masks):
    mask_probabilities = []
    masked_image = np.zeros(image.shape, dtype=np.uint8)
    for mask in masks:
        #TODO: GET RID OF THIS threshold??
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        _, _, feature_masked_image = mask_image(image, mask)
        masked_image = np.add(masked_image, feature_masked_image )
        mask_probabilities.append(np.sum(feature_masked_image ) / np.sum(mask))
    return mask_probabilities, masked_image


def GetUpdatedRoadFeatureLocationFarneback(prev_im, cur_im, feature_coord, flow=None):
    pyr_scale=0.5
    levels	= 3
    winsize = 15
    iterations	= 3
    poly_n	= 5
    poly_sigma = 1.2
    flags = 0
    flow = cv2.calcOpticalFlowFarneback(prev_im, cur_im, flow, 0.5, 3, winsize, iterations, poly_n, poly_sigma, flags )


    
    ave_x = np.mean(flow[130:390, 120:174, 0])
    ave_y = np.mean(flow[130:390, 120:174, 1])


    feature_coord = (feature_coord[0]+ave_x, feature_coord[1]+ave_y)
    optical_features = None
    return feature_coord, optical_features


#https://github.com/opencv/opencv/blob/master/samples/python/lk_track.py
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

MAX_OPTICAL_FEATURES = 20
def GetUpdatedRoadFeatureLocation(prev_image, this_frame_image, prev_road_feature_coord, optical_features=None, flow_mask=None):
    if optical_features is None:
        if flow_mask is None:
            print("No flow mask")
            flow_mask = np.ones(this_frame_image.shape, dtype=np.uint8)
            print("Mask shape = " + str(flow_mask.shape))
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
    feature_coord = (prev_road_feature_coord[0] - int(mean[0]), prev_road_feature_coord[1] - int(mean[1]))
    return feature_coord, new_optical_features