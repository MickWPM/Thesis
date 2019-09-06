import numpy as np
import cv2

def create_base_img(height=128,width=128):
    return 255*np.ones((height,width,3), np.uint8)

def add_points_visual(image, point_list, radius=5, colour=(255,0,0)):
    for point in point_list:
        cv2.circle(image,point, radius, colour, -1)

def get_p1_from_pc(p0,pc,p2,t=0.5, return_int=True):
    x = (pc[0] - p0[0]*t*t - p2[0]*t*t)/t
    y = (pc[1] - p0[1]*t*t - p2[1]*t*t)/t
    if return_int:
        x = int(x)
        y = int(y)
    return (x,y)

def bezier_quadratic(t, p0, p1, p2, return_int=True):
    x = (1-t)*(1-t)*p0[0] + 2*(1-t) * t * p1[0] + t*t*p2[0]
    y = (1-t)*(1-t)*p0[1] + 2*(1-t) * t * p1[1] + t*t*p2[1]
    if return_int:
        x = int(x)
        y = int(y)
    return (x,y)

def draw_bezier(img, p0, p1, p2):
    for t in range(0, 100):
        tt = t/100
        point = bezier_quadratic(tt, p0, p1, p2)
        cv2.circle(img,point, 1, (0,0,0), -1)

im = create_base_img()
points = []
points.append((64,100))
points.append((64,64))
points.append((20,64))
add_points_visual(im, points)

pc = points[1]
p1 = get_p1_from_pc(points[0], pc, points[2])

for aa in range(0,10):
    a = aa/10
    p_mid = (int(((1-a)*p1[0]+a*pc[0])), int(((1-a)*p1[1]+a*pc[1])))
    im_a = im.copy()
    draw_bezier(im_a, points[0], p1, points[2])
    cv2.imshow("Image", im_a)
    cv2.waitKey(0)
    cv2.destroyAllWindows()