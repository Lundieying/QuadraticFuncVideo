from manim import *

# config.frame_width = 100   # 默认是 14
# config.frame_height = 50  # 默认是 8

#manim -pqm quadratic_func.py BasketballFly
class BasketballFly(Scene):
    def construct(self):
        basketball = ImageMobject("Image/basketball.png")#导入篮球
        basketball.move_to([-8,-4,0])#移动至左下角
        self.add(basketball)#将篮球加入画面
        trace = TracedPath(basketball.get_center, dissipating_time=None)
        self.add(trace)

        copy_trace = None
        is_remove = False
        x = ValueTracker(0)
        y = ValueTracker(0)
        def fly(obj, dt):
            speed = 10 #自己填
            x.set_value(x.get_value()+dt*speed)
            y.set_value(-0.0625*x.get_value()**2 + x.get_value())
            obj.move_to([x.get_value()-8, y.get_value()-4, 0])
            if obj.get_y() < -4:
                nonlocal is_remove
                is_remove = True

        def remove_time(obj):
            nonlocal  is_remove,copy_trace,trace
            if is_remove and copy_trace != None:
                basketball.clear_updaters()
                trace.clear_updaters()
                copy_trace = trace.copy()
                self.remove(trace)
                self.add(copy_trace)
                trace = copy_trace
                self.remove(basketball)
                self.clear()

        self.add_updater(remove_time)
        basketball.add_updater(fly)

        self.play(Wait(run_time=10, stop_condition=lambda: copy_trace != None))
        self.wait()

        flicker = VMobject().set_stroke(color=YELLOW, width=5)
        start = ValueTracker(0)
        lenth = ValueTracker(0.01)
        def flick(obj):
            obj.pointwise_become_partial(trace, start.get_value(), start.get_value()+lenth.get_value())

        self.add(flicker)
        # self.add(copy_trace)
        flicker.add_updater(flick)
        self.play(start.animate.set_value(1), run_time=3)

        text1 = MathTex("Math", font_size=60, color=BLUE)
        text2 = MathTex("X", font_size=60)
        text3 = MathTex("physics", font_size=60, color=PINK)
        text1.move_to([-1.5,-2,0])
        text2.move_to([0,-2,0])
        text3.move_to([1.5,-2,0])
        self.play(Write(text1))
        self.play(Write(text2))
        self.play(Write(text3))

#manim -pqm quadratic_func.py ShowTitle
class ShowTitle(Scene):
    def construct(self):
        title = Text("二次函数中的物理")
        self.play(Write(title))
        self.wait()

#manim -pqm quadratic_func.py ShowFunc
class ShowFunc(Scene):
    def construct(self):
        func_text = MathTex("y=ax^2+bx+c")
        self.play(Write(func_text))
        self.wait()
        self.play(func_text.animate.shift(LEFT * 1.5))
        self.wait()
        explain = MathTex("(a\\neq0)")
        explain.set_x(1.5)
        self.play(Write(explain))
        self.wait()
        self.play(func_text.animate.shift(UP * 2), explain.animate.shift((UP * 2)))
        arrow = Arrow(start=UP * 1, end=DOWN * 1, stroke_width=4)
        self.play(Create(arrow))
        easy_func = MathTex("y=ax^2")
        easy_func.set_y(-2)
        self.play(Write(easy_func))
        self.wait()

#manim -pqm quadratic_func.py EasyFunc
class EasyFunc(Scene):
    def construct(self):
        #建立坐标系
        axis = NumberPlane(
            #[x,y,z]，x表示最小范围，y最大范围，z单位长度
            x_range=[-4,4,0.5],
            y_range=[-3,3,0.5],
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "stroke_opacity": 1
            },
            # axis_config={"include_numbers": True}
        )
        axis.set_y(0.5)
        self.play(Create(axis), run_time=3)
        unit_len=Text("单位长度:0.5", font_size=15)
        unit_len.set_y(-3.75)
        self.play(Write(unit_len))
        self.wait()
        self.play(axis.animate.shift(RIGHT * 2), unit_len.animate.shift(RIGHT * 2))
        self.wait()

        #文字说明
        func = MathTex("y=x^2")
        func.move_to([-4,3,0])
        self.play(Write(func))
        parameter = MathTex("a=0")
        parameter.move_to([-4,2,0])
        a = ValueTracker(0)
        def show_value(obj):
            obj = MathTex("a="+str(a.get_value()))
        self.play(Write(parameter))
        parameter.add_updater(show_value)
        self.play(a.animate.set_value(10), run_time=1)
        self.play(a.animate.set_value(-10), run_time=2)
        self.play(a.animate.set_value(0), run_time=1)