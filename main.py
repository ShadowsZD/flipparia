import wx
import calculator
import json

class MainWindow(wx.Frame):    
    def __init__(self, mode):
        super().__init__(parent=None, title='Flipparia', size=wx.Size(800,600))
        self.calc = calculator.Calculator()
        self.panel = wx.Panel(self)

        if mode == "debug":
            self.main_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel)
            self.calculate_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel)

            self.utility_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel)
            self.profit_sizer = wx.GridSizer(cols=1)
        else:
            self.main_sizer = wx.BoxSizer(wx.VERTICAL)
            self.calculate_sizer = wx.BoxSizer(wx.VERTICAL)

            self.utility_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.profit_sizer = wx.GridSizer(cols=8)

        profit_list = ["Delirium Orbs", "Scarabs", "Essences"]
        
        self.create_item_profit_buttons(profit_list)

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
        self.main_sizer.Add(self.profit_sizer, 0, wx.EXPAND, 0)
        self.main_sizer.AddStretchSpacer()
        self.main_sizer.Add(self.utility_sizer, 0 , wx.ALL | wx.EXPAND, 5)

        self.utility_sizer.Add(back_button, 0, wx.EXPAND, 5)
        self.utility_sizer.AddStretchSpacer()
        self.utility_sizer.Add(refresh_button, 0, wx.EXPAND, 5)

        self.panel.SetSizerAndFit(self.main_sizer)
        self.Show()

    def profit_calc(self, event):
        data = self.calc.profit_calc(event.GetEventObject().Name)
        print(event.GetEventObject().Name)
        self.hide_buttons()
        
        #data = json.load(open("sample_data.json"))
        self.profit_sizer.SetCols(8)
        self.profit_sizer.SetRows(2)

        for targets, profit in data.items():
            entry_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label=targets)
            self.profit_sizer.Add(entry_sizer, 0, wx.ALL, 5)
           
            for item in profit:
                profit_details = wx.StaticText(self.panel, label=str(item))
                profit_details.SetBackgroundColour(wx.GREEN)
                entry_sizer.Add(profit_details, 0, wx.ALL, 5)

        #self.profit_sizer.CalcRowsCols()
        self.panel.Layout()
               
            
    def hide_buttons(self):
        self.calculate_sizer.ShowItems(False)

    def show_buttons(self):
        self.calculate_sizer.ShowItems(True)

    def refresh_data(self, event):
        self.calc.refresh_prices()

    def return_to_menu(self, event):
        self.show_buttons()
    
    def create_item_profit_buttons(self, profit_list):
        for item in profit_list:
            button = wx.Button(self.panel, label=item, name=item)
            button.Bind(wx.EVT_BUTTON, self.profit_calc)
            self.calculate_sizer.Add(button, 0, wx.CENTER, 0)

        width, height = self.get_max_size(self.calculate_sizer)

        for child in self.calculate_sizer.GetChildren():
            child.SetMinSize(width, height)

    def get_max_size(self, sizer):
        max_width = 0
        max_height = 0

        for child in sizer.GetChildren():
            if child.GetSize().Width > max_width:
                max_width = child.GetSize().Width

            if child.GetSize().Width > max_height:
                max_height = child.GetSize().Height
    
        return [max_width, max_height]
        

if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow("debug")
    app.MainLoop()
