"""
Navigation localisation for final year thesis
Workflow:
    1. 
"""

import cv2
import test_data as td
import feature_tracker
import road_surface_detection

PROCESSING_RESOLUTION = (256, 256)

def get_next_frame(get_frame_method):
    frame = get_frame_method()
    print("TODO: RESIZE FRAME TO PROCESSING_RESOLUTION")
    return frame

def inverse_perspective_frame(frame, ipm):
    """Inverse perspective mapping on current frame"""
    #birds_eye = cv2.warpPerspective(frame, ipm, PROCESSING_RESOLUTION)
    birds_eye = frame
    print("TMP - NOT doing IPM")
    return birds_eye

def process_frame(frame, ipm, rsd):
    ipm_frame = inverse_perspective_frame(frame, ipm)
    
    res = rsd.get_road_surface_from_new_frame(frame)
    
    #identify road surface
    #feature already id'd?
    ##Estimate feature position using optical flow from raw image
    ##Confirm and refine feature estimate
    ##Update feature if needed (ie. have we passed a 'node')
    #ELSE
    ## check feature map against road surface
    ## IF id'd - Refine estimate

    cv2.imshow("roi ave", res)
    cv2.waitKey(50)

def main(data_interface):
    """
    Entry point for program
    data_interface: Interface to run data getter methods on
                    Such as get feature, get frame etc
    """
    data_interface.init()
    ipm = data_interface.get_inverse_perspective_matrix()
    ipm_mask = data_interface.get_ipm_mask()
    rsd = road_surface_detection.RoadSurfaceDetector(data_interface.HISTOGRAM_WINDOW, ipm_mask=ipm_mask)
    feature_found, feature = data_interface.get_next_feature()
    if not feature_found:
        print("NO FEATURES FOUND - EXITING")
        return
    frame = data_interface.get_next_frame()
    if frame is None:
        print("NO FRAMES FOUND - EXITING")
        return
    while (feature_found) and (frame is not None):
        process_frame(frame, ipm, rsd)
        frame = data_interface.get_next_frame()
    cv2.destroyAllWindows()
    print("END.")


if __name__ == "__main__":
    main(td)
