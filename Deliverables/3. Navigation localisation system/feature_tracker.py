"""
Handle road feature management
Includes generating a feature mask based off an input feature
and testing against this mask
"""
import numpy as np
import cv2
import bezier

def get_feature_masks(feature, mask_dimension, road_width_px, include_bezier=True, driving_line_road_px=5, bezier_offset=(0,0)):
    """
    Get the raw feature masks for the approach. 
	Note this currently uses image coordinates - the real world distance to pixel coordinate transformation
		needs to occur prior to this point. This is a straight forward scaling factor however was not addressed
		in this implementation.
	feature: 
	mask_dimension: Pixel dimensions for mask
	road_width_px: Desired width of feature masks
	include_bezier: Include the driving line mask in the combined mask
	driving_line_road_px: Width of bezier
	bezier_offset: Pixel space offset for bezier curve control points.
		This was not used however allows more control over exact location of bezier curve relative to the road.
		While it is not likely this should be used, it could be used to `centralise' the driving line as currently
		the feature will be detected at the first possible moment. Using the offset will allow the curve to be `cast' 
		further along the road to an offset. Few cases likely where this is the best approach. Used a lot in testing and
		kept for posterity.
		
	Returns:
	feature_masks: Individual masks for feature nodes
	combined_mask: Combined mask for full feature
	curve_mask: Driving line specific mask
    """
    np_mask_dim = (mask_dimension[1], mask_dimension[0])
    feature_masks = []
    to_feature = np.zeros(np_mask_dim)
    col = (255,255,255)
    feature_point = feature[0]
    approach_point = feature[1]
    exit_point = feature[2]
	
	#Initially create the `inbound' mask.
    cv2.line(to_feature, approach_point, feature_point, col, thickness=road_width_px)
    feature_masks.append(to_feature.astype(np.uint8))
        
	#Append all other legs
    if len(feature) > 2:
        for i in range(2, n):
            mask = np.zeros(np_mask_dim)
            cv2.line(mask, feature_point, feature[i], col, thickness=road_width_px)
            feature_masks.append(mask.astype(np.uint8))
    
    
	#Driving line curve mask
    p1 = np.add(feature_point, bezier_offset)
    p2 = np.add(approach_point, bezier_offset)
    p3 = np.add(exit_point, bezier_offset)
    curve_mask=bezier.get_curve_mask(p1, p2, p3, width=driving_line_road_px, img_dimensions=mask_dimension)[:,:,0]
   
    if include_bezier:
        feature_masks.append(curve_mask)

    combined_mask = np.sum(feature_masks, axis=0).astype(np.uint8)
    return feature_masks, combined_mask, curve_mask

def shift_mask(mask, coord_shift, ipm_mask=None):    
	"""
	Shift a mask based off a provided x and y shift (corresponds to optical flow between frames)
	This is a 'long' method but is simply moving values in the array based off the shift.
	
	mask: Existing mask to be shifted
	coord_shift: Pixel shift required
	ipm_mask: IPM mask to apply
	
	Returns:
	mask: Shifted mask
	"""
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
    Considers features elementwise and determines if a feature is detected
	feature_mask: Individual sub feature masks
	road_surface: Detected road surface
	coord_shift: Amount to shift the mask by if flow has occurred
	probability_threshold: Minimum probability for feature to be considered detected
	ipm_mask: IPM mask to apply
	
	Returns:
	return detected: Boolean flag indicating if feature was detected
	mask_probabilities: Individual probability values for sub masks
    """
    coord_shift = (int(coord_shift[0]), int(coord_shift[1]))
    mask_probabilities = []
    masked_image = np.zeros(road_surface.shape, dtype=np.uint8)
    shifted = np.absolute(coord_shift[0]) > 0 or  np.absolute(coord_shift[1]) > 0
    
	for mask in feature_mask:
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        if shifted:
            mask = shift_mask(mask, coord_shift, ipm_mask=ipm_mask)
        _, _, feature_masked_image = mask_image(road_surface, mask)
        
        if masked_image.shape[0] != feature_masked_image.shape[0]:
            masked_image = np.swapaxes(masked_image, 0, 1)

		#masked_image for visualisation only
		#Not currently returned but this code can be amended if specific visualisations are required
        masked_image = np.add(masked_image, feature_masked_image )
        mask_probabilities.append(np.sum(feature_masked_image ) / np.sum(mask))
    
	#'Detected' depends on the minimum mask probability compared to the probability_threshold
    min_probability = np.amin(mask_probabilities)
    detected = min_probability>probability_threshold
	
    return detected,  mask_probabilities


def mask_image(im, im_mask, resize_dim=None, min_threshold=200):
    """
	Simple helper to mask an image
	im: Base image
	im_mask: Mask to apply
	resize_dim: Dimensions to resize base image to
	min_threshold: Minimum threshold to consider for binary masking
	
	Returns:
	im_thresh: Thresholded image
	im_raw: Base image (resized if applicable)
	im_masked: Masked image
	"""
    if resize_dim is None:
        im_raw = im.copy()
    else:
        im_raw = cv2.resize(im, resize_dim)
		
    _, im_thresh = cv2.threshold(im_raw, min_threshold, 255, cv2.THRESH_BINARY)
    im_thresh = np.array(im_thresh)
    
    im_masked = cv2.bitwise_and(im_thresh, im_thresh, mask=im_mask)
    return im_thresh, im_raw, im_masked

		
def GetUpdatedRoadFeatureLocationFarneback(prev_im, cur_im, feature_coord, flow=None):
	"""
	Estimate new feature coordinate based off Gunnar Farnback optical flow over region of interest
	prev_im: Previous frame
	cur_im: Current frame 
	feature_coord: Feature coordinate on previous frame
	flow: Previous flow
	
	Returns:
	feature_coord: Estimated coordinate in current image
	"""
	
	#Farnback method hyperparameters, experimentally determined
    pyr_scale=0.5
    levels	= 3
    winsize = 15
    iterations	= 3
    poly_n	= 5
    poly_sigma = 1.2
    flags = 0
    flow = cv2.calcOpticalFlowFarneback(prev_im, cur_im, flow, 0.5, 3, winsize, iterations, poly_n, poly_sigma, flags )

	#This represents the optical flow region of interest.
	#This is held here for initial testing however for production or extension
	#should be refactored to the data interface and passed through the nav_localisation script
	#It is left here for future rapid iteration.
    ave_x = np.mean(flow[130:390, 120:174, 0])
    ave_y = np.mean(flow[130:390, 120:174, 1])

    feature_coord = (feature_coord[0]+ave_x, feature_coord[1]+ave_y)
    return feature_coord
