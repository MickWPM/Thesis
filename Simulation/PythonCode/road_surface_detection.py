import numpy as np
import cv2
import glob


#HIST_WINDOW = ((x1, y1), (x2, y2))
#HIST_WINDOW = ((124, 200), (174, 300))

#IPM from dashcam
#HIST_WINDOW = ((200,124), (300,174))

#Unity simulation IPM window
HIST_WINDOW = ((250, 460), (265, 500))




def OpenClose(img, iterations=1, kernel=np.ones((5,5),np.uint8)):
    for i in range(0, iterations):
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img

#Modified from
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_histograms/py_histogram_backprojection/py_histogram_backprojection.html
def HistogramFromImgROI(img, roi, imgScale=1, filter=(5,5)):
    x1, x2 = HIST_WINDOW[0][0], HIST_WINDOW[1][0]
    y1, y2 = HIST_WINDOW[0][1], HIST_WINDOW[1][1]
    newX,newY = img.shape[1]*imgScale, img.shape[0]*imgScale
    x1 = int(x1 * imgScale)
    x2 = int(x2 * imgScale)
    y1 = int(y1 * imgScale)
    y2 = int(y2 * imgScale)
    img = cv2.resize(img,(int(newX),int(newY)))

    roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    roihist = cv2.calcHist([roi],[0, 1], None, [180, 256], [0, 180, 0, 256] )
    hsvt = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)

    dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,filter)
    cv2.filter2D(dst,-1,disc,dst)
    # threshold and binary AND
    ret,thresh = cv2.threshold(dst,150,255,0)
    thresh = cv2.merge((thresh,thresh,thresh))
    thresh = OpenClose(thresh,iterations=1,kernel=np.ones((3,3),np.uint8))
    res = cv2.bitwise_and(img,thresh)

    img_ret = np.hstack((img, res))
    return dst, img_ret

def ExtractROI(img, imgScale=1):
    x1, x2 = HIST_WINDOW[0][0], HIST_WINDOW[1][0]
    y1, y2 = HIST_WINDOW[0][1], HIST_WINDOW[1][1]
    newX,newY = img.shape[1]*imgScale, img.shape[0]*imgScale
    x1 = int(x1 * imgScale)
    x2 = int(x2 * imgScale)
    y1 = int(y1 * imgScale)
    y2 = int(y2 * imgScale)
    img = cv2.resize(img,(int(newX),int(newY)))
    roi = img[y1:y2, x1:x2]
    return roi

ROI_AVG_FRAMES = 3
ROI_AVG = []
def GetROIAvg(img, imgScale=1):
    roi = ExtractROI(img, imgScale)
    if len(ROI_AVG) < 1:
        for i in range(0,ROI_AVG_FRAMES):
            print("Append")
            ROI_AVG.append(roi)
    else:
        ROI_AVG.pop(0)
        ROI_AVG.append(roi)

    #print("ROI[1][1] = " + str(roi[1][1]))
    ave = np.mean(ROI_AVG, axis=0)
    ave=np.array(np.round(ave),dtype=np.uint8)
    #print("AVE[1][1] = " + str(ave[1][1]))
    return ave

def GetBirdsEye(matrix, img, return_combo_img = False):
    birds_eye = cv2.warpPerspective(img, matrix, (img.shape[1], img.shape[0]))
    img_a = cv2.copyMakeBorder(img,10,10,10,5,cv2.BORDER_CONSTANT)
    img_b = cv2.copyMakeBorder(birds_eye,10,10,5,10,cv2.BORDER_CONSTANT)
    img_combine = np.hstack((img_a, img_b))
    # RETURN COMBINE
    if return_combo_img:
        return img_combine
    return birds_eye

VID_FPS = 30
def save_output(filename="road_surface_detection.avi", save_shape=None):
    if save_shape is None:
        save_shape = (OUTPUT_IMAGES[0].shape[1], OUTPUT_IMAGES[0].shape[0])
    print(save_shape)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vid_path = "D:\\GitRepos\\Uni\\Thesis\\Simulation\\PythonCode\\Output\\Videos\\"+str(filename)
    print(vid_path)
    out = cv2.VideoWriter(vid_path, 
                            fourcc, VID_FPS, save_shape, True)
    for vid_frame in OUTPUT_IMAGES:
        if len(vid_frame.shape) == 2:
            vid_frame_3 = cv2.merge((vid_frame, vid_frame, vid_frame))
            out.write(vid_frame_3)
        else:
            out.write(vid_frame)
    out.release()
    print("VIDEO SAVED")

#TEST_IMAGE_PATH = "D:/GitRepos/Uni/Thesis/Simulation/PythonCode/InversePerspective/dashcam"
TEST_IMAGE_PATH = "C:/Users/MIchael/Documents/GitHub/Thesis/Simulation/PythonCode/InversePerspective/dashcam"
INPUT_IMAGES = []
OUTPUT_IMAGES = []
def demo_all_images():
    print("ROAD SURFACE DETECTION TEST")

    #folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/'
    folder_path = 'C:/Users/MIchael/Documents/GitHub/Thesis/Simulation/PythonCode/'
    global INPUT_IMAGES
    global OUTPUT_IMAGES

    

    """Initialise the frames by loading them into TEST_IMAGES list"""
    files = glob.glob(TEST_IMAGE_PATH + '/*.png')
    if files:
        files = sorted(files)

        for file in files:
            INPUT_IMAGES.append(cv2.imread(file))
    else:
        print("No files")

    #matrix = GetCameraMatrix(load_from_file=True)

    #matrix_folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/'
    matrix_folder_path = 'C:/Users/MIchael/Documents/GitHub/Thesis/Simulation/PythonCode/'
    matrix = np.load(matrix_folder_path + "CameraInverseMatrix.npy")

    #im_path = "D:\\GitRepos\\Uni\\Thesis\\Simulation\\PythonCode\\Output\\Images\\dashcam\\"
    im_path = "C:\\Users\\MIchael\\Documents\\GitHub\\Thesis\\Simulation\\PythonCode\\Output\\Images\\dashcam\\"
    im_num = 0

    ipmFirst = True
    for im in INPUT_IMAGES:
        if ipmFirst:
            birdsEye = GetBirdsEye(matrix, im, return_combo_img= False)
            img_combine = GetBirdsEye(matrix, im, return_combo_img= True)
            roi_ave = GetROIAvg(birdsEye)
            roi_hist, im_ret = HistogramFromImgROI(birdsEye,roi_ave, filter=(7,7))
            roi3 = cv2.merge((roi_hist, roi_hist, roi_hist))
        else:
            roi_ave = GetROIAvg(im)
            roi_hist, im_ret = HistogramFromImgROI(im,roi_ave, filter=(7,7))
            roi3 = cv2.merge((roi_hist, roi_hist, roi_hist))
            #cv2.imshow("roi_ave",roi_ave)
            birdsEye = GetBirdsEye(matrix, roi3, return_combo_img= False)
            #cv2.imshow("birdsEye",birdsEye)
            img_combine = GetBirdsEye(matrix, roi_hist, return_combo_img= True)
            #cv2.imshow("img_combine",img_combine)


        #print("birdsEye.shape=", birdsEye.shape)
        #print("roi_hist.shape=", roi_hist.shape)
        #print("im_ret.shape=", im_ret.shape)



        roi3 = cv2.merge((roi_hist, roi_hist, roi_hist))

        #print(im.shape)
        #print(birdsEye.shape)
        #print(roi3.shape)
        combined = np.hstack((im, birdsEye, roi3))
        OUTPUT_IMAGES.append(combined)
        

        filename = "dashcam"
        if im_num < 10:
            filename += "000"
        elif im_num < 100:
            filename += "00"
        elif im_num < 1000:
            filename += "0"
        filename += str(im_num) + ".png"
        pth =im_path + filename
        cv2.imwrite(pth, combined)
        im_num+=1
        #print("Saved image to ", pth)

        cv2.imshow('combined',combined)
        cv2.waitKey(30)
    save_output()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    #demo_all_images()
    im = cv2.imread(r"C:\Users\MIchael\Documents\GitHub\Thesis\Simulation\PythonCode\NavLocalisation\TestData\RouteImages\img_241.png")
    matrix = np.load(r"C:\Users\MIchael\Documents\GitHub\Thesis\Simulation\PythonCode\unityCameraInverseMatrix.npy")
    birds_eye = GetBirdsEye(matrix, im)
    roi_ave = GetROIAvg(birds_eye)
    roi_hist, im_ret = HistogramFromImgROI(birds_eye, roi_ave)

    cv2.imshow("im", roi_hist)
    cv2.waitKey(0)
    cv2.destroyAllWindows()