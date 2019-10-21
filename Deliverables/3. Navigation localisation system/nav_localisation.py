"""
Navigation localisation for final year thesis
Workflow:
    1. 
"""

import cv2
import numpy as np
import test_data as td
import feature_tracker
import road_surface_detection
import bezier

PROCESSING_RESOLUTION = (512, 512)

def get_next_frame(get_frame_method):
    frame = get_frame_method()
    print("TODO: RESIZE FRAME TO PROCESSING_RESOLUTION")
    return frame

def inverse_perspective_frame(frame, ipm):
    """Inverse perspective mapping on current frame"""
    birds_eye = cv2.warpPerspective(frame, ipm, PROCESSING_RESOLUTION)
    #birds_eye = frame
    #print("TMP - NOT doing IPM")
    return birds_eye

temp_DetectedNum = 0
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
OPTICAL_FEATURES = None
RECORD_FRAME_OUTPUT = True
def process_frame(frame, feature, ipm, rsd):
    global temp_DetectedNum
    global FEATURE_IDENTIFIED
    global FEAUTRE_COORD_FLOW
    global CURRENT_FEATURE_MASK
    global CURRENT_COMBINED_FEATURE_MASK
    global CURRENT_DRIVING_LINE
    global FEATURE_ROAD_WIDTH_PX
    global FEAUTRE_COORD
    global PREV_ROAD_SURFACE
    global OPTICAL_FEATURES
    global RECORD_FRAME_OUTPUT
    ipm_frame = inverse_perspective_frame(frame, ipm)
    ipm_output = ipm_frame.copy()
    
    optical_track = cv2.cvtColor(ipm_frame, cv2.COLOR_BGR2GRAY)
    #optical_track = cv2.cvtColor(ipm_frame, cv2.COLOR_BGR2HSV)[:,:,0]


    road_surface, road_surface_visualised = rsd.get_road_surface_from_new_frame(ipm_frame)
    #identify road surface
    #feature already id'd?
    if FEATURE_IDENTIFIED:
        print("FEATURE IDENTIFIED")
        ##Estimate feature position using optical flow from raw image
        #this is old?
        #flow_mask = np.zeros((optical_track.shape[0],optical_track.shape[1]), dtype=np.uint8)
        #flow_mask[feature[0][0]-80:feature[0][0]+80,feature[0][1]-80:feature[0][1]+80] = 1 #THIS USES 80PX AS A FEATURE SPACING - UPDATE TO NOT BE MAGIC
        #flow_mask = None
        
        #If we need more output images to test on
        #cv2.imwrite("D:\\GitRepos\\Uni\\Thesis\\Simulation\\PythonCode\\Output\\Images\\ipm\\ipm"+str(temp_DetectedNum)+".png", ipm_frame)
        #cv2.imwrite("D:\\GitRepos\\Uni\\Thesis\\Simulation\\PythonCode\\Output\\Images\\opticaltrack\\track"+str(temp_DetectedNum)+".png", optical_track)
        temp_DetectedNum += 1
        print("DETECTED = ", temp_DetectedNum)

        #FEAUTRE_COORD, OPTICAL_FEATURES = feature_tracker.GetUpdatedRoadFeatureLocation(PREV_ROAD_SURFACE, optical_track, FEAUTRE_COORD, optical_features=OPTICAL_FEATURES, flow_mask=flow_mask)
        new_feature_coord, OPTICAL_FEATURES = feature_tracker.GetUpdatedRoadFeatureLocationFarneback(PREV_ROAD_SURFACE, optical_track, FEAUTRE_COORD, None)
        FEAUTRE_COORD_FLOW = (FEAUTRE_COORD_FLOW[0] + new_feature_coord[0] - FEAUTRE_COORD[0],FEAUTRE_COORD_FLOW[1] + new_feature_coord[1] - FEAUTRE_COORD[1])
        #print("FEAUTRE_COORD_FLOW = ", FEAUTRE_COORD_FLOW)
        FEAUTRE_COORD = new_feature_coord
        ##Confirm and refine feature estimate
        ##Update feature if needed (ie. have we passed a 'node')
        ## DONT FORGET TO SET FEATURE AS NOT IDENTIFIED WHEN OUTSIDE THE CORNER
        PREV_ROAD_SURFACE = optical_track.copy()
        #TODO: THIS SHOULD BE CAST BACK TO PERSPECTIVE MODE IF USED IN PERSPECTIVE IMAGES
        feature_draw_coord = (int(FEAUTRE_COORD[0]), int(FEAUTRE_COORD[1]))
        
        #cv2.circle((optical_track.shape[0],optical_track.shape[1]), feature_draw_coord, 25, (255,255,255), -1)
        #cv2.circle(road_surface_visualised,feature_draw_coord, 25, (255,255,255), -1)
        cv2.circle(optical_track, feature_draw_coord, 5, (0,0,255), thickness=3)
        cv2.circle(road_surface_visualised, feature_draw_coord, 5, (0,0,255), thickness=3)


        
        shift = (int(FEAUTRE_COORD_FLOW[0]), int(FEAUTRE_COORD_FLOW[1]))
        driving_mask = CURRENT_DRIVING_LINE.copy()
        driving_mask = feature_tracker.shift_mask(driving_mask, shift)
        image1 = np.zeros_like(road_surface_visualised)
        image1[:,:,0] = 255

        #Wrapping code poor - this is for visualisation
        driving_mask[:230,:]=0

        A = cv2.bitwise_and(image1,image1,mask = driving_mask)
        B = cv2.bitwise_and(road_surface_visualised,road_surface_visualised,mask = 255-driving_mask)
        
        road_surface_visualised = np.add(A, B)
        cv2.imshow("driving_mask", driving_mask)
        cv2.imshow("Mask and line", road_surface_visualised)
        #cv2.waitKey(0)
        #Result = Image1 & driving_mask + Image2 & ~driving_mask;

        FEATURE_IDENTIFIED,  mask_probabilities = feature_tracker.check_feature(CURRENT_FEATURE_MASK, road_surface, FEAUTRE_COORD_FLOW, ipm_mask=IPM_MASK)
        if not FEATURE_IDENTIFIED:
            print("LOST FEATURE")
            #We have lost the feature - are we "on" it?
            ## If so then follow the interpolated curve
            #If not then search and highlight lost
            RECORD_FRAME_OUTPUT = False
            
            cv2.waitKey(0)
    else:
        if CURRENT_FEATURE_MASK is None:
            CURRENT_FEATURE_MASK, CURRENT_COMBINED_FEATURE_MASK, CURRENT_DRIVING_LINE = feature_tracker.get_feature_masks(feature, PROCESSING_RESOLUTION, FEATURE_ROAD_WIDTH_PX, driving_line_road_px=DRIVING_LINE_ROAD_WIDTH_PX)
                
        ## check feature map against road surface
        
        FEATURE_IDENTIFIED,  mask_probabilities = feature_tracker.check_feature(CURRENT_FEATURE_MASK, road_surface)
        if FEATURE_IDENTIFIED:
            print("FEATURE DETECTED! WOO")
            PREV_ROAD_SURFACE = optical_track.copy()
            FEAUTRE_COORD=feature[0]
            feature_draw_coord = (int(FEAUTRE_COORD[0]), int(FEAUTRE_COORD[1]))
            cv2.circle(road_surface_visualised, feature_draw_coord, 5, (0,0,255), thickness=3)
            
                
    #VISUALISATION
    
    #store_output((ipm_output, road_surface_visualised), ipm)
    if RECORD_FRAME_OUTPUT:
        store_output((frame, optical_track, road_surface_visualised), ipm)
    cv2.imshow("roi ave", optical_track)
    #cv2.imshow("roi ave", road_surface)
    cv2.waitKey(50)

OUTPUT_IMAGES = []
def store_output(output, ipm):
    driver_view, road_surface, road_surface_visualised = output
    road_surface_3 = cv2.merge((road_surface, road_surface, road_surface))
    pm_frame = inverse_perspective_frame(road_surface_visualised, np.linalg.inv(ipm) )
    img_combine = np.hstack((driver_view, road_surface_3, pm_frame))
    OUTPUT_IMAGES.append(img_combine)
    

VID_FPS = 20
def save_output():
    DIMS = (OUTPUT_IMAGES[0].shape[1], OUTPUT_IMAGES[0].shape[0])
    print(DIMS)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vid_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/Output/Videos/nav_localisation.avi'
    out = cv2.VideoWriter(vid_path, 
                            fourcc, VID_FPS, DIMS, True)
    for vid_frame in OUTPUT_IMAGES:
        out.write(vid_frame)
    out.release()
    print("VIDEO SAVED")


def main(data_interface):
    startframe = 100
    curframe = 0
    """
    Entry point for program
    data_interface: Interface to run data getter methods on
                    Such as get feature, get frame etc
    """
    global IPM_MASK
    data_interface.init()
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
