
import random
import os
from math import cos, sin, radians

import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.animation import Animation
from kivy.core.text import Label as CoreLabel
from kivy.graphics import (
    Color, Ellipse, Line, Triangle,
    Rectangle, PushMatrix, PopMatrix, Rotate
)
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


# =====================================
# تنظیمات ظاهری
# =====================================

GREEN = (0.08, 0.48, 0.25, 1)
DARK_GREEN = (0.04, 0.30, 0.15, 1)
YELLOW = (1, 0.82, 0.12, 1)
WHITE = (1, 1, 1, 1)
RED = (0.95, 0.08, 0.08, 1)
BLUE = (0.05, 0.35, 1, 1)

FONT_PATH = (
    r"C:\Windows\Fonts\tahoma.ttf"
    if os.path.exists(r"C:\Windows\Fonts\tahoma.ttf")
    else "Roboto"
)


def fa(text):
    """نمایش صحیح متن فارسی"""
    return get_display(
        arabic_reshaper.reshape(str(text))
    )


def make_button(text, font_size=22):
    return Button(
        text=fa(text),
        font_size=font_size,
        font_name=FONT_PATH,
        bold=True,
        color=(0.08, 0.20, 0.10, 1),
        background_normal="",
        background_color=YELLOW,
        size_hint=(1, None),
        height=dp(55)
    )


def make_label(text, font_size=22, color=WHITE):
    return Label(
        text=fa(text),
        font_size=font_size,
        font_name=FONT_PATH,
        bold=True,
        color=color
    )


# =====================================
# صفحه اصلی
# =====================================

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(25)
        )

        with self.canvas.before:
            Color(*GREEN)
            self.bg = Rectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        title = make_label(
            "جرئت یا حقیقت",
            42,
            YELLOW
        )

        start = make_button("شروع بازی", 25)
        start.bind(on_release=self.start_game)

        layout.add_widget(Widget())
        layout.add_widget(title)
        layout.add_widget(start)
        layout.add_widget(Widget())

        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def start_game(self, *args):
        self.manager.current = "players"


# =====================================
# صفحه انتخاب تعداد بازیکنان
# =====================================

class PlayerScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(20)
        )

        with self.canvas.before:
            Color(*GREEN)
            self.bg = Rectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        title = make_label(
            "چند نفر بازیکن هستید؟",
            30,
            YELLOW
        )
        title.size_hint = (1, 0.25)

        layout.add_widget(title)

        grid = GridLayout(
            cols=3,
            spacing=dp(12),
            padding=dp(10)
        )

        for number in range(2, 10):

            btn = make_button(str(number), 28)

            btn.bind(
                on_release=lambda instance, n=number:
                self.select_players(n)
            )

            grid.add_widget(btn)

        layout.add_widget(grid)

        home = make_button("بازگشت به خانه", 18)
        home.bind(on_release=self.go_home)

        layout.add_widget(home)

        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def select_players(self, number):
        game = self.manager.get_screen("game")
        game.set_players(number)
        self.manager.current = "game"

    def go_home(self, *args):
        self.manager.current = "main"


# =====================================
# گردونه با دو عقربه
# =====================================

class WheelWidget(Widget):

    ask_angle = NumericProperty(0)
    answer_angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_count = 2

        self.ask_rotation = None
        self.answer_rotation = None

        self.bind(
            pos=self.draw_wheel,
            size=self.draw_wheel
        )

        self.bind(
            ask_angle=self.update_pointers,
            answer_angle=self.update_pointers
        )

    def set_players(self, count):
        self.player_count = count
        self.ask_angle = 0
        self.answer_angle = 0
        self.draw_wheel()

    def update_pointers(self, *args):

        if self.ask_rotation:
            self.ask_rotation.angle = self.ask_angle

        if self.answer_rotation:
            self.answer_rotation.angle = self.answer_angle

    def draw_wheel(self, *args):

        self.canvas.clear()

        cx, cy = self.center

        radius = min(
            self.width,
            self.height
        ) * 0.38

        with self.canvas:

            # دایره اصلی
            Color(*YELLOW)

            Ellipse(
                pos=(cx - radius, cy - radius),
                size=(radius * 2, radius * 2)
            )

            Color(*DARK_GREEN)

            Line(
                circle=(cx, cy, radius),
                width=dp(4)
            )

            # شماره بازیکنان
            for i in range(self.player_count):

                a = radians(
                    90 - i * 360 / self.player_count
                )

                px = cx + radius * 0.72 * cos(a)
                py = cy + radius * 0.72 * sin(a)

                Color(*DARK_GREEN)

                Ellipse(
                    pos=(px - dp(20), py - dp(20)),
                    size=(dp(40), dp(40))
                )

                label = CoreLabel(
                    text=str(i + 1),
                    font_size=dp(18),
                    bold=True,
                    color=WHITE
                )

                label.refresh()

                texture = label.texture

                Color(*WHITE)

                Rectangle(
                    texture=texture,
                    pos=(
                        px - texture.width / 2,
                        py - texture.height / 2
                    ),
                    size=texture.size
                )

            # عقربه قرمز: سؤال کننده
            PushMatrix()

            self.ask_rotation = Rotate(
                angle=self.ask_angle,
                origin=(cx, cy)
            )

            Color(*RED)

            Triangle(
                points=[
                    cx - dp(11), cy,
                    cx + dp(11), cy,
                    cx, cy + radius * 0.90
                ]
            )

            PopMatrix()

            # عقربه آبی: پاسخ دهنده
            PushMatrix()

            self.answer_rotation = Rotate(
                angle=self.answer_angle,
                origin=(cx, cy)
            )

            Color(*BLUE)

            Triangle(
                points=[
                    cx - dp(7), cy,
                    cx + dp(7), cy,
                    cx, cy + radius * 0.78
                ]
            )

            PopMatrix()

            # مرکز گردونه
            Color(*DARK_GREEN)

            Ellipse(
                pos=(cx - dp(13), cy - dp(13)),
                size=(dp(26), dp(26))
            )

        self.update_pointers()


# =====================================
# صفحه بازی
# =====================================

class GameScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_count = 2
        self.is_spinning = False

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        with self.canvas.before:
            Color(*GREEN)

            self.bg = Rectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # نوار بالایی
        top = BoxLayout(
            size_hint=(1, 0.10)
        )

        home = make_button("خانه", 16)
        home.bind(on_release=self.go_home)

        top.add_widget(home)
        layout.add_widget(top)

        # وضعیت بازی
        self.status = make_label(
            "برای شروع، گردونه را بچرخانید!",
            21,
            WHITE
        )
        self.status.size_hint = (1, 0.14)

        layout.add_widget(self.status)

        # گردونه
        self.wheel = WheelWidget(
            size_hint=(1, 0.65)
        )

        layout.add_widget(self.wheel)

        # راهنمای رنگ عقربه ها
        legend = BoxLayout(
            size_hint=(1, 0.08),
            spacing=dp(5)
        )

        legend.add_widget(
            make_label("قرمز: سؤال کننده", 14, RED)
        )

        legend.add_widget(
            make_label("آبی: پاسخ دهنده", 14, BLUE)
        )

        layout.add_widget(legend)

        # دکمه چرخاندن
        self.spin_button = make_button(
            "بچرخان!",
            25
        )

        self.spin_button.bind(
            on_release=self.spin
        )

        layout.add_widget(self.spin_button)

        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def set_players(self, count):

        Animation.cancel_all(self.wheel)

        self.player_count = count
        self.wheel.set_players(count)

        self.is_spinning = False
        self.spin_button.disabled = False

        self.status.text = fa(
            f"{count} بازیکن آماده هستند!"
        )

    # =================================
    # چرخش دو عقربه
    # =================================

    def spin(self, *args):

        if self.is_spinning:
            return

        self.is_spinning = True
        self.spin_button.disabled = True

        self.status.text = fa(
            "هر دو عقربه در حال چرخش هستند..."
        )

        # انتخاب دو بازیکن متفاوت
        questioner, answerer = random.sample(
            range(self.player_count),
            2
        )

        step = 360 / self.player_count

        # زاویه نهایی عقربه قرمز
        ask_target = (
            self.wheel.ask_angle
            + 360 * 5
            + (
                (-questioner * step - self.wheel.ask_angle)
                % 360
            )
        )

        # زاویه نهایی عقربه آبی
        answer_target = (
            self.wheel.answer_angle
            + 360 * 5
            + (
                (-answerer * step - self.wheel.answer_angle)
                % 360
            )
        )

        animation = Animation(
            ask_angle=ask_target,
            answer_angle=answer_target,
            duration=4,
            transition="out_quad"
        )

        animation.bind(
            on_complete=lambda *args:
            self.finish_spin(questioner, answerer)
        )

        animation.start(self.wheel)

    # =================================
    # نتیجه
    # =================================

    def finish_spin(self, questioner, answerer):

        self.status.text = fa(
            f"بازیکن {questioner + 1} سؤال می‌پرسد، "
            f"بازیکن {answerer + 1} پاسخ می‌دهد!"
        )

        self.spin_button.disabled = False
        self.is_spinning = False

    # =================================
    # بازگشت به خانه
    # =================================

    def go_home(self, *args):

        Animation.cancel_all(
            self.wheel,
            "ask_angle"
        )

        Animation.cancel_all(
            self.wheel,
            "answer_angle"
        )

        self.is_spinning = False
        self.spin_button.disabled = False

        self.wheel.ask_angle = 0
        self.wheel.answer_angle = 0

        self.manager.current = "main"


# =====================================
# اجرای برنامه
# =====================================

class TruthOrDareApp(App):

    def build(self):

        manager = ScreenManager()

        manager.add_widget(
            MainScreen(name="main")
        )

        manager.add_widget(
            PlayerScreen(name="players")
        )

        manager.add_widget(
            GameScreen(name="game")
        )

        return manager


if __name__ == "__main__":
    TruthOrDareApp().run()
