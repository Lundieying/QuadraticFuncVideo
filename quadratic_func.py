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
        self.play(Create(axis), run_time=3)
        unit_len=Text("单位长度:0.5", font_size=15)
        unit_len.set_y(-3.75)
        self.play(Write(unit_len))
        self.wait()
        self.play(axis.animate.shift(RIGHT * 2), unit_len.animate.shift(RIGHT * 2))
        self.wait()

        #文字说明
        func = MathTex("y=ax^2")
        func.move_to([-5,3,0])
        self.play(Write(func))
        a_text = MathTex("a=")
        a_text.next_to([-6,2,0])
        a = ValueTracker(1)
        a_show = DecimalNumber(a.get_value()).next_to(a_text, RIGHT)
        def show_value(obj):
            a_show.set_value(a.get_value())
        self.play(Write(a_text))
        self.play(Write(a_show))
        a_show.add_updater(show_value)
        #画函数图像
        def draw():
            return axis.plot(lambda x: a.get_value() * x ** 2)
        graph = always_redraw(draw)
        self.play(Create(graph))
        self.play(a.animate.set_value(10), run_time=5, rate_func=linear)
        self.play(a.animate.set_value(-10), run_time=10, rate_func=linear)
        self.play(a.animate.set_value(0), run_time=5, rate_func=linear)
        self.wait(3)

#manim -pqm quadratic_func.py BasketballEasyFunc
class BasketballEasyFunc(MovingCameraScene):
    config.frame_width = 28  # 默认是 14
    config.frame_height = 16  # 默认是 8
    def construct(self):
        axis = NumberPlane(
            x_range=[-14,14,0.25],
            y_range=[-100,100,0.25]
        )
        self.play(Create(axis), run_time=5)
        self.wait()
        basketball = ImageMobject("Image/basketball.png")
        basketball.scale(0.5)
        time_dot = Dot()
        func = MathTex("y=ax^2")
        func.add_updater(lambda: func.next_to(self.camera.frame, LEFT*13+UP*3.5))
        a_text = MathTex("a=")
        a_text.add_updater(lambda: a_text.next_to(self.camera.frame, LEFT*14+UP*2.5))
        a = ValueTracker(1)
        a_show = DecimalNumber(a.get_value()).next_to(a_text, RIGHT)
        x_text = MathTex("x=")
        x_text.add_updater(lambda: x_text.next_to(self.camera.frame,LEFT*-14+UP*1.5))
        x = ValueTracker(0)
        x_show = DecimalNumber(x.get_value()).next_to(x_text, RIGHT)
        def show_value(obj):
            if obj == a_show:
                obj.set_value(a.get_value())
            if obj == x_show:
                obj.set_value(x.get_value())
        a_show.add_updater(show_value)
        x_show.add_updater(show_value)
        self.play(FadeIn(basketball))
        self.wait()

        #引入篮球和时间点
        arrow = Arrow(start=UP*0.2 + RIGHT*0.2, end=UP*1 + RIGHT*1, stroke_width=4)
        introduc_text = Text("受重力影响的物体", font_size=40).next_to(arrow, UP * 0.5 + RIGHT * 0.5)
        self.play(Create(arrow))
        self.play(Write(introduc_text))
        self.wait()
        self.remove(arrow)
        self.remove(introduc_text)
        self.play(FadeOut(basketball))

        self.play(Create(time_dot))
        self.play(time_dot.animate.set_x(7), run_time=1)
        self.play(time_dot.animate.set_x(-7), run_time=2)
        self.play(time_dot.animate.set_x(0), run_time=1)
        self.wait()
        arrow = Arrow(start=UP * 0.1 + RIGHT * 0.1, end=UP * 1 + RIGHT * 1, stroke_width=4)
        introduc_text = Text("物体运动的时间", font_size=40).next_to(arrow, UP * 0.5 + RIGHT * 0.5)
        self.play(Create(arrow))
        self.play(Write(introduc_text))
        self.wait()
        self.remove(arrow)
        self.remove(introduc_text)
        self.play(FadeOut(time_dot))

        self.play(Write(func))
        self.play(Write(a_text))
        self.play(Write(a_show))
        self.play(Write(x_text))
        self.play(Write(x_show))
        self.wait()

        #绘制函数
        self.play(FadeIn(basketball, time_dot))
        projection_dot = Dot()
        def projection(obj):
            projection_dot.move_to(basketball.get_center() + time_dot.get_center())
        trace = TracedPath(projection_dot.get_center, dissipating_time=None)
        def move(obj, dt):
            x.set_value(x.get_value()+dt)
            time_dot.set_x(x.get_value())
            basketball.move_to([0,a.get_value()*x.get_value()**2,0])
        projection_dot.add_updater(projection)
        self.add(projection_dot)
        self.add(trace)
        projection_dot.add_updater(move)
        def move_with_camera(obj):
            self.camera.frame.move_to(obj.get_center())
        basketball.add_updater(move_with_camera)
        # def follow(obj):
        #     obj.move_to(self.camera.frame.get_y()+obj.get_center())
        # func.add_updater(follow)
        # a_text.add_updater(follow)
        # a_show.add_updater(follow)
        # x_text.add_updater(follow)
        # x_show.add_updater(follow)
        self.wait(19)