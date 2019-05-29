
from element_sketch import *
import IOFile as filet


# main programm
if __name__ == '__main__':
    root = Tk()
    root.title("Model Combination Tool")
    root.iconbitmap('icons.ico')
    size = str(WIN_WIDTH)+'x'+str(WIN_HEIGHT)+'+100+10'
    root.geometry(size)
    root.resizable(0, 0)
    lanch(root)
    root.mainloop()
