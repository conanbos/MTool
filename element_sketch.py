from tkinter import *
# 导入ttk
from tkinter import ttk
from object import *
from object import relationship
from object import object_icon
from object import object_item

import random

WIN_WIDTH = 1080
WIN_HEIGHT = 600

class element_sketch:
    def __init__(self, master):
        self.master = master
        # save default width 保存设置初始的边框宽度
        self.width = IntVar()
        self.width.set(1)
        # save default color 保存设置初始的边框颜色
        self.outline = 'black'
        # save default filled color保存设置初始的填充颜色
        self.fill = None
        # save pre-drag posX,Y 记录拖动时前一个点的x、y坐标
        self.prevx = self.prevy = -10
        # save drag posX,Y 记录拖动开始的第一个点的x、y坐标
        self.firstx = self.firsty = -10
        # save move-drag posX,Y 记录拖动右键来移动图形时前一个点的x、y坐标
        self.mv_prevx = self.mv_prevy = -10
        # item type 记录要绘制哪种图形
        self.item_type = 0
        self.points = []
        self.init_widgets()
        self.temp_item = None
        self.temp_items = []
        # 初始化选中的图形项
        self.choose_item = None

        # 创建界面组件
    def init_widgets(self):
        # Create button panel
        button_panel = Frame(self.master)
        button_panel.pack(side=TOP, pady=10)
        # Create source, destination and combination canvas.
        self.cv_src = Canvas(button_panel, background='white', width=WIN_WIDTH/2-20, height=WIN_HEIGHT/2-10, bd=2, relief='raised')
        self.cv_src.grid(row=0, column=0)
        self.cv_dest = Canvas(button_panel, background='white', width=WIN_WIDTH/2-20, height=WIN_HEIGHT/2-10, bd=2, relief='sunken')
        self.cv_dest.grid(row=0, column=1)
        self.cv_cmb = Canvas(button_panel, background='white', width=WIN_WIDTH-38, height=WIN_HEIGHT / 2-30, bd=2, relief='groove')
        self.cv_cmb.grid(row=1, column=0, columnspan=2)

        # self.cv_src.bind('<B1-Motion>', self.drag_event)


    def drag_event(self, event):
        print('I am here:% %', str(event.x), str(event.y))


# crate new object and attach to destination canvas
def create_objects(name, destination):
    new_obj = object_icon(name)
    new_obj.attach(destination, random.randrange(1, 500), random.randrange(1, 250))


def lanch(root_app):
    '''
    Initiate and bind all the elements to corresponding canvas
    :param root_app: tk main window
    :return: null
    '''
    app = element_sketch(root_app)
    # root.bind('<Delete>', app.delete_item)
    # list of source and target elements, it will be change to read elements from external file or model files.
    source_element = ["Functional view", "Function", "Exchange"]
    target_element = ["Primitive", "Port", "Connector"]

    # create  elements on source canvas from list source_element
    for i in range(len(source_element)):
        create_objects(source_element[i], app.cv_src)
    # create  elements on target canvas from list target_element
    for k in range(len(target_element)):
        create_objects(target_element[k], app.cv_dest)

    object_item(root_app, app.cv_src)
    object_item(root_app, app.cv_dest)
    object_item(root_app, app.cv_cmb)

    for i in range(len(obj_list)):
        print("created %s:" % str(i), obj_list[i])

    relation_pair.append([0, 2])
    relation_pair.append([1, 2])
    relation_pair.append([3, 4])
    relation_pair.append([3, 5])

    print("relation:%d", relation_pair)
    print("object position:%d", obj_position)

    tt=relationship(app.cv_dest)
    for i in range(len(relation_pair)):
        if i<2:
            tt = relationship(app.cv_src)
            tt.draw_line(i)
        else:
            tt = relationship(app.cv_dest)
            tt.draw_line(i)

# main programm
root = Tk()
root.title("Model Combination Tool")
root.iconbitmap('icons.ico')
size= str(WIN_WIDTH)+'x'+str(WIN_HEIGHT)+'+100+10'
root.geometry(size)
root.resizable(0, 0)
lanch(root)
root.mainloop()