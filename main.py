from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from enum import Enum

class State(Enum):
    EnteringIntegers = 1
    EnteringFloats = 2
    CalculatingIntegers = 3
    CalculatingFloats = 4
    Calculated = 5

class MainApp(App):
    state: State = State.EnteringIntegers
    memoryLabel: None
    resultLabel: None
    memory = 0.0
    result = 0.0
    lastOperator = ''
    isDone = False
    decimal = 0 

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
        if (self.state == State.Calculated):
            self.state = State.EnteringIntegers
            self.result = 0.0
        if (self.state == State.EnteringIntegers or self.state == State.CalculatingIntegers):
            if self.isDone:
                self.result = 0.0
                self.isDone = False
            else:
                self.result = self.result * 10 + num
        elif (self.state == State.EnteringFloats or self.state == State.CalculatingFloats):
            self.result = self.result + num * 1 / 10**self.decimal
            self.decimal += 1
   

    def op(self, operator):
        if (self.state == State.EnteringIntegers): 
            self.state = State.CalculatingIntegers
        if (self.state == State.EnteringFloats): 
            self.state = State.CalculatingFloats
        self.memory = self.result
        self.result = 0.0
        self.lastOperator = operator
     

    def equals(self):
        if (self.state == State.CalculatingIntegers or self.state == State.CalculatingFloats):
            self.state = State.Calculated
            plus = self.memory + self.result
            minus = self.memory - self.result
            times = self.memory * self.result
            division = self.memory / self.result
            if self.lastOperator == '+': 
                calculated_numb = plus
            elif self.lastOperator == '-': 
                calculated_numb = minus
            elif self.lastOperator == '*': 
                calculated_numb = times
            elif self.lastOperator == '/': 
                calculated_numb = division      

            self.isDone = True
            self.clear()
            self.result = calculated_numb
            self.memory = self.result
        

    def clear(self):
        self.memory = 0.0
        self.result = 0.0
        self.lastOperator = ''
        self.decimal = 1
        self.state = State.CalculatingIntegers

    
    def puntje(self):
        if self.state == State.EnteringIntegers:
            self.state = State.EnteringFloats
            self.decimal  

        else:
            self.state = State.EnteringFloats
            self.decimal = 1
    
    def build(self):
        
        def btn(numb):
            self.result = self.memory
            self.result = 0.0
            return lambda: self.enter(numb)
            

        def spc(crc):
            self.isNext = True
            self.result = self.memory
            self.result = 0.0
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
            { '.': lambda: self.puntje(), '0': btn(0.0), 'C': lambda: self.clear(), '+': spc('+') },
            { '=': lambda: self.equals() }
        ]
        self.addButtons(totalLayout, buttons)

        return totalLayout

if __name__ == '__main__':
    app = MainApp()
    app.run()