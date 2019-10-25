"""
Simple script to generate a quadratic bezier curve mask
"""

import numpy as np
import cv2

def create_base_img(height,width):
	"""Simple base image helper function"""
    return 255*np.ones((height,width,3), np.uint8)

def bezier_quadratic(t, p0, p1, p2, return_int=True):
	"""
	Function to determine point on bezier curve given bezier data
	t: The proportion along the curve we are looking for (between 0 and 1)
	p0, p1, p2: Bezier control points
	return_int: Flag to cast the return coordinates to integers
		This is useful if they need to be converted to image coordinates for example
	Returns: Tuple coordinate of bezier curve position at t
	"""
    x = (1-t)*(1-t)*p0[0] + 2*(1-t) * t * p1[0] + t*t*p2[0]
    y = (1-t)*(1-t)*p0[1] + 2*(1-t) * t * p1[1] + t*t*p2[1]
    if return_int:
        x = int(x)
        y = int(y)
    return (x,y)

def draw_bezier(img, p0, p1, p2, colour=(0,0,0), width=3):
	"""
	Function to draw a full bezier curve to an image mask
	img: The mask image to draw to
	p0, p1, p2: Bezier control points
	colour: The colour to use. This will be white if a mask is used
		however this method is generic in that it can draw to a colour image as well
	width: Width of the curve to draw
	"""
    t_range = 1000
    for t in range(0, t_range):
        tt = t/t_range
        point = bezier_quadratic(tt, p0, p1, p2)
        cv2.circle(img,point, width, colour, -1)

def get_curve_mask(feature_point, inbound_point, outbound_point, width=3, img_dimensions=(512,512)):
	"""
	Method to get a curve mask for driving lines.
	feature_point: The pixel coordinate of the central feature point
	inbound_point: The pixel coordinate of the approach point (first point encountered along the driving line)
	outbound_point: The pixel coordinate of the final (outbound) feature point
	width: Width of bezier curve 
	img_dimensions: Dimensions of mask
	
	Returns: Binary driving line curve mask
	"""
    im_height = img_dimensions[1]
    im_width = img_dimensions[0]

	#Create blank mask and draw new bezier to it
    im = create_base_img(height=im_height, width=im_width)
    draw_bezier(im, inbound_point, feature_point, outbound_point, width=width)
	#Binary mask developed by thresholding bezier mask image
    ret,curve_mask = cv2.threshold(im,127,255,cv2.THRESH_BINARY_INV)
    return curve_mask