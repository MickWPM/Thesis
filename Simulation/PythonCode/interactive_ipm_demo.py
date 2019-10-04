import cv2
import numpy as np

IPM_MATRIX=None
CURRENT_CLICK = False
IMG_WIDTH = 512
def on_mouse(event,x,y,flags,param):
    global CURRENT_CLICK
    if event == cv2.EVENT_LBUTTONDOWN and not CURRENT_CLICK:
        CURRENT_CLICK = True
        print("Coords: " + str((x,y)))
        if x >=IMG_WIDTH:
            #print("IPM CHANGE")
            change_ipm_point(x-IMG_WIDTH,y)
            #change_ipm_point(x-512,y)
        else:
            #print("IMG CHANGE")
            change_img_point(x,y)
        update_images()
    elif event == cv2.EVENT_LBUTTONUP:
        CURRENT_CLICK=False

POINT_COLOURS = [(200,100,50), (100,200,0), (200,100,150), (0,100,50)]
POINTS_IMG = [(50,50),(50,100),(100,100),(100,50)]
POINTS_IPM = [(50,50),(50,100),(100,100),(100,50)]
INDEX_IMG_POINTS = 0
INDEX_IPM_POINTS = 0

def change_ipm_point(x,y):
    global POINTS_IPM
    global INDEX_IPM_POINTS
    POINTS_IPM[INDEX_IPM_POINTS] = (x,y)
    INDEX_IPM_POINTS = (INDEX_IPM_POINTS+1)%4
    #print("INDEX_IPM_POINTS="+str(INDEX_IPM_POINTS) + ". POINTS: " + str(POINTS_IPM))
    

def change_img_point(x,y):
    global POINTS_IMG
    global INDEX_IMG_POINTS
    POINTS_IMG[INDEX_IMG_POINTS] = (x,y)
    INDEX_IMG_POINTS = (INDEX_IMG_POINTS+1)%4
    #print("INDEX_IMG_POINTS="+str(INDEX_IMG_POINTS) + ". POINTS: " + str(POINTS_IMG))

def update_ipm():
    global IPM_IMG
    if IPM_MATRIX is None:
        IPM_IMG = np.zeros_like(MAIN_IMG)
    else:
        IPM_IMG = cv2.warpPerspective(MAIN_IMG, IPM_MATRIX, (MAIN_IMG.shape[1], MAIN_IMG.shape[0]))


def update_images():
    global IPM_IMG
    global DISPLAY_IMG_WITH_POINTS
    DISPLAY_IMG_WITH_POINTS = MAIN_IMG.copy()
    update_ipm()
    for i in range(0, 4):
        cv2.circle(DISPLAY_IMG_WITH_POINTS, POINTS_IMG[i], 5, POINT_COLOURS[i], -1)
        cv2.circle(IPM_IMG, POINTS_IPM[i], 5, POINT_COLOURS[i], -1)



MAIN_IMG=None
IPM_IMG=None
DISPLAY_IMG_WITH_POINTS=None
def main():
    global MAIN_IMG
    global IMG_WIDTH
    global IPM_IMG
    global DISPLAY_IMG_WITH_POINTS
    global IPM_MATRIX
    print("RUN")
    folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/'
    im_path = 'InversePerspective/car_dashcam.jpg'
    #im_path = 'InversePerspective/unityCamCalibration.png'
    #im_path = 'InversePerspective/sce_c.png'
    
    MAIN_IMG = cv2.imread(folder_path+im_path)

    cv2.namedWindow('IPM Demo')
    cv2.setMouseCallback('IPM Demo', on_mouse)

    DISPLAY_IMG_WITH_POINTS = MAIN_IMG.copy()
    IMG_WIDTH = MAIN_IMG.shape[1]
    print(IMG_WIDTH)
    IPM_IMG = np.zeros_like(MAIN_IMG)
    update_images()
    run = True
    while run:
        update_images()
        img_combine = np.hstack((DISPLAY_IMG_WITH_POINTS, IPM_IMG))
        cv2.imshow('IPM Demo',img_combine)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 32:
            IPM_MATRIX = cv2.getPerspectiveTransform(np.float32(POINTS_IMG), np.float32(POINTS_IPM))
            print("Matrix calculated")
            update_images()
            
    
    np.save(folder_path + "InversePerspective/interactiveInverseMatrix", matrix)
    print("DONE")
    cv2.destroyAllWindows()


if __name__ == "__main__": main()