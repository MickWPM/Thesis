import cv2
import numpy as np


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

def mask_image(im, im_mask, resize_dim=None):
    if resize_dim is None:
        im_raw = im.copy()
    else:
        im_raw = cv2.resize(im, resize_dim)
    ###TODO: THIS THRESHOLD HERE SHOULD BE ALREADY DONE AT THIS STAGE!!!
    _, im_thresh = cv2.threshold(im_raw, 200, 255, cv2.THRESH_BINARY)
    im_thresh = np.array(im_thresh)
    im_mask = cv2.bitwise_and(im_thresh, im_thresh, mask=im_mask)
    return im_thresh, im_raw, im_mask

def CheckMasksProbability(image, masks):
    mask_probabilities = []
    masked_image = np.zeros(image.shape, dtype=np.uint8)
    for mask in masks:
        #TODO: GET RID OF THIS???
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        _, _, feature_masked_image = mask_image(image, mask)
        masked_image = np.add(masked_image, feature_masked_image )
        mask_probabilities.append(np.sum(feature_masked_image ) / np.sum(mask))
    return mask_probabilities, masked_image
