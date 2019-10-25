"""
Detector class which implements Histogram based road surface probability detection
"""

import cv2
import numpy as np

def ExtractROI(img, roi_window):
	"""
	Helper function to extract a region of interest
	img: Target image
	roi_window: Region of interest
	
	Returns:
	roi: An image containing the region of interest information
	"""
    x1, x2 = roi_window[0][0], roi_window[1][0]
    y1, y2 = roi_window[0][1], roi_window[1][1]
    roi = img[y1:y2, x1:x2]
    return roi

class RoadSurfaceDetector:
	"""
	Detector class implementing Histogram backprojection based road surface detection.
	Uses a rolling average ROI for backprojection
	"""
    def __init__(self, roi_window, roi_ave_count=2, kernel_size=(5, 5), ipm_mask=None):
        self.roi_window = roi_window
        self.roi_average = None
        self.ipm_mask = ipm_mask
        self.roi_ave_count = roi_ave_count	#How many frames to average the historgram ROI over
		#Convolution kernal is the filter that is used as part of the histogram backprojection
        self.convolution_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)

    def get_updated_roi_average(self, img):
		"""
		Updates the average ROI for backprojection
		img: The input image to extract the ROI from
		
		Returns:
		ave: The averaged ROI
		"""
        roi = ExtractROI(img, self.roi_window)
        if self.roi_average is None:
            self.roi_average = []
            for i in range(0, self.roi_ave_count):
                self.roi_average.append(roi)
        else:
            self.roi_average.pop(0)
            self.roi_average.append(roi)
        ave = np.mean(self.roi_average, axis=0)
        ave = np.array(np.round(ave), dtype=np.uint8)
        return ave
    
    def get_road_surface_from_new_frame(self, new_frame, use_hsv=True):
		"""
		Detect the road surface from a new frame
		
		new_frame: The new frame to detect the road surface on
		use_hsv: Use HSV rather than RGB for histogram. This resulted in improved detection
		
		Returns: 
		road_surface: Detected road surface 
		road_surface_visualised: Visualised detected road
		"""
        average_roi = self.get_updated_roi_average(new_frame)
        if use_hsv:
            average_roi = cv2.cvtColor(average_roi, cv2.COLOR_BGR2HSV)
            new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2HSV)
        roihist = cv2.calcHist([average_roi], [0, 1], None, [180, 256], [0, 180, 0, 256] )
        cv2.normalize(roihist, roihist, 0, 255, cv2.NORM_MINMAX)

        road_surface = cv2.calcBackProject([new_frame], [0,1], roihist, [0,180,0,256], 1)
        cv2.filter2D(road_surface, -1, self.convolution_kernel, road_surface)
        if self.ipm_mask is not None:
            road_surface = cv2.bitwise_and(road_surface, self.ipm_mask)

        #To visualise detected road
        # threshold and binary AND
        _, thresh = cv2.threshold(road_surface, 150, 255, 0)
        thresh = cv2.merge((thresh, thresh, thresh))
        if use_hsv:
            new_frame = cv2.cvtColor(new_frame, cv2.COLOR_HSV2BGR)
        road_surface_visualised = cv2.bitwise_and(new_frame, thresh)
        
        return road_surface, road_surface_visualised
