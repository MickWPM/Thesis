"""
Navigation localisation for final year thesis
This script runs feature detection and tracking off provided data
It is an initial implementation of the developed algorithm however will
need to be extended for `live' usage to provide callbacks based on key events 
and information (such as feature detected, updated position, bezier curve data etc)
as well as generating subsequent features
"""

import cv2
import numpy as np
import test_data as td
import feature_tracker
import road_surface_detection

PROCESSING_RESOLUTION = (512, 512)

VISUALISATION_VIDEO_SAVE_PATH = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/Output/Videos/nav_localisation.avi'

def get_next_frame(get_frame_method):
	"""This method is a future proof placeholder to get the next frame.
	Additional work here can include resizing, for example:
	If the camera input frame is higher resolution than the desired processing"""
    frame = get_frame_method()
    return frame

def inverse_perspective_frame(frame, ipm):
    """Inverse perspective mapping on current frame. """
    birds_eye = cv2.warpPerspective(frame, ipm, PROCESSING_RESOLUTION)
    return birds_eye

#Processing variables
IPM_MASK=None	
FEATURE_IDENTIFIED = False
CURRENT_FEATURE_MASK = None
CURRENT_COMBINED_FEATURE_MASK = None
CURRENT_DRIVING_LINE = None
FEATURE_ROAD_WIDTH_PX = 25	
DRIVING_LINE_ROAD_WIDTH_PX = 10
FEAUTRE_COORD = None
FEAUTRE_COORD_FLOW = (0,0)
PREV_ROAD_SURFACE = None
RECORD_FRAME_OUTPUT = True
def process_frame(frame, feature, ipm, rsd):
	"""Process the individual frame
	Includes managing feature indentification or tracking/update
	frame: The current video frame to consider
	feature: The current generated feature to identify/track
	ipm: The inverse perspective matrix
	rsd: The road surface detector instance"""		
	global FEATURE_IDENTIFIED
    global FEAUTRE_COORD_FLOW
    global CURRENT_FEATURE_MASK
    global CURRENT_COMBINED_FEATURE_MASK
    global CURRENT_DRIVING_LINE
    global FEATURE_ROAD_WIDTH_PX
    global FEAUTRE_COORD
    global PREV_ROAD_SURFACE
    global RECORD_FRAME_OUTPUT
    ipm_frame = inverse_perspective_frame(frame, ipm)
    ipm_output = ipm_frame.copy()
    
    optical_track = cv2.cvtColor(ipm_frame, cv2.COLOR_BGR2GRAY)
	#Alternate optical flow approach is to use hue or saturation
    #optical_track = cv2.cvtColor(ipm_frame, cv2.COLOR_BGR2HSV)[:,:,0]
    #optical_track = cv2.cvtColor(ipm_frame, cv2.COLOR_BGR2HSV)[:,:,1]


    road_surface, road_surface_visualised = rsd.get_road_surface_from_new_frame(ipm_frame)
    if FEATURE_IDENTIFIED:
		#Useful for debugging but very spammy!
        #print("FEATURE IDENTIFIED")
        new_feature_coord = feature_tracker.GetUpdatedRoadFeatureLocationFarneback(PREV_ROAD_SURFACE, optical_track, FEAUTRE_COORD, None)
        FEAUTRE_COORD_FLOW = (FEAUTRE_COORD_FLOW[0] + new_feature_coord[0] - FEAUTRE_COORD[0],FEAUTRE_COORD_FLOW[1] + new_feature_coord[1] - FEAUTRE_COORD[1])
        FEAUTRE_COORD = new_feature_coord
		
        ##Confirm and refine feature estimate
        ##Update feature if needed (ie. have we passed a 'node')
        ## DONT FORGET TO SET FEATURE AS NOT IDENTIFIED WHEN OUTSIDE THE CORNER
        PREV_ROAD_SURFACE = optical_track.copy()
		
		
        #Get the pixel coordinate to draw the feature to for visualisation
        feature_draw_coord = (int(FEAUTRE_COORD[0]), int(FEAUTRE_COORD[1]))
        #NOTE: THIS SHOULD BE CAST BACK TO PERSPECTIVE MODE IF USED IN PERSPECTIVE IMAGES
		
        cv2.circle(optical_track, feature_draw_coord, 5, (0,0,255), thickness=3)
        cv2.circle(road_surface_visualised, feature_draw_coord, 5, (0,0,255), thickness=3)

		#Shift the mask based on the optical flow 
        shift = (int(FEAUTRE_COORD_FLOW[0]), int(FEAUTRE_COORD_FLOW[1]))
        driving_mask = CURRENT_DRIVING_LINE.copy()
        driving_mask = feature_tracker.shift_mask(driving_mask, shift)
        image1 = np.zeros_like(road_surface_visualised)
        image1[:,:,0] = 255

		#This portion is to visualise the detected road surface by using the 
		#detected road surface as a mask on the original image
		#This has no `real' use in the system but very effective for demonstration purposes
        A = cv2.bitwise_and(image1,image1,mask = driving_mask)
        B = cv2.bitwise_and(road_surface_visualised,road_surface_visualised,mask = 255-driving_mask)
        road_surface_visualised = np.add(A, B)
			
        FEATURE_IDENTIFIED,  mask_probabilities = feature_tracker.check_feature(CURRENT_FEATURE_MASK, road_surface, FEAUTRE_COORD_FLOW, ipm_mask=IPM_MASK)
        if not FEATURE_IDENTIFIED:
            print("LOST FEATURE")
			"""
			Logic here depends on implemented controller. 
			This code can be extended to provide a callback at this point to a controller.
			Options and considerations:
			1. If we have lost the feature - are we 'on' it (is the bottom of the generated mask at the bottom of the frame?
				Alternatively - Are we at the first node of the driving line?
			2. If we have just lost the feature (eg. due to optical flow errors) then we can start bracketing to relocate it.
				A naiive implementation is just a guess however a more intelligent approach might be to use previous optical flow
				to estimate how far we should bracket: If we HAD been tracking the feature we can consider multiples of the mean optical
				flow to estimate a more intelligent bracketing start point
			For the purposes of demonstration, at this point we will halt so it is clear the feature is lost.
			"""
            RECORD_FRAME_OUTPUT = False
            cv2.waitKey(0)
    else:
        if CURRENT_FEATURE_MASK is None:
            CURRENT_FEATURE_MASK, CURRENT_COMBINED_FEATURE_MASK, CURRENT_DRIVING_LINE = feature_tracker.get_feature_masks(feature, PROCESSING_RESOLUTION, FEATURE_ROAD_WIDTH_PX, driving_line_road_px=DRIVING_LINE_ROAD_WIDTH_PX)
                
        # check feature map against road surface
        FEATURE_IDENTIFIED,  mask_probabilities = feature_tracker.check_feature(CURRENT_FEATURE_MASK, road_surface)
        if FEATURE_IDENTIFIED:
            print("FEATURE DETECTED!")
            PREV_ROAD_SURFACE = optical_track.copy()
            FEAUTRE_COORD=feature[0]
            feature_draw_coord = (int(FEAUTRE_COORD[0]), int(FEAUTRE_COORD[1]))
            cv2.circle(road_surface_visualised, feature_draw_coord, 5, (0,0,255), thickness=3)
            
    #VISUALISATION
    if RECORD_FRAME_OUTPUT:
        store_output((frame, optical_track, road_surface_visualised), ipm)
    cv2.imshow("roi ave", optical_track)
    cv2.waitKey(30)

#Output images will be written as a video
OUTPUT_IMAGES = []
def store_output(output, ipm):
	"""Stores images in the desired output format
	This method was updated regularly based on what the desired video output was.
	"""
    driver_view, road_surface, road_surface_visualised = output
    road_surface_3 = cv2.merge((road_surface, road_surface, road_surface))
    pm_frame = inverse_perspective_frame(road_surface_visualised, np.linalg.inv(ipm) )
    img_combine = np.hstack((driver_view, road_surface_3, pm_frame))
    OUTPUT_IMAGES.append(img_combine)
    

VID_FPS = 20
def save_output():
	"""At the end of the localisation run, save the images contained in OUTPUT_IMAGES to video"""
    DIMS = (OUTPUT_IMAGES[0].shape[1], OUTPUT_IMAGES[0].shape[0])
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vid_path = VISUALISATION_VIDEO_SAVE_PATH
    out = cv2.VideoWriter(vid_path, 
                            fourcc, VID_FPS, DIMS, True)
    for vid_frame in OUTPUT_IMAGES:
        out.write(vid_frame)
    out.release()
    print("VIDEO SAVED")


def main(data_interface):
    """
    Entry point for program
    data_interface: Interface to run data getter methods on
                    Such as get feature, get frame etc
    """

    global IPM_MASK
    data_interface.init()

	#For testing purposes, allows skipping of early frames
	#This can be helpful if a video of only a key portion is desired
	startframe = 1
	
    curframe = 0

    ipm = data_interface.get_inverse_perspective_matrix()
    ipm_mask = data_interface.get_ipm_mask()
    IPM_MASK = ipm_mask
    rsd = road_surface_detection.RoadSurfaceDetector(data_interface.HISTOGRAM_WINDOW, ipm_mask=ipm_mask)
    feature = data_interface.get_next_feature()
    if feature is None:
        print("NO FEATURES FOUND - EXITING")
        return
    frame = data_interface.get_next_frame()
    if frame is None:
        print("NO FRAMES FOUND - EXITING")
        return
		
    while (feature is not None) and (frame is not None):
        curframe += 1
        if curframe > startframe:
            process_frame(frame, feature, ipm, rsd)
        frame = data_interface.get_next_frame()
		
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("END.")
    save_output()


if __name__ == "__main__":
    main(td)
