"""
Uses ZMQ to establish server for Unity process to communicate.
Base detail from: http://zguide.zeromq.org/py:hwserver

This is set up to recieve a series of images from the Unity process
but can be extended as needed

Binds to tcp://*:5555
"""


import zmq
import numpy as np
import cv2

IMAGE_SAVE_PATH = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/Output/Images/'
VIDEO_SAVE_FULLPATH = 'D:/GitRepos/Uni/Thesis/Simulation/PythonCode/Output/Videos/unity_output.avi'
DIMENSION = 512 #Dimensions of images to be recieved from Unity
VID_FPS = 20
VID_SECONDS = 20

#ZMQ server initialisation
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Listening")

images_to_save = VID_FPS*VID_SECONDS
imgNum = 0
images = []
while imgNum < images_to_save:
    #  Wait for next request from client
    message = socket.recv()
    #message will be a  2D array of 4 element vectors (ABGR or ARGB format) that has been flattened

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

    if imgNum < images_to_save:
        socket.send(b"Ack")
    else:
        print(img)
        socket.send(b"END")
        break

print("Server communication complete")

#Saving output to images and video
DIMS = (images[0].shape[0], images[0].shape[1])
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(VIDEO_SAVE_FULLPATH, fourcc, VID_FPS, DIMS, True)

for i in range(0, imgNum):
    path = IMAGE_SAVE_PATH 
    num = str(i)
	#To keep images auto sorted in order, we need to add leading zeroes
	#This works for up to 9999 images 
    if i < 10:
        num = "00" + str(i)
    elif i < 100:
        num = "0" + str(i)
    name = path + 'img_' + num + '.png'
    print("saving " + name)

    vid_frame = images[i]
    cv2.imwrite(name, vid_frame)
    out.write(vid_frame)

out.release()
print("Video and Image saving complete")
