import cv2
import numpy as np

def process_image(im, im_mask):
    im_raw = cv2.resize(im, (64, 64))
    _, im_thresh = cv2.threshold(im_raw, 200, 255, cv2.THRESH_BINARY)
    im_thresh = np.array(im_thresh)
    im_mask = cv2.bitwise_and(im_thresh, im_thresh, mask=im_mask)
    return im_thresh, im_raw, im_mask

#T junction test
IMG_DIM = 64
cur_point = (int(IMG_DIM/2), int(IMG_DIM))
feature_point = (int(IMG_DIM/2), int(IMG_DIM/2)-10)
left_branch = (2, 10-5)
right_branch = (61, 43-5)
FEATURES = (cur_point, feature_point, left_branch, right_branch)

def CreateFullMask(features, mask_dimension, road_width_px):
    img = np.zeros(mask_dimension)
    col = (255,255,255)
    cur_point = features[0]
    feature_point = features[1]
    cv2.line(img, cur_point, feature_point, col, thickness=road_width_px)
    n = len(features)
    print(n)
    if len(features) > 2:
        for i in range(2, n):
            cv2.line(img, feature_point, features[i], col, thickness=road_width_px)

    return img.astype(np.uint8)


def CreateMask(features, mask_dimension, road_width_px):
    return_mask = np.zeros(mask_dimension)
    masks = CreateMasks(features, mask_dimension, road_width_px)
    for mask in masks:
        return_mask = np.add(return_mask, mask)

    return return_mask.astype(np.uint8)


def CreateMasks(features, mask_dimension, road_width_px):
    feature_masks = []
    to_feature = np.zeros(mask_dimension)
    col = (255,255,255)
    cur_point = features[0]
    feature_point = features[1]
    cv2.line(to_feature, cur_point, feature_point, col, thickness=road_width_px)
    feature_masks.append(to_feature.astype(np.uint8))
    n = len(features)
    print(n)
    if len(features) > 2:
        for i in range(2, n):
            mask = np.zeros(mask_dimension)
            cv2.line(mask, feature_point, features[i], col, thickness=road_width_px)
            feature_masks.append(mask.astype(np.uint8))

    return feature_masks



#img_template_path = 'img_matching/first_intersection.bmp'
#img_template = cv2.imread(img_template_path, 0)

#img_template = CreateMask(FEATURES, (IMG_DIM, IMG_DIM), 7)
#_, img_template = cv2.threshold(img_template, 200,255,cv2.THRESH_BINARY)
#mask_sum = np.sum(img_template)

def DoMaskCheck():

    mask_sums = []
    img_templates = CreateMasks(FEATURES, (IMG_DIM, IMG_DIM), 3)
    for mask in img_templates:
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        mask_sums.append(np.sum(mask))


    im_names = ['img_18.png', 'img_20.png', 'img_33.png', 'img_57.png', 'img_63.png', 'img_74.png', 'img_83.png', 'img_89.png']
    ims_thresh = []
    ims_raw = []
    ims_masked = []
    ims_pct = []

    # for i in range(0, len(im_names)):
    #     image = cv2.imread('img_matching/'+im_names[i], 0)
    #     img_thresh, img_raw, img_mask = process_image(image, img_template)
    #     ims_thresh.append(img_thresh)
    #     ims_raw.append(img_raw)
    #     ims_masked.append(img_mask)
    #     pct = np.sum(img_mask) / mask_sum
    #     ims_pct.append(pct)


    for i in range(0, len(im_names)):
        image = cv2.imread('img_matching/'+im_names[i], 0)
        for j in range(0, len(img_templates)):
            img_thresh, img_raw, img_mask = process_image(image, img_templates[j])
            ims_thresh.append(img_thresh)
            ims_raw.append(img_raw)
            ims_masked.append(img_mask)
            pct = np.sum(img_mask) / mask_sums[j]
            ims_pct.append(pct)


    cv2.imshow('image',img_templates[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    for i in range(0, len(ims_thresh)):
        if i % len(img_templates) == 0:
            print("--- Next point ---")
        im_thresh = ims_thresh[i]
        im_masked = ims_masked[i]
        im_pct = ims_pct[i]
        print('Percent = ' + "{:3.2f}".format(im_pct*100) + '%')
        vis = np.concatenate((im_thresh, im_masked), axis=1)
        cv2.imshow('Image', vis)
        #cv2.imshow('Raw image',im_raw)
        #cv2.imshow('Masked image',im_masked)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



def DoOpticalFlow():
    im_names = ['img_83.png', 'img_85.png', 'img_87.png', 'img_89.png']
    images = []
    for i in range(0, len(im_names)):
        images.append( cv2.imread('img_matching/'+im_names[i], 0) )



    flow_points = cv2.goodFeaturesToTrack(images[0], 6, 0.01, 0.01)
    for i in range(0, (len(images)-1)):
        p1, _st, _err = cv2.calcOpticalFlowPyrLK(images[i], images[i+1], flow_points, None, **lk_params)
        print('Points:' + str(p1))
        flow_points = p1

#DoMaskCheck()

#https://github.com/opencv/opencv/blob/master/samples/python/lk_track.py
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
DoOpticalFlow()