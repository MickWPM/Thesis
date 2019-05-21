import cv2
import numpy as np
folder_path = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/Output/'

img_a = cv2.imread('img_99.png')
img_b = cv2.imread('img_100.png')

img_a = cv2.copyMakeBorder(img_a,10,10,10,5,cv2.BORDER_CONSTANT)
img_b = cv2.copyMakeBorder(img_b,10,10,5,10,cv2.BORDER_CONSTANT)
img_combine = np.hstack((img_a, img_b))

cv2.imwrite(folder_path + "combined_image.png", img_combine)