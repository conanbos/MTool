import sys
import os
import main_UI as dnd
import pygubu
import Flash_screen



try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

# class SketchApp(wx.App):
#     def OnInit(self):
#         bmp = wx.Image("splash.png").ConvertToBitmap()
#         wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,1000, None, -1)
#         wx.Yield()
#         frame = SketchFrame(None)
#         frame.Show(True)
#         self.SetTopWindow(frame)
#         return True




class Myapp:
    """This is main class
    Hint"""
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__), "ui/main_window.ui")
        builder.add_from_file(fpath)
        mainwindow = builder.get_object('mainwindow', master)
        lb = builder.get_object('ttk.Label_1')
        lb.configure(text='lable')
        builder.connect_callbacks(self)
        callbacks = {'on_b1_clicked': self.on_button1_clicked}
        builder.connect_callbacks(callbacks)
        callbacks = {'on_b2_clicked': self.on_button2_clicked}
        builder.connect_callbacks(callbacks)

    def on_button1_clicked(self):
        # messagebox.showinfo('From callback', '按键一被按下!!')
        dnd.test()

    def on_button2_clicked(self):
        lb = self.builder.get_object('ttk.Label_1')
        lb.configure(text='recovery')
        messagebox.showinfo('From callback', 'Button 2 was clicked !!')
        sys.exit()


if __name__ == '__main__':
    root = tk.Tk()
    app = Myapp(root)
    root.mainloop()
#
# t4 = ab.Tester(root)
# t4.top.geometry("+340+360")
# i5 = ab.Icon("ICON5")
# i5.attach(t4.canvas, 50, 60)



