import cv2
import numpy as np

def LoadCameraMatrix(folder_path):
    matrix = np.load(folder_path + "CameraInverseMatrix.npy")
    return matrix


def CreateCameraMatrix(folder_path, img):
    show_guides = False

    topR = (312,48)#topR
    topL= (233,46)#topL
    botR = (495,155)#botR 314,155
    botL = (69,155)#botL  232,155

#500x174
    topR = (500,0)#topR
    topL = (0,0)#topL
    botL = (500,174)#botR 314,155
    botR = (0,174)#botL  232,155

    
    topR = (300,40)#topR
    topL = (240,40)#topL
    botL = (500,174)#botR 314,155
    botR = (0,174)#botL  232,155


    if show_guides:
        s = 5
        cv2.circle(img, topR, s, (0,0,255), -1)
        cv2.circle(img, topL, s, (0,255,0), -1)
        cv2.circle(img, botR, s, (0,0,255), -1)
        cv2.circle(img, botL, s, (0,255,0), -1)
        
        
    newTopLeft = (250-int(250/2),0)
    newTopRight = (250+int(250/2),0)
    newBottomLeft = (250-int(250/2),174)
    newBottomRight = (250+int(250/2),174)

    
    newTopRight = (250-int(250/4),0)
    newTopLeft = (250+int(250/4),0)
    newBottomRight = (250-int(250/4),174)
    newBottomLeft = (250+int(250/4),174)
    

    pts1 = np.float32([topR, topL, botR, botL])
    #pts1 = np.float32([(178,261), (330,261), (484,289), (18,289)])
    pts2 = np.float32([newTopLeft, newTopRight, newBottomRight, newBottomLeft])
    #pts2 = np.float32([(l,u), (r,u), (r,b), (l,b)])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    np.save(folder_path + "CameraInverseMatrix", matrix)

    matrix = np.load(folder_path + "CameraInverseMatrix.npy")
    return matrix

def GetBirdsEye(matrix, img, resolution = (512,512), return_combo_img = False):
    birds_eye = cv2.warpPerspective(img, matrix, resolution)
    img_a = cv2.copyMakeBorder(img,10,10,10,5,cv2.BORDER_CONSTANT)
    img_b = cv2.copyMakeBorder(birds_eye,10,10,5,10,cv2.BORDER_CONSTANT)
    img_combine = np.hstack((img_a, img_b))
    # RETURN COMBINE
    if return_combo_img:
        return img_combine
    return birds_eye



def main():
    print("IN WRONG CLASS")
    folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/'
    im_path = 'InversePerspective/car_dashcam.jpg'
    #im_path = 'InversePerspective/unityCamCalibration.png'
    
    img = cv2.imread(im_path)

    #matrix = CreateCameraMatrix(folder_path, img)
    matrix = LoadCameraMatrix(folder_path)
    img_combine = GetBirdsEye(matrix, img, (img.shape[1], img.shape[0]), return_combo_img= True)

    cv2.imshow('Inverse Perspective Example',img_combine)
    cv2.imwrite(folder_path + "InversePerspectiveEg.png", img_combine)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__": main()

