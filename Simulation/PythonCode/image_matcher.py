import cv2
import numpy as np
import road_feature_tracking as tracker
import road_feature_matching as matcher


#T junction test
IMG_DIM = 512
cur_point = (int(IMG_DIM/2), int(IMG_DIM))
feature_point = (int(IMG_DIM/2), int(IMG_DIM/2)-int(IMG_DIM*10/64))
left_branch = (int(IMG_DIM*2/64), int(IMG_DIM*(10-5)/64))
right_branch = (int(IMG_DIM*61/64), int(IMG_DIM*(43-5)/64))
FEATURES = (cur_point, feature_point, left_branch, right_branch)

def GetTestFeatureMatcherImages():
    images = []
    test_image_names = ['img_18.png', 'img_20.png', 'img_33.png', 'img_57.png', 'img_63.png', 'img_74.png', 'img_83.png', 'img_89.png']
    for image_name in test_image_names:
        images.append(cv2.imread('img_matching/'+image_name, 0))
    return images

def FeatureMatcherUpdateLoop(image, feature_masks, mask_sums=None):
    if mask_sums is None:
        mask_sums = []
        for mask in masks:
            mask_sums.append(np.sum(mask))

#Temproary method to get the upcoming feature masks
def TMP_GetNextFeatureMasks():
    return matcher.CreateMasks(FEATURES, (IMG_DIM, IMG_DIM), 3)

#TMP!!!
FEATURE_PCT_THRESHOLD = 0.5
def TestIsFeature(feature_probabilities):
    for p in feature_probabilities:
        if p < FEATURE_PCT_THRESHOLD:
            return False
    return True

def TestFeatureMatcher():
    images = GetTestFeatureMatcherImages()
    next_road_feature_masks = TMP_GetNextFeatureMasks()

    for image in images:
        feature_probabilities, masked_image = matcher.CheckMasksProbability(image, next_road_feature_masks)
        if TestIsFeature(feature_probabilities):
            print("FEATURE FOUND AT " + str(feature_point))
        else:
            print("Feature not detected at"  + str(feature_point))
        #print("Feature probabilities for current image: " + str(feature_probabilities))
        cv2.imshow("Current feature", masked_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def TestOpticalFlow(show_flow_points=False):
    feature_coord = (296, 158) #This is hand placed for the 512x512 source images
    im_names = ['img_83.png', 'img_85.png', 'img_87.png', 'img_89.png']
    images = []
    for i in range(0, len(im_names)):
        im = cv2.imread('img_matching/'+im_names[i], 0)
        _, im = cv2.threshold(im, 200, 240, cv2.THRESH_BINARY)
        images.append( im )
    flow_mask = np.zeros(images[0].shape, dtype=np.uint8)
    flow_mask[60:300,140:380] = 1 #This is an approximate feature location and needs to be done mathemetically

    for i in range(1, (len(images))):
        feature_coord, optical_features = tracker.GetUpdatedRoadFeatureLocation(images[i-1], images[i], feature_coord, flow_mask=flow_mask)
        im = images[i].copy()
        if show_flow_points:
            for point in optical_features:
                cv2.circle(im, tuple(point[0]), 3, (125, 125, 125))
        cv2.circle(im, feature_coord, 5, (0,0,0))
        cv2.imshow("Flow IMG", im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

###DoMaskCheck()
TestFeatureMatcher()
#TestOpticalFlow(True)