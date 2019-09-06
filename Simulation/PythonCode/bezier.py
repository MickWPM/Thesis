import numpy as np
import cv2

def create_base_img(height=128,width=128):
    return 255*np.ones((height,width,3), np.uint8)

def add_points_visual(image, point_list, radius=7, colour=(255,0,0), write_point_text=False, offsets=[], offset=(0,0)):
    i = 0
    for point in point_list:
        cv2.circle(image,point, radius, colour, -1)
        if write_point_text:
            if len(offsets) > i:
                offset=offsets[i]
            point_name = 'p'+str(i)
            if i == 1:
                point_name = 'pc'
            if i == 3:
                point_name = 'p1'
            write_text(image, (point[0]-offset[0], point[1]-offset[1]), point_name, fontScale=0.5, lineType=1)
            i += 1

def get_p1_from_pc(p0,pc,p2,t=0.5, return_int=True):
    x = (pc[0] - (1-t)*(1-t)*p0[0] - p2[0]*t*t)/(2*t*(1-t))
    y = (pc[1] - (1-t)*(1-t)*p0[1] - p2[1]*t*t)/(2*t*(1-t))
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
    t_range = 1000
    for t in range(0, t_range):
        tt = t/t_range
        point = bezier_quadratic(tt, p0, p1, p2)
        cv2.circle(img,point, 3, (0,0,0), -1)


def write_text(img, bottomLeftCornerOfText, text, font= cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, fontColor = (0,0,0), lineType = 2):
    cv2.putText(img,text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)


def create_t_demo():
    IM_HEIGHT = 512
    IM_WIDTH = 512

    frame_delay = 30
    t_ticks = 100
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (IM_HEIGHT, IM_WIDTH))

    for tt in range(t_ticks,t_ticks*2):
        t = tt/(t_ticks*3)
        im = create_base_img(height=IM_HEIGHT, width=IM_WIDTH)
        point_offsets = []
        point_offsets.append((10,-20))
        point_offsets.append((-10,20))
        point_offsets.append((10,-20))
        points = []
        points.append((64*4,100*4))
        points.append((64*4,64*4))
        points.append((20*4,64*4))

        pc = points[1]
        p1 = get_p1_from_pc(points[0], pc, points[2], t=t)
        points.append(p1)
        add_points_visual(im, points, write_point_text=True, offset=(10,-20), offsets=point_offsets)

        draw_bezier(im, points[0], p1, points[2])
        write_text(im, (10,30), ('t : '+str(round(t, 2))))
        cv2.imshow("Image", im)
        cv2.waitKey(frame_delay)
        out.write(im)
        

    for tt in range(t_ticks,t_ticks*2):
        t = 1-tt/(t_ticks*3)
        im = create_base_img(height=IM_HEIGHT, width=IM_WIDTH)
        point_offsets = []
        point_offsets.append((10,-20))
        point_offsets.append((-10,20))
        point_offsets.append((10,-20))
        points = []
        points.append((64*4,100*4))
        points.append((64*4,64*4))
        points.append((20*4,64*4))

        pc = points[1]
        p1 = get_p1_from_pc(points[0], pc, points[2], t=t)
        points.append(p1)
        add_points_visual(im, points, write_point_text=True, offset=(10,-20), offsets=point_offsets)

        draw_bezier(im, points[0], p1, points[2])
        write_text(im, (10,30), ('t : '+str(round(t, 2))))
        cv2.imshow("Image", im)
        cv2.waitKey(frame_delay)
        out.write(im)

    out.release()
    cv2.destroyAllWindows()

def create_demo():
    IM_HEIGHT = 512
    IM_WIDTH = 512
    im = create_base_img(height=IM_HEIGHT, width=IM_WIDTH)
    point_offsets = []
    point_offsets.append((10,-20))
    point_offsets.append((-10,20))
    point_offsets.append((10,-20))
    points = []
    points.append((64*4,100*4))
    points.append((64*4,64*4))
    points.append((20*4,64*4))

    pc = points[1]
    p1 = get_p1_from_pc(points[0], pc, points[2])
    points.append(p1)
    add_points_visual(im, points, write_point_text=True, offset=(10,-20), offsets=point_offsets)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (IM_HEIGHT,IM_WIDTH))

    aa_range = 100
    aa_delay = 30
    for aa in range(0,aa_range):
        a = 1-aa/aa_range
        p_mid = (int(((1-a)*p1[0]+a*pc[0])), int(((1-a)*p1[1]+a*pc[1])))
        im_a = im.copy()
        draw_bezier(im_a, points[0], p_mid, points[2])
        write_text(im_a, (10,30), ('Central point (pc) bais : '+str(round(a, 2))))
        cv2.imshow("Image", im_a)
        cv2.waitKey(aa_delay)
        out.write(im_a)
        
    for aa in range(0,aa_range):
        a = aa/aa_range
        p_mid = (int(((1-a)*p1[0]+a*pc[0])), int(((1-a)*p1[1]+a*pc[1])))
        im_a = im.copy()
        draw_bezier(im_a, points[0], p_mid, points[2])
        write_text(im_a, (10,30), ('Central point (pc) bais : '+str(round(a, 2))))
        cv2.imshow("Image", im_a)
        cv2.waitKey(aa_delay)
        out.write(im_a)

    out.release()
    cv2.destroyAllWindows()

def show_ideal():
    IM_HEIGHT = 512
    IM_WIDTH = 512
    im = create_base_img(height=IM_HEIGHT, width=IM_WIDTH)
    point_offsets = []
    point_offsets.append((10,-20))
    point_offsets.append((-10,20))
    point_offsets.append((10,-20))
    points = []
    points.append((64*4,100*4))
    points.append((64*4,64*4))
    points.append((20*4,64*4))

    pc = points[1]
    p1 = get_p1_from_pc(points[0], pc, points[2])
    points.append(p1)
    add_points_visual(im, points, write_point_text=True, offset=(10,-20), offsets=point_offsets)

    a=0.6
    p_mid = (int(((1-a)*p1[0]+a*pc[0])), int(((1-a)*p1[1]+a*pc[1])))
    draw_bezier(im, points[0], p_mid, points[2])
    
    cv2.imshow("Image", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__": 
    print("Bezier demo being saved")
    create_t_demo()