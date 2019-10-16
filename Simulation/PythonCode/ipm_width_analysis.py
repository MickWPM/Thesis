import cv2
import numpy as np

im_path = r"D:\GitRepos\Uni\Thesis\Simulation\PythonCode\Analysis\road_surface.png"
#im_path = r"D:\GitRepos\Uni\Thesis\Simulation\PythonCode\Analysis\road_surface2.png"
base_img = cv2.imread(im_path, 0)

print(base_img.shape)

xmid = int(base_img.shape[1]/2)
yspan = int(base_img.shape[0]/3)

correct = []
guess = []
correctInv = []
for i in range(0,3):
    ystart = i * yspan
    yend = ystart + yspan
    imC = base_img[ystart:yend, :xmid-1]
    imG = base_img[ystart:yend, xmid+1:base_img.shape[1]]
    
    #ret, imC = np.divide( cv2.threshold(imC,127,255,cv2.THRESH_BINARY), 255 )
    #ret, imG = np.divide( cv2.threshold(imG,127,255,cv2.THRESH_BINARY), 255 )
    #ret, imCinv = np.divide( cv2.threshold(imC,127,255,cv2.THRESH_BINARY_INV), 255 )

    ret, imC = cv2.threshold(imC,127,255,cv2.THRESH_BINARY)
    ret, imG = cv2.threshold(imG,127,255,cv2.THRESH_BINARY)
    ret, imCinv = cv2.threshold(imC,127,255,cv2.THRESH_BINARY_INV)

    correct.append(imC)
    guess.append(imG)
    correctInv.append(imCinv)

print(correct[0].shape)
print(guess[0].shape)

maskedCorrect = []
maskedIncorrect = []


for i in range(0,3):
    corr = cv2.bitwise_and(correct[i], guess[i])
    incorr = cv2.bitwise_and(correctInv[i], guess[i])
    maskedCorrect.append(corr)
    maskedIncorrect.append(incorr)


correctSum = []
for m in correct:
    correctSum.append(float(np.sum(m)))

correctPct = []
incorrectPct = []

for i in range(0,3):
    divisor = correctSum[i]
    divisorincorrect = np.sum(correctInv[i])
    mcorrectsum = np.sum(maskedCorrect[i])
    mincorrectsum = np.sum(maskedIncorrect[i])
    print("i = ", i)
    # cv2.imshow("Image", maskedCorrect[i])
    # print("mcorrectsum=",mcorrectsum)
    # cv2.waitKey(0)
    # cv2.imshow("Image", maskedIncorrect[i])
    # print("mcorrectsum=",mincorrectsum)
    # cv2.waitKey(0)
    corr = 100*mcorrectsum / divisor
    inccorr =  100*mincorrectsum / divisorincorrect
    print(corr, "% correct, ", inccorr, "% incorrect")
    correctPct.append(corr)
    incorrectPct.append(incorr)



cv2.destroyAllWindows()