from typing import Callable

from manim import *

class BasketballFly(Scene):#渲染代码：manim -pqm quadratic_func.py BasketballFly
    def construct(self):
        basketball = ImageMobject("Image/basketball.png")#导入篮球
        basketball.move_to([-8,-4,0])#移动至左下角
        self.add(basketball)#将篮球加入画面

        #篮球从空中划过
        def Fly(obj,dt):
            x = basketball.get_x() + 8
            y = basketball.get_y() + 4
            x += dt*10#x随时间变化
            y = -0.0625*x**2 + x#篮球移动逻辑的二次函数
            basketball.move_to([-8 + x,-4 + y,0])#移动篮球

            if y<=-4:#落下后删除对象
                basketball.remove()

        trace = TracedPath(basketball.get_center)
        self.add(trace)
        basketball.add_updater(Fly)

        self.wait(3)