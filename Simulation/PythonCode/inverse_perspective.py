import cv2
import numpy as np

folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/Output/Images/'
im_path = 'PerspectiveTest.png'
img = cv2.imread(im_path)

a = (142,184)
b= (384,184)
c = (53,378)
d = (484,378)

#cv2.circle(img, a, 2, (0,0,255), -1)
#cv2.circle(img, b, 2, (0,255,0), -1)
#cv2.circle(img, c, 2, (0,0,255), -1)
#cv2.circle(img, d, 2, (0,255,0), -1)
print(img.shape)
pts1 = np.float32([a,b,c,d])
e = 512/4
pts2 = np.float32([ [e,e], [512-e,e], [e,512-e], [512-e,512-e] ])
matrix = cv2.getPerspectiveTransform(pts1, pts2)

birds_eye = cv2.warpPerspective(img, matrix, (512,512))

#cv2.imshow('Original',img)
#cv2.imshow('Inverse Perspective',birds_eye)
img_a = cv2.copyMakeBorder(img,10,10,10,5,cv2.BORDER_CONSTANT)
img_b = cv2.copyMakeBorder(birds_eye,10,10,5,10,cv2.BORDER_CONSTANT)

img_combine = np.hstack((img_a, img_b))
cv2.imshow('Inverse Perspective Example',img_combine)
cv2.imwrite(folder_path + "InversePerspectiveEg.png", img_combine)
cv2.waitKey(0)
cv2.destroyAllWindows()