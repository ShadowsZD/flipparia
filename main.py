import wx
import calculator

class MainWindow(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Flipparia')
        self.calc = calculator.Calculator()
        self.panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        profit_list = ["Delirium Orbs", "Scarabs", "Essences"]

        for item in profit_list:
            button = wx.Button(self.panel, label=item, name=item)
            button.Bind(wx.EVT_BUTTON, self.profit_calc)
            my_sizer.Add(button, 0, wx.ALL | wx.CENTER, 5)

        refresh_button = wx.Button(self.panel, label="Refresh", name="Refresh")
        refresh_button.Bind(wx.EVT_BUTTON, self.refresh_data)
        my_sizer.Add(refresh_button, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(my_sizer)        
        self.Show()

    def profit_calc(self, event):
        data = self.calc.profit_calc(event.GetEventObject().Name)

        posY = 20
        posX = 20
        for targets, profit in data.items():
            wx.StaticText(self.panel, label=targets, pos=(posX, 20))
            #change from list to dict to separate better each scenario
            wx.StaticText(self.panel, label=str(profit), pos=(posX, 50))
            posX = posX + 300

    def hide_buttons(self):
        for child in self.panel.GetChildren():
            child.Hide()

    def show_buttons(self):
        for child in self.panel.GetChildren():
            child.Show()

    def refresh_data(self, event):
        self.calc.refresh_prices()
        

if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()
