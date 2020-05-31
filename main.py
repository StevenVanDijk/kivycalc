from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix import button

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
        if self.lastOperator == '+': calculated = self.memory + self.result
        elif self.lastOperator == '-': calculated = self.memory - self.result
        elif self.lastOperator == '*': calculated = self.memory * self.result
        elif self.lastOperator == '/': calculated = self.memory / self.result

        self.clear()
        self.result = calculated

    def clear(self):
        self.memory = 0.0
        self.result = 0.0
        self.lastOperator = ''

    def build(self):
        totalLayout = BoxLayout(orientation='vertical')
        resultLayout = BoxLayout(orientation='horizontal')
        self.memoryLabel = Label(text='memory', size_hint=(0.4, 0.4), pos_hint={'top': 0.4})
        self.resultLabel = Label(text='result')
        resultLayout.add_widget(self.memoryLabel)
        resultLayout.add_widget(self.resultLabel)        
        totalLayout.add_widget(resultLayout)

        buttons = [
            { '7': lambda: self.enter(7.0), '8': lambda: self.enter(8.0), '9': lambda: self.enter(9.0), '/': lambda: self.op('/') },
            { '4': lambda: self.enter(4.0), '5': lambda: self.enter(5.0), '6': lambda: self.enter(6.0), '*': lambda: self.op('*') },
            { '1': lambda: self.enter(1.0), '2': lambda: self.enter(2.0), '3': lambda: self.enter(3.0), '-': lambda: self.op('-') },
            { '.': None, '0': lambda: self.enter(0.0), 'C': lambda: self.clear(), '+': lambda: self.op('+') },
            { '=': lambda: self.equals() }
        ]
        self.addButtons(totalLayout, buttons)

        return totalLayout

    def on_press_button(self):
        print('You pressed the bumba!')

if __name__ == '__main__':
    app = MainApp()
    app.run()