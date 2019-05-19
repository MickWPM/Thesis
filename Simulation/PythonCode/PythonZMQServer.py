#   Hello World server in Python
#   Binds REP socket to tcp://*:5555

#import time
import zmq
import numpy as np
#from PIL import Image
#import struct
import cv2

DIMENSION = 512

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Listening")

images_to_save = 100
imgNum = 0
images = []
while imgNum < images_to_save:
    #  Wait for next request from client
    message = socket.recv()
    #message will be a  2D array of 4 element vectors (ABGR or ARGB format) that has been flattened


###OLD CODE START
    #img_bytes = np.array(message)
    #int_message = np.zeros((DIMENSION, DIMENSION, 3), dtype=np.uint8)

    #We need to reshape the array from a 1D array into a 3D array of colour vectors
    #We also want to drop the alpha value as it is redundant information
    #The 1D array consists of the colour vector as 4 individual byte elements
    #So we need to reshape the array AND drop the first element of each colour 
#    for x in range(0,DIMENSION):
#        for y in range(0,DIMENSION):
#                i = 4*(y*DIMENSION + x) #Index of Alpha value - ABGR or ARGB format
#                arr = np.array( [ message[i+2], message[i+1], message[i] ] )
#                int_message[DIMENSION-1-y,x] = arr
###OLD CODE END

    #Force message to byte array and cast as np array
    img_bytes = np.array(bytearray(message))
    #reshape from 1D to 3D array, x, y and colour
    arr2 = np.reshape(img_bytes, (DIMENSION, DIMENSION, 4))
    #Vertical part of image needs to be flipped (differing coord systems)
    int_message = np.flip(arr2[:, :, :-1], 0)
    #Also set the data to RGB format (instead of BGR)
    img = np.flip(int_message, 2)
    
    images.append(img)
    imgNum += 1
    print("imgNum = " + str(imgNum))

    if imgNum < images_to_save:
        socket.send(b"Ack")
    else:
        #socket.send_string("END")
        print(img)
        socket.send(b"END")
        break

print("DONE")

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('D:/GitRepos/Uni/Thesis/Simulation/Output/unity_calibration_output.avi', 
                        fourcc, 20, (DIMENSION, DIMENSION), True)

for i in range(0, imgNum):
    name = 'img_' + str(i) + '.png'
    #images[i].save(name)
    cv2.imwrite(name, images[i])
    print("saving " + name)

    if i < imgNum / 2:
        vid_frame = images[i]
    else:
        edges = cv2.Canny(images[i], 150, 180)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        vid_frame = edges

    out.write(vid_frame)

out.release()
print("end")
