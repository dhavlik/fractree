import sys
from PIL import Image, ImageDraw
from math import *
imgx = 1920
imgy = 1080
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)






def rad_to_deg(angle_rad):
    angle_deg = angle_rad*180/pi
    return angle_deg

def deg_to_rad(angle_deg):
    angle_rad = (angle_deg * pi)/180.0
    return angle_rad

def get_angle(line):
    x1, y1 = line[0]
    x2, y2 = line[1]
    deltax = x2 - x1
    deltay = y2 - y1
    angle_rad = atan2(deltay,deltax)
    return angle_rad

def get_length(line):
    x1, y1 = line[0]
    x2, y2 = line[1]
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    return sqrt(dx**2 + dy**2)

def line_rotated_end(distance, start_x, start_y, theta):
    theta = theta - 90
    deltax = distance * cos(deg_to_rad(theta))
    deltay = distance * sin(deg_to_rad(theta))
    x1 = start_x + deltax
    y1 = start_y + deltay
    return x1, y1

def point_on_line(distance, line):
    theta = rad_to_deg(get_angle(line)) + 90
    x0, y0 = line[0]
    return line_rotated_end(distance, x0, y0, theta)




#draw.line((line_start, line_rotated_end(100, line_start[0], line_start[1], 125)), width=5)
#draw.line((line_start, line_rotated_end(100, line_start[0], line_start[1], -125)), width=5)



def tree(startline, depth, angle):
    gval = int(255*depth/7.0)
    col = (0, gval, 0)
    inc_mul = 0.71
    depth = depth - 1
    if depth == 0:
        return
    len_startline = get_length(startline)
    inc = len_startline / 0.7 - (len_startline * 0.3)
    deg = rad_to_deg(get_angle(startline))+90
    while True:
        inc = inc * inc_mul
        if inc < 1:# len_startline:
            break
        startp = point_on_line(len_startline - inc, startline)
        endright = line_rotated_end(inc*inc_mul, startp[0], startp[1], deg+angle)
        endleft = line_rotated_end(inc*inc_mul, startp[0], startp[1], deg-angle)
        draw.line((startp, endright), fill=col)
        tree((startp, endright), depth, angle)
        draw.line((startp, endleft), fill=col)
        tree((startp, endleft), depth, angle)

       # import pdb; pdb.set_trace()

frames = 1250.0


def make_video():
    for x in range(int(frames)):
        endend = imgy - (imgy * (x/frames)) - 50
        line_start = (imgx/2.0,imgy - 50)
        line_end =  (imgx/2.0,endend)
        startline = (line_start, line_end)
        draw.line(startline, fill=(0, 255, 0))
        a = 120 * (x/frames)
        print '%s of %s' % (x, frames)
        tree(startline, 6, a)
        image.save('foo_%s.png' % x)
        image.close()
        image = Image.new("RGB", (imgx, imgy))
        draw = ImageDraw.Draw(image)



line_start = (imgx/2.0,imgy - 50)
line_end =  (imgx/2.0,50)
startline = (line_start, line_end)
draw.line(startline, fill=(0, 255, 0))
tree(startline, 6, 70)
image.show()


sys.exit(0)
