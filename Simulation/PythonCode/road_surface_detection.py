import numpy as np
import cv2

HIST_WINDOW = ((250, 460), (265, 500))

def OpenClose(img, iterations=1, kernel=np.ones((5,5),np.uint8)):
    for i in range(0, iterations):
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img

#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_histograms/py_histogram_backprojection/py_histogram_backprojection.html
def HistogramFromImgROI(img, roi, imgScale=1):
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
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    cv2.filter2D(dst,-1,disc,dst)
    # threshold and binary AND
    ret,thresh = cv2.threshold(dst,150,255,0)
    thresh = cv2.merge((thresh,thresh,thresh))
    thresh = OpenClose(thresh,iterations=1,kernel=np.ones((3,3),np.uint8))
    res = cv2.bitwise_and(img,thresh)

    img_ret = np.hstack((img, res))
    return roihist, img_ret

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

    print("ROI[1][1] = " + str(roi[1][1]))
    ave = np.mean(ROI_AVG, axis=0)
    ave=np.array(np.round(ave),dtype=np.uint8)
    print("AVE[1][1] = " + str(ave[1][1]))
    return ave

def main():
    print("ROAD SURFACE DETECTION TEST")
    folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/'
    ims = []
    ims.append( cv2.imread('InverseTransformed/a.png') )
    ims.append( cv2.imread('InverseTransformed/b.png') )
    ims.append( cv2.imread('InverseTransformed/c.png') )
    ims.append( cv2.imread('InverseTransformed/d.png') )

    #matrix = GetCameraMatrix(load_from_file=False)
    #img_combine = GetBirdsEye(matrix, img, return_combo_img= True)
 

    for im in ims:
        roi_ave = GetROIAvg(im)
        roi_hist, im = HistogramFromImgROI(im,roi_ave,imgScale = 0.125*4)
        cv2.imshow('Inverse Perspective Example',im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__": main()