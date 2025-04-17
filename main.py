from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

class MainScr(Screen):
    def __init__(self, name="", **kwargs):
        super().__init__(name=name, **kwargs)

        hl = BoxLayout(orientation="horizontal", spacing=10, padding=10)
        vl = BoxLayout(orientation="vertical", spacing=10, padding=10)

        text1 = Label(text=f"{user_input}") 
        txt_index = Label(text="Ваш індекс Руф’є:")
        txt_workheart = Label(text="Працездатність серця:")
        txt_nodata = Label(text="Немає даних для такого віку")

        txt_res = []
        txt_res.append("Низька. Терміново зверніться до лікаря!")
        txt_res.append("Задовільна. Зверніться до лікаря!")
        txt_res.append("Середня. Можливо, варто додатково обстежитись у лікаря.")
        txt_res.append("Вище середнього")
        txt_res.append("Висока")

        vl.add_widget(text1)
        vl.add_widget(txt_index)
        vl.add_widget(txt_workheart)
        hl.add_widget(vl)
        self.add_widget(hl)

        def ruffier_index(P1, P2, P3):
            return (4 * (P1 + P2 + P3) - 200) / 10

        def neud_level(age):
            norm_age = (min(age, 15) - 7) // 2
            result = 21 - norm_age * 1.5
            return result

        def ruffier_result(r_index, level):
            if r_index >= level:
                return 0
            level = level - 4
            if r_index >= level:
                return 1
            level = level - 5
            if r_index >= level:
                return 2
            level = level - 5.5
            if r_index >= level:
                return 3
            return 4

        def test(P1, P2, P3, age):
            if age < 7:
                return (txt_index + "0", txt_nodata)
            else:
                ruff_index = ruffier_index(P1, P2, P3)
                result = txt_res[ruffier_result(ruff_index, neud_level(age))]
                res = txt_index + str(ruff_index) + "\n" + txt_workheart + result
                return res

class MyApp(App):
    def build(self):
        app = ScreenManager()
        app.add_widget(MainScr())
        return app
MyApp().run()