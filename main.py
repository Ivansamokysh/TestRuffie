from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.core.window import Window

from ErrorWindow import ErrorWindow

Window.size = (1280, 720)


class ScrButton(Button):
    def __init__(self, screen, direction, goal, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal

    def on_press(self):
        self.screen.manager.transition.direction = self.direction 
        self.screen.manager.current = self.goal

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        instructions = (
            "Ця програма дозволить вам за допомогою тесту Руф'є провести первинну діагностику вашого здоров'я.\n\n"
            "Проба Руф'є являє собою навантажувальний комплекс, призначений для оцінки працездатності серця при фізичному навантаженні.\n"
            "У випробуваного визначають частоту пульсу за 15 секунд.\n"
            "Потім протягом 45 секунд випробуваний виконує 30 присідань.\n\n"
            "Після закінчення навантаження пульс підраховується знову: число пульсацій за перші 15 секунд, 30 секунд відпочинку, "
            "число пульсацій за останні 15 секунд."
        )

        instruction_label = Label(text=instructions, color=(1, 1, 1, 1), halign='left', valign='top', font_size='18sp')
        instruction_label.bind(size=instruction_label.setter('text_size'))
        layout.add_widget(instruction_label)

        self.name_input = TextInput(hint_text='Введіть імʼя', multiline=False, size_hint=(1, None), height=40)
        layout.add_widget(self.name_input)

        self.age_input = TextInput(hint_text='Введіть вік', multiline=False, input_filter='int', size_hint=(1, None), height=40)
        layout.add_widget(self.age_input)

        start_button = Button(text="Почати", size_hint=(1, 0.3), background_color=(0.3, 0.3, 0.3, 1))
        start_button.bind(on_press=self.save_data_and_start)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def save_data_and_start(self, instance):
        app = App.get_running_app()
        app.us_name = self.name_input.text
        try:
            app.age = int(self.age_input.text)
        except:
            app.age = 0
        self.manager.transition.direction = 'up'
        self.manager.current = 'second_screen'

        if not self.name_input.text or not self.age_input.text:  #ErrorWindow з'являється на екрані тоді коли користувач не ввів дані
            error_text1 = "Треба ввести ім'я та вік"
            ErrorWindow(title=error_text1).open()
        else:
            self.manager.transition.direction = 'up'
            self.manager.current = 'second_screen'

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=10)
        layout.add_widget(Label(
            text="Виміряйте пульс за 15 секунд.",
            font_size='18sp',
            size_hint_y=None,
            height=40,
            halign='center',
            valign='middle'
        ))
        layout.add_widget(Label(
            text="Результат запишіть у відповідне поле.",
            font_size='18sp',
            size_hint_y=None,
            height=40
        ))
        
        input_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        input_layout.add_widget(Label(
            text="Введіть результат:",
            font_size='18sp',
            size_hint_x=None,
            width=150
        ))
        self.text_input = TextInput(
            text="",
            multiline=False,
            font_size='18sp',
            size_hint_x=0.7
        )
        input_layout.add_widget(self.text_input)
        layout.add_widget(input_layout)
        
        continue_button = ScrButton(self, "up", "third_screen", text="Продовжити", font_size='18sp', size_hint=(1, None), height=80, background_color=(0.3, 0.3, 0.3, 1))
        layout.add_widget(continue_button)
        self.add_widget(layout)

        if not self.text_input.text:    #ErrorWindow з'являється на екрані тоді коли користувач не ввів дані
            error_text2 = "Треба ввести результат"
            ErrorWindow(title=error_text2).open()
        else:
            self.manager.transition.direction = 'up'
            self.manager.current = 'third_screen'
        
class ThirdScreen(Screen):
    def __init__(self, name="third_screen"):
        super().__init__(name=name)
        label = Label(text="Виконай 30 присідань за 45 секунд", font_size='18sp', size_hint=(1, 0.5), halign='center', valign='middle')
        vl = BoxLayout(orientation="vertical", spacing=10, padding=10)
        hl = BoxLayout(orientation="horizontal", spacing=10, padding=10)

        button_1 = ScrButton(self, "up", "fourth_screen", text="Продовжити", size_hint=(0.5, 0.2), background_color=(0.3, 0.3, 0.3, 1))
        hl.add_widget(button_1)

        vl.add_widget(label)
        vl.add_widget(hl)
        self.add_widget(vl)

class FourthScreen(Screen):
    def __init__(self, name="fourth_screen", **kwargs):
        super().__init__(name=name, **kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        instructions = (
            "Протягом хвилини заміряйте пульс двічі:\n"
            "за перші 15 секунд хвилини, потім за останні 15 секунд.\n"
            "Результати запишіть у відповідні поля."
        )
        instruction_label = Label(
            text=instructions,
            halign='center',
            valign='middle',
            text_size=(Window.width - 100, None),
            font_size='18sp'
        )
        layout.add_widget(instruction_label)

        self.result_input = TextInput(
            hint_text='Результат',
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(self.result_input)

        self.result_after_input = TextInput(
            hint_text='Результат після відпочинку',
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(self.result_after_input)

        finish_button = Button(
            text='Завершити',
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.3, 0.3, 1)
        )
        finish_button.bind(on_press=self.finish)
        layout.add_widget(finish_button)

        self.add_widget(layout)

    def finish(self, instance):
        app = App.get_running_app()
        app.P1 = int(self.result_input.text) if self.result_input.text.isdigit() else 0
        app.P2 = int(self.result_after_input.text) if self.result_after_input.text.isdigit() else 0
        self.manager.transition.direction = 'up'
        self.manager.current = 'fifth_screen'

        if not self.result_input or not self.result_after_input:  #ErrorWindow з'являється на екрані тоді коли користувач не ввів дані
            error_text3 = "Треба ввести результат до відпочинку та після"
            ErrorWindow(title=error_text3).open()
        else:
            self.manager.transition.direction = 'up'
            self.manager.current = 'fifth_screen'

class FifthScreen(Screen):
    def __init__(self, name="fifth_screen", **kwargs):
        super().__init__(name=name, **kwargs)
        self.layout = BoxLayout(orientation="vertical", spacing=5, padding=10)
        self.add_widget(self.layout)

    def on_enter(self):
        self.layout.clear_widgets()
        app = App.get_running_app()

        txt_res = [
            "Низька. Терміново зверніться до лікаря!",
            "Задовільна. Зверніться до лікаря!",
            "Середня. Можливо, варто додатково обстежитись у лікаря.",
            "Вище середнього",
            "Висока"
        ]
        txt_nodata = "Немає даних для такого віку"

        def ruffier_index(P1, P2, P3):
            return (4 * (P1 + P2 + P3) - 200) / 10

        def neud_level(age):
            norm_age = (min(age, 15) - 7) // 2
            return 21 - norm_age * 1.5

        def ruffier_result(r_index, level):
            if r_index >= level:
                return 0
            level -= 4
            if r_index >= level:
                return 1
            level -= 5
            if r_index >= level:
                return 2
            level -= 5.5
            if r_index >= level:
                return 3
            return 4

        def test(P1, P2, P3, age):
            if age < 7:
                return ("0", txt_nodata)
            else:
                r_index = ruffier_index(P1, P2, P3)
                result = txt_res[ruffier_result(r_index, neud_level(age))]
                return (str(round(r_index, 1)), result)

        P1 = app.P1
        P2 = app.P2
        P3 = app.P3
        age = app.age
        us_name = app.us_name

        index, test_result = test(P1, P2, P3, age)

        text1 = Label(text=f"Ім'я: {us_name}, Вік: {age}", font_size='24sp')
        txt_index = Label(text=f"Ваш індекс Руф’є: {index}", font_size='24sp')
        txt_workheart = Label(text=f"Працездатність серця: {test_result}", font_size='24sp')

        self.layout.add_widget(text1)
        self.layout.add_widget(txt_index)
        self.layout.add_widget(txt_workheart)

class RuffierApp(App):
    def build(self):
        self.age = 0
        self.us_name = "Unknown"
        self.P1 = 0
        self.P2 = 0
        self.P3 = 0

        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first_screen'))
        sm.add_widget(SecondScreen(name='second_screen'))
        sm.add_widget(ThirdScreen(name='third_screen'))
        sm.add_widget(FourthScreen(name='fourth_screen'))
        sm.add_widget(FifthScreen(name='fifth_screen'))
        return sm
print
if __name__ == '__main__':
    RuffierApp().run()
