import wx
import calculator

class MainWindow(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Flipparia')
        self.calc = calculator.Calculator()
        self.panel = wx.Panel(self)

        #self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        #self.calculate_sizer = wx.BoxSizer(wx.VERTICAL)

        #self.bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        #self.utility_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.main_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel)
        self.calculate_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel)

        self.bottom_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel)
        self.utility_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel)

        profit_list = ["Delirium Orbs", "Scarabs", "Essences"]

        for item in profit_list:
            button = wx.Button(self.panel, label=item, name=item)
            button.Bind(wx.EVT_BUTTON, self.profit_calc)
            self.calculate_sizer.Add(button, 0, wx.CENTER, 0)

        max_width = 0
        max_height = 0

        for child in self.calculate_sizer.GetChildren():
            if child.GetSize().Width > max_width:
                max_width = child.GetSize().Width

            if child.GetSize().Width > max_height:
                max_height = child.GetSize().Height
        
        for child in self.calculate_sizer.GetChildren():
            child.SetMinSize(max_width, max_height)

        refresh_button = wx.Button(self.panel, label="Refresh", name="Refresh")
        refresh_button.Bind(wx.EVT_BUTTON, self.refresh_data)

        image = wx.Image("resources/images/refresh.png")
        size = refresh_button.GetDefaultSize().Height
        image = image.Scale(size - 5, size - 5, wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(image)    
        refresh_button.SetBitmap(bmp)
        
        back_button = wx.Button(self.panel, label="Back", name="Back")
        back_button.Bind(wx.EVT_BUTTON, self.return_to_menu)

        self.main_sizer.Add(self.calculate_sizer, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 5)
        self.main_sizer.AddStretchSpacer()
        self.main_sizer.Add(self.bottom_sizer, 0 , wx.EXPAND)

        self.bottom_sizer.Add(self.utility_sizer, 0, wx.EXPAND, 5)
        self.utility_sizer.Add(back_button, 0, wx.EXPAND, 5)
        self.utility_sizer.AddStretchSpacer()
        self.utility_sizer.Add(refresh_button, 0, wx.EXPAND, 5)

        self.panel.SetSizerAndFit(self.main_sizer)
        self.Show()

    def profit_calc(self, event):
        #data = self.calc.profit_calc(event.GetEventObject().Name)
        self.hide_buttons()

        posX = 20
        """
        for targets, profit in data.items():
            posY = 20
            wx.StaticText(self.panel, label=targets, pos=(posX, posY))
            posY = posY + 100
            for item in profit:
                wx.StaticText(self.panel, label=str(item), pos=(posX, posY))
                posY = posY + 100
            
            posX = posX + 300
        """
            
    def hide_buttons(self):
        self.calculate_sizer.ShowItems(False)

    def show_buttons(self):
        self.calculate_sizer.ShowItems(True)

    def refresh_data(self, event):
        self.calc.refresh_prices()

    def return_to_menu(self, event):
        self.show_buttons()
        

if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()
