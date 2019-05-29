# if self.item_type == 0:
#     # 如果第一个点不存在（self.firstx 和 self.firsty都小于0）
#     if self.firstx < -1 and self.firsty < -1:
#         self.firstx, self.firsty = event.x, event.y
#     # 删除上一次绘制的虚线图形
#     if self.temp_item is not None:
#         self.cv.delete(self.temp_item)
#     # 重新绘制虚线
#     self.temp_item = self.cv.create_line(self.firstx, self.firsty,
#                                          event.x, event.y, dash=2, arrow=LAST)


import tkinter
import IOFile as fio

obj_list = []    # list of created objects [name,type,canvas,x,y,x2,y2] type: 1 element
line_list = []   # list of created line [id(x+y),type,canvas,id,x,y,x2,y2] type:0 line
lines_temp_from = []   # save temp lines which are from the related object for movement
lines_temp_to = []   # save temp lines which link to the related object for movement
solid_line = []
press_element = ''   # clicked element




def dnd_start(source, event):
    h = DndHandler(source, event)
    if h.root:
        return h
    else:
        return None


# The class that does the work

class DndHandler:
    root = None
    def __init__(self, source, event):
        if event.num > 5:
            return
        root = event.widget._root()
        try:
            root.__dnd
            return  # Don't start recursive dnd
        except AttributeError:
            root.__dnd = self
            self.root = root
        self.source = source
        self.target = None
        self.initial_button = button = event.num
        self.initial_widget = widget = event.widget
        self.release_pattern = "<B%d-ButtonRelease-%d>" % (button, button)
        self.save_cursor = widget['cursor'] or ""
        widget.bind(self.release_pattern, self.on_release)
        widget.bind("<Motion>", self.on_motion)
        widget['cursor'] = "hand2"



    def __del__(self):
        root = self.root
        self.root = None
        if root:
            try:
                del root.__dnd
            except AttributeError:
                pass

    def on_motion(self, event):
        x, y = event.x_root, event.y_root
        target_widget = self.initial_widget.winfo_containing(x, y)
        source = self.source
        new_target = None
        while target_widget:
            try:
                attr = target_widget.dnd_accept
            except AttributeError:
                pass
            else:
                new_target = attr(source, event)
                if new_target:
                    break
            target_widget = target_widget.master
        old_target = self.target
        if old_target is new_target:
            if old_target:
                old_target.dnd_motion(source, event)
        else:
            if old_target:
                self.target = None
                old_target.dnd_leave(source, event)
            if new_target:
                new_target.dnd_enter(source, event)
                self.target = new_target

    def on_release(self, event):
        self.finish(event, 1)

    def cancel(self, event=None):
        self.finish(event, 0)

    def finish(self, event, commit=0):
        target = self.target
        source = self.source
        widget = self.initial_widget
        root = self.root
        try:
            del root.__dnd
            self.initial_widget.unbind(self.release_pattern)
            self.initial_widget.unbind("<Motion>")
            widget['cursor'] = self.save_cursor
            self.target = self.source = self.initial_widget = self.root = None
            if target:
                if commit:
                    target.dnd_commit(source, event)
                else:
                    target.dnd_leave(source, event)
        finally:
            source.dnd_end(target, event)

class object_icon:
    def __init__(self, name):
        self.name = name
        self.canvas = self.label = self.id = None


    def attach(self, canvas, x, y):
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return
        label = tkinter.Label(canvas, text=self.name,borderwidth=2, relief="raised")
        id = canvas.create_window(x, y, window=label, anchor="nw")
        self.canvas = canvas
        self.label = label
        self.id = id
        label.bind("<ButtonPress>", self.press)
        x1, y1, x2, y2 = self.canvas.bbox(self.id) # get element's geometric info
        obj_list.append([self.name, 1, self.canvas, x1, y1, x2, y2]) #insert new elemnt obj list

    def detach(self):
        canvas = self.canvas
        if not canvas:
            return
        id = self.id
        label = self.label
        self.canvas = self.label = self.id = None
        canvas.delete(id)
        label.destroy()

    def press(self, event):
        global press_element
        if dnd_start(self, event):
            # where the pointer is relative to the label widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)
            if press_element != self.name:
                press_element = self.name #update press_element
                solid_line.clear()
            relationship.get_line_group(self,press_element) # get related lines 点击对像时就一次性获取所有关联线条



    def move(self, event):
        x, y = self.where(self.canvas, event)
        self.canvas.coords(self.id, x, y)
        print("move: id-%d, x-%d,y-%d" %(self.id,x,y))

    def putback(self):
        self.canvas.coords(self.id, self.x_orig, self.y_orig)

    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off

    def dnd_end(self, target, event):
        pass




class object_item:

    def __init__(self, main_app, canvas_candidate):
        self.canvas = canvas_candidate
        #self.top = tkinter.Toplevel(main_app) ##这里产生了三个窗口，去除！
        self.dot_line = []
        self.temp_line_to = None
        self.temp_line_from = None
        # self.prev_fx=self.prev_fy=self.prev_tx=self.prev_ty=0

        self.canvas.dnd_accept = self.dnd_accept



    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source.id)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)


    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)

        # 删除上一次绘制的虚线图形
        for i in range(len(self.dot_line)):
            self.canvas.delete(self.dot_line[i])
        self.dot_line.clear()

        if lines_temp_to:
            for i in range(len(lines_temp_to)):
                lines_temp_to[i][2].delete(lines_temp_to[i][3])
        if lines_temp_from:
            for i in range(len(lines_temp_from)):
                lines_temp_from[i][2].delete(lines_temp_from[i][3])
        if solid_line:
            print(len(solid_line))
            for i in range(len(solid_line)):
                solid_line[i][2].delete(solid_line[i][3])




        # 实时重绘虚线
        if lines_temp_to:
            for i in range(len(lines_temp_to)):
                print("line_to:",x, y, x1, y1, x2, y2)
                self.temp_line_to = self.canvas.create_line(lines_temp_to[i][4],
                                                             lines_temp_to[i][5], x, y, dash=2, arrow="last")
                self.dot_line.append(self.temp_line_to)
                self.prev_tx = lines_temp_to[i][6] = x   ##update temp line position
                self.prev_ty = lines_temp_to[i][7] = y
                lines_temp_to[i][3] = self.temp_line_to
                lines_temp_to[i][2] = self.canvas




        if lines_temp_from:
            for i in range(len(lines_temp_from)):
                print("line_from:", x, y, x1, y1, x2, y2)
                self.temp_line_from = self.canvas.create_line(x, y,
                                                             lines_temp_from[i][6],lines_temp_from[i][7], dash=2, arrow="last")
                self.dot_line.append(self.temp_line_from)
                self.prev_fx = lines_temp_from[i][4] = x
                self.prev_fy = lines_temp_from[i][5] = y
                lines_temp_from[i][3] = self.temp_line_from
                lines_temp_from[i][2] = self.canvas


        update_coord(x, y, x2, y2,1,press_element)



    def dnd_leave(self, source, event):
        global line_list
        global lines_temp_to
        global lines_temp_from
        global obj_list
        global solid_line
        self.canvas.delete(self.dndid)
        self.dndid = None
        # if lines_temp_from:
        #     self.canvas=lines_temp_from[0][2]
        #
        # if lines_temp_to:
        #     self.canvas = lines_temp_to[0][2]


        for i in range(len(self.dot_line)):
            self.canvas.delete(self.dot_line[i])
        self.dot_line.clear()

        # if lines_temp_from:
        for j in range(len(lines_temp_from)):
            self.lineid = self.canvas.create_line(lines_temp_from[j][4]+20, lines_temp_from[j][5]+10,
                                                      lines_temp_from[j][6] + 20
                                                      , lines_temp_from[j][7] + 10, fill="red", width=2,
                                                      joinstyle="round")
            lines_temp_from[j][3] = self.lineid


        # # if lines_temp_to:
        for j in range(len(lines_temp_to)):
            self.lineid = self.canvas.create_line(lines_temp_to[j][4] + 20, lines_temp_to[j][5] + 10,
                                                      lines_temp_to[j][6]+20
                                                      , lines_temp_to[j][7]+10, fill="red", width=2,
                                                      joinstyle="round")
            lines_temp_to[j][3]=self.lineid
        solid_line = lines_temp_from+lines_temp_to


    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
        source.attach(self.canvas, x, y)





class relationship:
    '''
    Construct relationship among elements
    '''
    def __init__(self, canvas):
        self.canvas = canvas
        # self.src = src
        # self.dest = dest
        # self.line_type = line_type
        # obj_relation.append(src,dest,line_type)



    def insert_relation(self,x,y):
        return 0

    def insert_linetype(self):
        return 1


    def draw_line(self, src,dest):
        '''
        Draw a line by element id (source and destination)
        :param src: source element id
        :param dest: destination element id
        :return:
        '''
        if (self.get_element_coord(src,1) is not None) and (self.get_element_coord(dest,1) is not None):
            from_x,from_y,from_x2, from_y2 = self.get_element_coord(src,1)
            to_x, to_y, to_x2, to_y2 = self.get_element_coord(dest,1)
            # 绘制实际的直线
            line_id=self.canvas.create_line(from_x+20,from_y+10,to_x+20,to_y+10,
                                          fill="red", width=2, joinstyle="round")
            # insert new line to obj_list, type=0 :line
            line_list.append([str(from_x)+str(from_y), 0, self.canvas,line_id, from_x, from_y, to_x, to_y])
        else:
            return

        # d = obj_list[0][2] 存储的对像是可以再次当成对像使用的
        # d.delete(1)
    def get_element_coord(self, element_id, element_type):
        '''
        get coordinate of element by searching element_id
        :param element_id: element id
        :param element_type: 0 line, 1 object
        :return:
        '''
        for i in range(len(obj_list)):
            if (obj_list[i][0] == element_id) and (obj_list[i][1] == element_type):
                return obj_list[i][3:]


    def get_line_group(self,element_id):
        '''
        get coordinate of line which linked to element_id
        :param element_id:
        :return:
        '''
        lines_temp_to.clear()
        lines_temp_from.clear()
        for i in range(len(obj_list)):
            if (obj_list[i][0] == element_id) and (obj_list[i][1] == 1):
                this_x = obj_list[i][3]
                this_y = obj_list[i][4]
                for x in range(len(line_list)):
                    if (this_x+5 >= line_list[x][4] >= this_x-5) \
                            and (this_y-5 <= line_list[x][5] <= this_y+5):
                        lines_temp_from.append(line_list[x])
                    if (this_x-5 <= line_list[x][6] <= this_x+5) \
                            and (this_y-5 <= line_list[x][7] <= this_y+5):
                        lines_temp_to.append(line_list[x])
        # if lines_temp_from:  #输出临时文件
        #     fio.output_file("lines_temp_from.txt", 1, "Line from -- "+element_id+str(lines_temp_from))
        # if lines_temp_to:
        #     fio.output_file("lines_temp_to.txt", 1, "Line to -- :"+element_id+str(lines_temp_to))


def update_coord(top_x,top_y, to_x, to_y, type, obj_name): #type 0:line 1:element
    if type==1:
        for i in range(len(obj_list)):
            if obj_list[i][0] == obj_name:
                obj_list[i][3] = top_x
                obj_list[i][4] = top_y
                obj_list[i][5] = to_x
                obj_list[i][6] = to_y
    if type==0:
        for i in range(len(line_list)):
            if line_list[i][0]==obj_name:
                line_list[i][0]




