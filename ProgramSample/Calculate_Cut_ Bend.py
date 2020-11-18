from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
import tkinter.messagebox

class Calculate():

    # 初始框的声明
    def __init__(self):
        self.root = Tk()
        self.root.title('间隔条裁切折弯计算软件V0.0')
        self.root.resizable(0, 0)
        self.creat_widgets()

    width = []
    length = []
    number = []
    state = []
    k = 0

    # 双击进入编辑状态，修改表格中数值
    def set_cell_value(self, event):
        global k
        for item in self.treeview.selection():
            item_text = self.treeview.item(item, "values")
            #print(item_text[0:2])  # 输出所选行的值
        column = self.treeview.identify_column(event.x)# 列
        row = self.treeview.identify_row(event.y)  # 行
        cn = int(str(column).replace('#', ''), 16)
        rn = int(str(row).replace('I', ''), 16)-self.k
        print('cn,rn', cn, rn)
        entryedit = Text(self.mighty, width=10, height = 1)
        entryedit.place(x=16+(cn-1)*80, y=6+rn*20)
        def saveedit():
            self.treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
            for item1 in self.treeview.selection():
                item_text1 = self.treeview.item(item1, "values")
            self.width[rn-1] = int(item_text1[0].split('\n')[0])
            self.length[rn-1] = int(item_text1[1].split('\n')[0])
            self.number[rn-1] = int(item_text1[2].split('\n')[0])
            entryedit.destroy()
            okb.destroy()
            print(self.width, self.length, self.number)
        okb = ttk.Button(self.mighty, text='OK', width=4, command=saveedit)
        okb.place(x=70+(cn-1)*80, y=2+rn*20)

    # 新建行
    def newrow(self):
        self.width.append(800)
        self.length.append(1500)
        self.number.append(20)
        self.state.append('未完成')
        self.treeview.insert('', len(self.width)-1, values=(self.width[len(self.width)-1], self.length[len(self.width)-1],
                                                            self.number[len(self.width)-1], self.state[len(self.width)-1]))
        self.treeview.update()

    total_length = []
    width_length = []
    bend_length = []
    specification = []
    remain_length = []
    remain_num = []
    warehouse_no = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    warehouse_length = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    specifications = [1800, 2200, 2600, 3000, 3600, 4600, 6000]
    i, j = 0, 0

    # 间隔条裁切折弯算法程序
    def calculated_value(self):
        global i, j
        if self.number[self.j] > 0:
            if self.i == 0:  # 第一组间隔条计算程序
                self.total_length.append(self.width[self.j] + 200)
                for s in self.specifications:
                    if s > (self.width[self.j] + 200) * 2:
                        self.specification.append(s)
                        break
                self.width_length.append(self.width[self.j])
                self.bend_length.append((self.total_length[self.i] - self.width_length[self.i]) // 2)
                self.remain_length.append(self.specification[self.i] - self.total_length[self.i])
                self.warehouse_length[self.i] = self.remain_length[self.i]
                self.total_length.append((self.length[self.j] - self.bend_length[self.i]) * 2 + self.width[self.j])
                for s in self.specifications:
                    if (s - self.total_length[self.i + 1]) >= (self.width[self.j] + 200):
                        self.specification.append(s)
                        break
                self.width_length.append(self.width[self.j])
                self.bend_length.append((self.total_length[self.i + 1] - self.width_length[self.i + 1]) // 2)
                self.remain_length.append(self.specification[self.i + 1] - self.total_length[self.i + 1])
                self.warehouse_length[self.i + 1] = self.remain_length[self.i + 1]
                self.number[self.j] -= 2
                self.treeview1.insert('', len(self.total_length) - 2,
                                 values = (self.total_length[len(self.total_length) - 2], self.width_length[len(self.total_length) - 2],
                                          self.bend_length[len(self.total_length) - 2], self.specification[len(self.total_length) - 2],
                                          self.remain_length[len(self.total_length) - 2], self.number[self.j]))
                self.treeview1.insert('', len(self.total_length) - 1,
                                 values = (self.total_length[len(self.total_length) - 1], self.width_length[len(self.total_length) - 1],
                                          self.bend_length[len(self.total_length) - 1], self.specification[len(self.total_length) - 1],
                                          self.remain_length[len(self.total_length) - 1], self.number[self.j]))
                self.treeview1.update()
            else:
                self.width_length.append(self.width[self.j])
                for k in range(len(self.warehouse_length)):
                    if (self.warehouse_length[k] > self.width[self.j] + 160) and (
                            self.warehouse_length[k] < self.width[self.j] + (self.length[self.j] * 2) - 160):
                        self.total_length.append(self.warehouse_length[k])
                        self.warehouse_length[k] = 0
                        self.remain_length.append(0)
                        self.specification.append(0)
                        break
                else:
                    self.total_length.append(self.width[self.j] + 200)
                    for s in self.specifications:
                        if s > (self.width[self.j] + 200) * 2:
                            self.specification.append(s)
                            break
                    self.remain_length.append(self.specification[self.i] - self.total_length[self.i])
                    for k in range(len(self.warehouse_length)):
                        if self.warehouse_length[k] == 0:
                            self.warehouse_length[k] = self.remain_length[i]
                            break
                self.bend_length.append((self.total_length[self.i] - self.width_length[self.i]) // 2)
                self.treeview1.insert('', len(self.total_length) - 1,
                                 values = (self.total_length[len(self.total_length) - 1], self.width_length[len(self.total_length) - 1],
                                         self.bend_length[len(self.total_length) - 1], self.specification[len(self.total_length) - 1],
                                         self.remain_length[len(self.total_length) - 1], self.number[self.j]))
                self.treeview1.update()
                self.width_length.append(self.width[self.j])
                self.total_length.append((self.length[self.j] - self.bend_length[self.i]) * 2 + self.width[self.j])
                self.bend_length.append((self.total_length[self.i + 1] - self.width_length[self.i + 1]) // 2)
                for s in self.specifications:
                    if (s - self.total_length[self.i + 1]) >= (self.width[self.j] + 200):
                        self.specification.append(s)
                        break
                self.remain_length.append(self.specification[self.i + 1] - self.total_length[self.i + 1])
                for k in range(len(self.warehouse_length)):
                    if self.warehouse_length[k] == 0:
                        self.warehouse_length[k] = self.remain_length[self.i + 1]
                        break
                self.number[self.j] -= 1
                if self.number[self.j] == 0:
                    self.state[self.j] = ('完成')
                self.k += len(self.width)
                for _ in map(self.treeview.delete, self.treeview.get_children("")):
                    pass
                for n in range(len(self.width)):  # 写入数据
                    self.treeview.insert('', n, values=(self.width[n], self.length[n], self.number[n], self.state[n]))
                print('k1=', self.k)

                self.treeview1.insert('', len(self.total_length) - 1,
                                 values = (self.total_length[len(self.total_length) - 1], self.width_length[len(self.total_length) - 1],
                                         self.bend_length[len(self.total_length) - 1], self.specification[len(self.total_length) - 1],
                                         self.remain_length[len(self.total_length) - 1], self.number[self.j]))
                self.treeview1.update()

            for _ in map(self.treeview2.delete, self.treeview2.get_children("")):
                pass
            for n in range(min(len(self.warehouse_no), len(self.warehouse_length))):  # 写入数据
                self.treeview2.insert('', n, values=(self.warehouse_no[n], self.warehouse_length[n]))
            # 将计算数据显示在文本框中
            self.scr.config(state=NORMAL)
            self.scr.insert(INSERT, '********************************************************************************\n\n' +
                       f"第{self.i + 1}根间隔条，总长{self.total_length[self.i]}mm，全边长{self.width_length[self.i]}mm，折边长{self.bend_length[self.i]}mm，"
                       f"余长{self.remain_length[self.i]}mm\n第{self.i + 2}根间隔条，总长{self.total_length[self.i + 1]}mm，全边长{self.width_length[self.i + 1]}mm，"
                       f"折边长{self.bend_length[self.i + 1]}mm，余长{self.remain_length[self.i + 1]}mm\n\n" +
                       '********************************************************************************\n')
            self.scr.config(state=DISABLED)
            self.i += 2
            print(self.total_length, self.width_length, self.bend_length, self.specification, self.remain_length,
                  self.number[self.j], self.i)
        else:
            if self.j < len(self.number)-1:
                self.j += 1
                self.calculated_value()
            else:
                tkinter.messagebox.showinfo(title='完成提示', message='计算完成，请添加新的生产数据')

    def clear_table(self):
        global i, j, k
        self.k += len(self.width)
        print('k=', self.k)
        self.total_length.clear()
        self.width_length.clear()
        self.bend_length.clear()
        self.specification.clear()
        self.remain_length.clear()
        self.width.clear()
        self.length.clear()
        self.number.clear()
        self.state.clear()
        self.i, self.j = 0, 0
        for n in range(len(self.warehouse_length) - 1):
            self.warehouse_length[n] = 0
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for _ in map(self.treeview1.delete, self.treeview1.get_children("")):
            self.treeview1.update()
        for _ in map(self.treeview2.delete, self.treeview2.get_children("")):
            pass
        for n in range(min(len(self.warehouse_no), len(self.warehouse_length))):  # 写入数据
            self.treeview2.insert('', n, values=(self.warehouse_no[n], self.warehouse_length[n]))
        self.scr.config(state=NORMAL)
        self.scr.delete(1.0, END)
        self.scr.config(state=DISABLED)

    def creat_widgets(self):
        '''
        1.遍历表格
        t = treeview.get_children()
        for i in t:
            print(treeview.item(i,'values'))
        2.绑定单击离开事件
        def treeviewClick(event):  # 单击
            for item in tree.selection():
                item_text = tree.item(item, "values")
                print(item_text[0:2])  # 输出所选行的第一列的值
        tree.bind('<ButtonRelease-1>', treeviewClick)
        ------------------------------
        鼠标左键单击按下1/Button-1/ButtonPress-1 
        鼠标左键单击松开ButtonRelease-1 
        鼠标右键单击3 
        鼠标左键双击Double-1/Double-Button-1 
        鼠标右键双击Double-3 
        鼠标滚轮单击2 
        鼠标滚轮双击Double-2 
        鼠标移动B1-Motion 
        鼠标移动到区域Enter 
        鼠标离开区域Leave 
        获得键盘焦点FocusIn 
        失去键盘焦点FocusOut 
        键盘事件Key 
        回车键Return 
        控件尺寸变Configure
        ------------------------------
        '''
        # 创建窗口型号显示表格
        columns = ("宽度W", "长度L", "数量N", "状态S")
        self.mighty = ttk.LabelFrame(self.root, text='所需窗框型号')
        self.mighty.grid(column=0, row=0, padx=8, pady=4)
        self.ybar = Scrollbar(self.mighty, orient='vertical') # 创建滑动条
        self.treeview = ttk.Treeview(self.mighty, show="headings", height=18, columns=columns,
                                     yscrollcommand=self.ybar.set)  # 创建窗口型号显示表格
        self.ybar['command'] = self.treeview.yview
        self.treeview.column("宽度W", width=80, anchor='center')  # 表示列,不显示
        self.treeview.column("长度L", width=80, anchor='center')
        self.treeview.column("数量N", width=80, anchor='center')
        self.treeview.column("状态S", width=80, anchor='center')
        self.treeview.heading("宽度W", text="宽度W")  # 显示表头
        self.treeview.heading("长度L", text="长度L")
        self.treeview.heading("数量N", text="数量N")
        self.treeview.heading("状态S", text="状态S")
        self.treeview.grid(row=0, column=0)
        self.ybar.grid(row=0, column=1, sticky='ns')

        self.treeview.bind('<Double-1>', self.set_cell_value)  # 双击左键进入编辑
        self.newb = ttk.Button(self.mighty, text='新建窗框型号', width=15, command=self.newrow)
        self.newb.grid(row=1, column=0, sticky='s')

        # 创建间隔条裁切折弯计算结果显示表格
        self.columns1 = ("总长", "全边", "折边", "规格", "余长", "剩余")
        self.mighty1 = ttk.LabelFrame(self.root, text='裁切折弯间隔条计算值')
        self.mighty1.grid(column=1, row=0, padx=8, pady=4)
        self.ybar1=Scrollbar(self.mighty1,orient='vertical')    # 创建滑动条
        self.treeview1 = ttk.Treeview(self.mighty1, show="headings", height=18, columns=self.columns1,
                                      yscrollcommand=self.ybar1.set)    # 创建表格
        self.ybar1['command']= self.treeview1.yview
        self.treeview1.column("总长", width=80, anchor='center')  # 表示列,不显示
        self.treeview1.column("全边", width=80, anchor='center')
        self.treeview1.column("折边", width=80, anchor='center')
        self.treeview1.column("规格", width=80, anchor='center')
        self.treeview1.column("余长", width=80, anchor='center')
        self.treeview1.column("剩余", width=80, anchor='center')
        self.treeview1.heading("总长", text="总长") # 显示表头
        self.treeview1.heading("全边", text="全边")
        self.treeview1.heading("折边", text="折边")
        self.treeview1.heading("规格", text="规格")
        self.treeview1.heading("余长", text="余长")
        self.treeview1.heading("剩余", text="剩余")
        self.treeview1.grid(row=0, columnspan=2)
        self.ybar1.grid(row=0,column=2,sticky='ns')

        # 创建缓存仓存料情况显示表格
        self.columns2 = ("仓号", "料长")
        self.mighty2 = ttk.LabelFrame(self.root, text='缓存仓存料情况')
        self.mighty2.grid(column=2, row=0, padx=8, pady=4)
        self.ybar2 = Scrollbar(self.mighty2,orient='vertical')
        self.treeview2 = ttk.Treeview(self.mighty2, show="headings", height=19, columns=self.columns2,
                                      yscrollcommand=self.ybar2.set)  # 表格
        self.ybar2['command'] = self.treeview2.yview
        self.treeview2.column("仓号", width=100, anchor='center')  # 表示列,不显示
        self.treeview2.column("料长", width=100, anchor='center')
        self.treeview2.heading("仓号", text="仓号") # 显示表头
        self.treeview2.heading("料长", text="料长")
        self.treeview2.grid(row=0, column=0)
        self.ybar2.grid(row=0, column=1, sticky='ns')

        self.cal_start = ttk.Button(self.mighty1, text='开始计算', width=15, command=self.calculated_value)
        self.cal_start.grid(row=1, column=0, sticky='s')

        self.clear_table = ttk.Button(self.mighty1, text='清空列表', width=15, command=self.clear_table)
        self.clear_table.grid(row=1, column=1, sticky='s')

        self.mighty3 = ttk.LabelFrame(self.root, text='计算信息')
        self.mighty3.grid(column=0, row=1, padx=8, pady=4, columnspan=3)
        self.scr = scrolledtext.ScrolledText(self.mighty3, width=170, height=10, wrap=WORD)
        self.scr.grid(column=0, row=0, sticky='WE')

cal = Calculate()
cal.root.mainloop()  # 进入消息循环