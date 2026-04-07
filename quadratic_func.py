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
        title = Text("从抛体运动看二次函数的物理意义")
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
        #建立坐标系
        asix = NumberPlane(
            x_range=[-14,14,0.25],
            y_range=[-100,100,0.25]
        )
        self.play(Create(asix), run_time=5)

        #准备物体
        basketball = ImageMobject("Image/basketball.png")
        time_dot = Dot()
        projection_dot = Dot()

        #准备介绍文字
        arrow = Arrow(start=UP*0.1+RIGHT*0.1, end=UP*2+RIGHT*2, stroke_width=5)
        introduc_text = None

        #引入篮球
        basketball.move_to([0,9,0])
        basketball.scale(0.5)
        self.add(basketball)
        self.play(basketball.animate.shift(DOWN*9), run_time=5)
        self.wait()
        #介绍篮球
        introduc_text = Text("受重力影响的物体", font_size=40).next_to(arrow, UP+RIGHT)
        self.play(Create(arrow))
        self.play(Write(introduc_text))
        self.wait(3)
        #篮球退场
        self.play(FadeOut(arrow,introduc_text))
        self.play(basketball.animate.shift(UP*9), run_time=5)
        self.remove(basketball)
        basketball.move_to([0,0,0])
        self.wait()

        #引入时间点
        self.play(FadeIn(time_dot))
        self.play(time_dot.animate.shift(RIGHT*14), run_time=1)
        self.play(time_dot.animate.shift(RIGHT*-28), run_time=2)
        self.play(time_dot.animate.shift(RIGHT*14), run_time=1)
        self.wait()
        #介绍时间点
        introduc_text = Text("物体运动的时间", font_size=40).next_to(arrow, UP+RIGHT)
        self.play(Create(arrow))
        self.play(Write(introduc_text))
        self.wait(3)
        #时间点退场
        self.play(FadeOut(arrow, introduc_text))
        self.play(FadeOut(time_dot))
        self.wait()

        #准备说明文字
        text_center = Dot().next_to(basketball,LEFT*13+UP*7)#所有说明文字的空壳，不用显示
        func = MathTex("y=ax^2").next_to(text_center, UP)
        a_text = MathTex("a=").next_to(text_center, LEFT*0.5)
        a = ValueTracker(1)
        a_show = DecimalNumber(a.get_value()).next_to(a_text, RIGHT)
        x_text = MathTex("x=").next_to(text_center, LEFT*0.5 + DOWN)
        x = ValueTracker(0)
        x_show = DecimalNumber(x.get_value()).next_to(x_text, RIGHT)
        def bind(mob, dt):
            #绑定数值
            a_show.set_value(a.get_value())
            x.set_value(time_dot.get_x())
            x_show.set_value(x.get_value())
            #绑定位置
            text_center.next_to(basketball,LEFT*13 + UP*7)
            func.next_to(text_center, UP)
            a_text.next_to(text_center, LEFT*0.5)
            a_show.next_to(a_text, RIGHT)
            x_text.next_to(text_center, LEFT*0.5 + DOWN)
            x_show.next_to(x_text, RIGHT)
        #写文字动画
        for i in [func,a_text,a_show,x_text,x_show]:
            self.play(Write(i))

        #准备画函数图像
        def camera_with(mob, dt):#将相机绑定在篮球上
            self.camera.frame.move_to(basketball)
        def projection(mob, dt):
            projection_dot.move_to(basketball.get_center()+time_dot.get_center())
        p_or_n = 1
        def move(mob, dt):
            time_dot.shift(p_or_n*RIGHT*dt)
        def of_func(mob,dt):
            basketball.move_to([0,a.get_value()*time_dot.get_x()**2,0])
        trace = TracedPath(projection_dot.get_center, dissipating_time=None)
        basketball.move_to([0,0,0])

        #引入动画
        self.play(FadeIn(basketball, time_dot, projection_dot))
        self.add(trace)
        #装载函数开始绘制
        for i in [move,of_func,projection,camera_with,bind]:
            func.add_updater(i)
        asix.add_updater(lambda mob,dt: asix.set_y(time_dot.get_y()))
        self.wait(14)
        #回到初始
        func.clear_updaters()
        self.wait()
        for i in [of_func, projection, camera_with, bind]:
            func.add_updater(i)
        self.play(time_dot.animate.set_x(0), run_time=1)
        self.wait()

        #停止篮球比喻
        #隐藏
        func.clear_updaters()
        self.play(FadeOut(basketball, time_dot, projection_dot, trace, x_text, x_show))
        #绘制函数
        func.add_updater(bind)
        graph = always_redraw(lambda : asix.plot(lambda i: a.get_value()*i**2))
        self.play(Create(graph))
        #正数
        self.play(a.animate.set_value(2.5), run_time=1)
        self.wait()
        self.play(a.animate.set_value(5), run_time=1)
        self.wait()
        self.play(a.animate.set_value(100), run_time=5, rate_func=linear)
        self.wait()
        #负数
        self.play(a.animate.set_value(-2.5), run_time=1)
        self.wait()
        self.play(a.animate.set_value(-5), run_time=1)
        self.wait()
        self.play(a.animate.set_value(-100), run_time=5, rate_func=linear)
        self.wait()
        #0
        self.play(a.animate.set_value(0), run_time=1)
        self.wait()

#manim -pqm quadratic_func.py MiddleFunc
class MiddleFunc(Scene):
    config.frame_width = 14  # 默认是 14
    config.frame_height = 8  # 默认是 8
    def construct(self):
        # 建立坐标系
        axis = NumberPlane(
            # [x,y,z]，x表示最小范围，y最大范围，z单位长度
            x_range=[-4, 4, 0.5],
            y_range=[-3, 3, 0.5],
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "stroke_opacity": 1
            }
        )
        self.play(Create(axis), run_time=3)
        unit_len = Text("单位长度:0.5", font_size=15)
        unit_len.set_y(-3.75)
        self.play(Write(unit_len))
        self.wait()
        self.play(axis.animate.shift(RIGHT * 2), unit_len.animate.shift(RIGHT * 2))
        self.wait()

        # 文字说明
        func = MathTex("y=ax^2+bx")
        func.move_to([-5, 3, 0])
        self.play(Write(func))
        a_text = MathTex("a=")
        a_text.next_to([-6, 2, 0])
        a = ValueTracker(-1)
        a_show = DecimalNumber(a.get_value()).next_to(a_text, RIGHT)
        b_text = MathTex("b=")
        b_text.next_to([-6, 1, 0])
        b = ValueTracker(0)
        b_show = DecimalNumber(b.get_value()).next_to(b_text, RIGHT)

        def show_value(obj):
            if obj == a_show:
                a_show.set_value(a.get_value())
            if obj == b_show:
                b_show.set_value(b.get_value())

        self.play(Write(a_text))
        self.play(Write(a_show))
        a_show.add_updater(show_value)
        self.play(Write(b_text))
        self.play(Write(b_show))
        b_show.add_updater(show_value)

        # 画函数图像
        def draw():
            return axis.plot(lambda x: a.get_value()*x**2 + b.get_value()*x)

        graph = always_redraw(draw)
        self.play(Create(graph))
        self.play(b.animate.set_value(2), run_time=1)
        self.wait()
        self.play(b.animate.set_value(3.5), run_time=1)
        self.wait()
        self.play(b.animate.set_value(-1.45), run_time=1)
        self.wait(3)

#manim -pqm quadratic_func.py BasketballMiddleFunc
class BasketballMiddleFunc(MovingCameraScene):
    config.frame_width = 28  # 默认是 14
    config.frame_height = 16  # 默认是 8

    def construct(self):
        # 建立坐标系
        asix = NumberPlane(
            x_range=[-14, 14, 0.25],
            y_range=[-100, 100, 0.25]
        )
        self.play(Create(asix), run_time=5)

        # 准备物体
        basketball = ImageMobject("Image/basketball.png")
        basketball.scale(0.5)
        time_dot = Dot()
        projection_dot = Dot()

        # 准备说明文字
        text_center = Dot().next_to(basketball, LEFT * 13 + UP * 7)  # 所有说明文字的空壳，不用显示
        func = MathTex("y=ax^2+bx").next_to(text_center, UP)
        a_text = MathTex("a=").next_to(text_center, LEFT * 0.5)
        a = ValueTracker(-1)
        a_show = DecimalNumber(a.get_value()).next_to(a_text, RIGHT)
        b_text = MathTex("b=").next_to(text_center, LEFT * 0.5 + DOWN)
        b = ValueTracker(5)
        b_show = DecimalNumber(a.get_value()).next_to(b_text, RIGHT)
        x_text = MathTex("x=").next_to(text_center, LEFT * 0.5 + DOWN*2.75)
        x = ValueTracker(0)
        x_show = DecimalNumber(x.get_value()).next_to(x_text, RIGHT)

        def bind(mob, dt):
            # 绑定数值
            a_show.set_value(a.get_value())
            b_show.set_value(b.get_value())
            x.set_value(time_dot.get_x())
            x_show.set_value(x.get_value())
            # 绑定位置
            text_center.next_to(basketball, LEFT * 13 + UP * 7)
            func.next_to(text_center, UP)
            a_text.next_to(text_center, LEFT * 0.5)
            a_show.next_to(a_text, RIGHT)
            b_text.next_to(text_center, LEFT * 0.5 + DOWN)
            b_show.next_to(b_text, RIGHT)
            x_text.next_to(text_center, LEFT * 0.5 + DOWN*2.75)
            x_show.next_to(x_text, RIGHT)

        # 写文字动画
        for i in [func, a_text, a_show,b_text, b_show, x_text, x_show]:
            self.play(Write(i))

        # 准备画函数图像
        def camera_with(mob, dt):  # 将相机绑定在篮球上
            self.camera.frame.move_to(basketball)

        def projection(mob, dt):
            projection_dot.move_to(basketball.get_center() + time_dot.get_center())

        p_or_n = 1

        def move(mob, dt):
            time_dot.shift(p_or_n * RIGHT * dt)

        def of_func(mob, dt):
            basketball.move_to([0, a.get_value()*time_dot.get_x()**2 + b.get_value()*time_dot.get_x(), 0])

        trace = TracedPath(projection_dot.get_center, dissipating_time=None)
        basketball.move_to([0, 0, 0])

        # 引入动画
        self.play(FadeIn(basketball, time_dot, projection_dot))
        self.add(trace)
        self.wait()
        force = Arrow(start=UP*0, end=UP*2, stroke_width=5, stroke_color=GREEN)
        self.play(Create(force))
        # 装载函数开始绘制
        for i in [move, of_func, projection, camera_with, bind]:
            func.add_updater(i)
        asix.add_updater(lambda mob, dt: asix.set_y(time_dot.get_y()))
        self.play(FadeOut(force))
        self.wait(6)
        # 回到初始
        func.clear_updaters()
        self.wait()
        for i in [of_func, projection, camera_with, bind]:
            func.add_updater(i)
        self.play(time_dot.animate.set_x(0), run_time=1)
        self.wait()
        self.play(FadeOut(trace))
        trace = TracedPath(projection_dot.get_center, dissipating_time=None)
        self.add(trace)
        self.wait()
        #b改为负
        func.clear_updaters()
        force = Arrow(start=UP*0, end=DOWN*2, stroke_width=5, stroke_color=GREEN)
        self.play(b.animate.set_value(-5), Create(force), run_time=1)
        self.wait()
        for i in [move, of_func, projection, camera_with, bind]:
            func.add_updater(i)
        asix.add_updater(lambda mob, dt: asix.set_y(time_dot.get_y()))
        self.play(FadeOut(force))
        self.wait(6)
        # 回到初始
        func.clear_updaters()
        self.wait()
        for i in [of_func, projection, camera_with, bind]:
            func.add_updater(i)
        self.play(time_dot.animate.set_x(0), run_time=1)
        self.wait()

        # 停止篮球比喻
        # 隐藏
        func.clear_updaters()
        self.play(FadeOut(basketball, time_dot, projection_dot, trace, x_text, x_show))
        # 绘制函数
        func.add_updater(bind)
        graph = always_redraw(lambda: asix.plot(lambda i: a.get_value()*i**2+b.get_value()*i))
        self.play(Create(graph))
        # 正数
        self.play(b.animate.set_value(2.5), run_time=1)
        self.wait()
        self.play(b.animate.set_value(5), run_time=1)
        self.wait()
        self.play(b.animate.set_value(100), run_time=5, rate_func=linear)
        self.wait()
        # 负数
        self.play(b.animate.set_value(-2.5), run_time=1)
        self.wait()
        self.play(b.animate.set_value(-5), run_time=1)
        self.wait()
        self.play(b.animate.set_value(-100), run_time=5, rate_func=linear)
        self.wait()
        # 0
        self.play(b.animate.set_value(0), run_time=1)
        self.wait()

#manim -pqm quadratic_func.py FullFunc
class FullFunc(Scene):
    config.frame_width = 14  # 默认是 14
    config.frame_height = 8  # 默认是 8

    def construct(self):
        # 建立坐标系
        axis = NumberPlane(
            # [x,y,z]，x表示最小范围，y最大范围，z单位长度
            x_range=[-4, 4, 0.5],
            y_range=[-3, 3, 0.5],
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "stroke_opacity": 1
            }
        )
        self.play(Create(axis), run_time=3)
        unit_len = Text("单位长度:0.5", font_size=15)
        unit_len.set_y(-3.75)
        self.play(Write(unit_len))
        self.wait()
        self.play(axis.animate.shift(RIGHT * 2), unit_len.animate.shift(RIGHT * 2))
        self.wait()

        # 文字说明
        func = MathTex("y=ax^2+bx+c")
        func.move_to([-5, 3, 0])
        self.play(Write(func))
        a_text = MathTex("a=")
        a_text.next_to([-6, 2, 0])
        a = ValueTracker(-1)
        a_show = DecimalNumber(a.get_value()).next_to(a_text, RIGHT)
        b_text = MathTex("b=")
        b_text.next_to([-6, 1, 0])
        b = ValueTracker(2)
        b_show = DecimalNumber(b.get_value()).next_to(b_text, RIGHT)
        c_text = MathTex("c=")
        c_text.next_to([-6, 0, 0])
        c = ValueTracker(0)
        c_show = DecimalNumber(b.get_value()).next_to(c_text, RIGHT)

        def show_value(obj):
            if obj == a_show:
                a_show.set_value(a.get_value())
            if obj == b_show:
                b_show.set_value(b.get_value())
            if obj == c_show:
                c_show.set_value(c.get_value())

        self.play(Write(a_text))
        self.play(Write(a_show))
        a_show.add_updater(show_value)
        self.play(Write(b_text))
        self.play(Write(b_show))
        b_show.add_updater(show_value)
        self.play(Write(c_text))
        self.play(Write(c_show))
        c_show.add_updater(show_value)

        # 画函数图像
        def draw():
            return axis.plot(lambda x:a.get_value()*x**2 + b.get_value()*x + c.get_value())

        graph = always_redraw(draw)
        self.play(Create(graph))
        self.play(c.animate.set_value(2), run_time=1)
        self.wait()
        self.play(c.animate.set_value(3.5), run_time=1)
        self.wait()
        self.play(c.animate.set_value(-1.45), run_time=1)
        self.wait(3)

#manim -pqm quadratic_func.py BasketballFullFunc
class BasketballFullFunc(Scene):
    def construct(self):
        rectangle1 = Rectangle(width=3, height=2, color=GRAY).move_to(DOWN * 1)
        rectangle2 = Rectangle(width=3, height=1, color=GRAY).next_to(rectangle1, RIGHT).shift(DOWN*0.5)
        basketball = ImageMobject("Image/basketball.png").next_to(rectangle1, UP)
        self.play(FadeIn(rectangle1, rectangle2))
        self.wait()
        self.play(FadeIn(basketball))
        arrow = CurvedArrow(
            start_point=basketball.get_center(),
            end_point=rectangle2.get_center() + UP,
            color=RED,
            angle=-PI / 2,
            stroke_width=5,
        )
        self.play(Create(arrow))
        self.wait()

#manim -pqm quadratic_func.py Summary
class Summary(Scene):
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
        arrow = Arrow(start=UP * 1, end=DOWN * 1, stroke_width=4, stroke_color=GREEN)
        self.play(Create(arrow))
        a_text = Text("a:与重力加速度有关").next_to(arrow, DOWN)
        a_text.set_color_by_t2c({"a": YELLOW})
        b_text = Text("b:与物体初速度有关").next_to(a_text, DOWN)
        b_text.set_color_by_t2c({"b": YELLOW})
        c_text = Text("c:表示物体抛出点的初始高度").next_to(b_text, DOWN)
        c_text.set_color_by_t2c({"c": YELLOW})
        for x in [a_text, b_text, c_text]:
            self.play(Write(x))
        self.wait()

#manim -pqm quadratic_func.py End
class End(Scene):
    def construct(self):
        m1 = MathTex("Math", color=BLUE)
        m2 = MathTex("X")
        m3 = MathTex("Physics", color=PINK)
        group = VGroup(m1, m2, m3).arrange(RIGHT)
        self.play(Write(group))
        self.wait()