import cv2
import numpy as np


folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/'
im_path = 'unityCamCalibration.png'
img = cv2.imread(im_path)

def GetCameraMatrix(load_from_file = False):
    if load_from_file:
        matrix = np.load(folder_path + "unityCameraInverseMatrix.npy")
        return matrix

    show_guides = False

    a = (223,264)
    b= (288,264)
    c = (501,375)
    d = (9,375)

    if show_guides:
        cv2.circle(img, a, 2, (0,0,255), -1)
        cv2.circle(img, b, 2, (0,255,0), -1)
        cv2.circle(img, c, 2, (0,0,255), -1)
        cv2.circle(img, d, 2, (0,255,0), -1)
    #Unity ratio 5x30
    #New image ratio 75x450
    l = 256-60
    r = 256+60
    u = 30
    b = 500-120
    newTopLeft = (l, u)
    newTopRight = (r, u)
    newBottomLeft = (l, d)
    newBottomRight = (r, d)

    #pts1 = np.float32([a, b, c, d])
    pts1 = np.float32([(178,261), (330,261), (484,289), (18,289)])
    #pts2 = np.float32([newTopLeft, newTopRight, newBottomRight, newBottomLeft])
    pts2 = np.float32([(l,u), (r,u), (r,b), (l,b)])
    #matrix = cv2.getPerspectiveTransform(pts1, pts2)
    #np.save(folder_path + "unityCameraInverseMatrix", matrix)

    matrix = np.load(folder_path + "unityCameraInverseMatrix.npy")
    return matrix


matrix = GetCameraMatrix(load_from_file=False)
birds_eye = cv2.warpPerspective(img, matrix, (512,512))

img_a = cv2.copyMakeBorder(img,10,10,10,5,cv2.BORDER_CONSTANT)
img_b = cv2.copyMakeBorder(birds_eye,10,10,5,10,cv2.BORDER_CONSTANT)

img_combine = np.hstack((img_a, img_b))

cv2.imshow('Inverse Perspective Example',img_combine)
cv2.imwrite(folder_path + "InversePerspectiveEg.png", img_combine)
cv2.waitKey(0)
cv2.destroyAllWindows()