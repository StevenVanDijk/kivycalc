from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainApp(App):
    memoryLabel: None
    resultLabel: None
    memory = 0.0
    result = 0.0
    lastOperator = ''

    def addButtons(self, widget, buttons):
        for rowButtons in buttons:
            boxLay = BoxLayout(orientation='horizontal')
            for button in rowButtons.keys():
                newButton = Button(text=button)
                def generate_func(executor):
                    return lambda instance: self.wrapper(executor) 
                newButton.bind(on_press=generate_func(rowButtons[button]))
                boxLay.add_widget(newButton)
            widget.add_widget(boxLay)

    def wrapper(self, execute):
        execute()
        self.memoryLabel.text = str(self.memory)
        self.resultLabel.text = str(self.result)

    def enter(self, num):
        self.result = self.result * 10 + num

    def op(self, operator):
        self.memory = self.result
        self.result = 0.0
        self.lastOperator = operator

    def equals(self):
        plus = self.memory + self.result
        minus = self.memory - self.result
        times = self.memory * self.result
        division = self.memory / self.result
        if self.lastOperator == '+': calculated = plus
        elif self.lastOperator == '-': calculated = minus
        elif self.lastOperator == '*': calculated = times
        elif self.lastOperator == '/': calculated = division

        self.clear()
        self.result = calculated

    def clear(self):
        self.memory = 0.0
        self.result = 0.0
        self.lastOperator = ''

    def build(self):
        def btn(numb):
            return lambda: self.enter(numb)
            

        def spc(crc):
            return lambda: self.op(crc)

        totalLayout = BoxLayout(orientation='vertical')
        resultLayout = BoxLayout(orientation='horizontal')
        self.memoryLabel = Label(text='memory', size_hint=(0.4, 0.4), pos_hint={'top': 0.4})
        self.resultLabel = Label(text='result')
        resultLayout.add_widget(self.memoryLabel)
        resultLayout.add_widget(self.resultLabel)        
        totalLayout.add_widget(resultLayout)

        buttons = [
            { '7': btn(7.0), '8': btn(8.0), '9': btn(9.0), '/': spc('/') },
            { '4': btn(4.0), '5': btn(5.0), '6': btn(6.0), '*': spc('*') },
            { '1': btn(1.0), '2': btn(2.0), '3': btn(3.0), '-': spc('-') },
            { '.': None, '0': btn(0.0), 'C': lambda: self.clear(), '+': spc('+') },
            { '=': lambda: self.equals() }
        ]
        self.addButtons(totalLayout, buttons)

        return totalLayout

    def on_press_button(self):
        print('You pressed the bumba!')

if __name__ == '__main__':
    app = MainApp()
    app.run()