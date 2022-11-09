import random 
from math import sin, cos, pi, log 
from tkinter import * 


CANVAS_WIDTH = 640  # 画布的宽 
CANVAS_HEIGHT = 480  # 画布的高
CANVAS_CENTER_X = CANVAS_WIDTH / 2 # 画布中心的X轴坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2 # 画布中心的Y轴坐标 
IMAGE_ENLARGE = 8 # 放大比例


def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
     """ 
     “爱心函数生成器” 
     :param shrink_ratio: 放大比例 
     :param t: 参数 
     :return: 坐标 
     """ 
     x = 16 * (sin(t) ** 3)
     y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)) 
     
     x *= shrink_ratio 
     y *= shrink_ratio 

     x += CANVAS_CENTER_X 
     y += CANVAS_CENTER_Y 
     
     return int(x), int(y) 


def scatter_inside(x, y, beta=0.15): 
    """ 随机内部扩散
     :param x: 原x 
     :param y: 原y 
     :param beta: 强度 :return: 新坐标 
     """ 
    ratiox = - beta * log(random.random()) 
    ratioy = - beta * log(random.random()) 

    dx = ratiox * (x - CANVAS_CENTER_X) 
    dy = ratioy * (y - CANVAS_CENTER_Y) 

    return x - dx, y - dy


def shrink(x, y, ratio): 
    """ 抖动
     :param x: 原x 
     :param y: 原y 
     :param ratio: 比例
     :return: 新坐标 """ 
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6) # 这个参数... 
    dx = ratio * force * (x - CANVAS_CENTER_X) 
    dy = ratio * force * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy 

class Heart:
    def __init__(self):
        self._points=set()
        self._extra_points=set()
        self._inside=set()
        self.all_points={}
        self.build(2000)

    def build(self,number):
        for _ in range(number):
            t=random.uniform(0, 2*pi)
            x,y=heart_function(t)
            self._points.add((int(x),int(y)))

        for xx,yy in list(self._points):
            for _ in range(3):
                x,y=scatter_inside(xx, yy,0.05)   
                self._extra_points.add((x,y))

        point_list= list(self._points)
        for _ in range(4000):
                x,y=random.choice(point_list)
                x,y=scatter_inside(x, y)   
                self._inside.add((int(x),int(y)))
 
    def calc_position(self,x, y, ratio): # 调整缩放比例
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520) 
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1) 
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1) 
        return x - dx, y - dy
    
    def calc(self,frame):
        calc_position=self.calc_position
        ratio=10*sin(frame /10*pi)
        all_points=[]
        
        for x, y in self._points:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size)) 


        for x, y in self._extra_points: 
            x, y =calc_position(x, y, ratio)
            size = random.randint(1, 2) 
            all_points.append((x, y, size)) 

        for x, y in self._inside: 
            x, y =calc_position(x, y, ratio)
            size = random.randint(1, 2) 
            all_points.append((x, y, size))

        self.all_points[frame]=all_points


    def render(self,canvas,frame):
        for x,y, size in self.all_points[frame % 20]:
            canvas.create_rectangle(x,y,x+size,y+size,width=0,fill="#ff7171")

def draw(root:Tk,canvas:Canvas,heart:Heart,frame=0):
    canvas.delete('all')
    heart.render(canvas,frame)
    root.after(160,draw,root,canvas,heart,frame+1)


def scatter_inside(x, y, beta=0.15): 
    """ 随机内部扩散
     :param x: 原x 
     :param y: 原y 
     :param beta: 强度 :return: 新坐标 
     """ 
    ratio_x = - beta * log(random.random()) 
    ratio_y = - beta * log(random.random()) 

    dx = ratio_x * (x - CANVAS_CENTER_X) 
    dy = ratio_y * (y - CANVAS_CENTER_Y) 

    return x - dx, y - dy

def calc_position(self,x, y, ratio): # 调整缩放比例
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520) 
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1) 
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1) 
        return x - dx, y - dy


if __name__ == "__main__": 
    root = Tk() 
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack() 
    heart = Heart()
    for frame in range(20):
        heart.calc(frame)
    draw(root,canvas,heart) 
    root.mainloop()  
