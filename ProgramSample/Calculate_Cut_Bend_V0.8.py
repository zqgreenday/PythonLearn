from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
import tkinter.messagebox
import csv
import serial
import serial.tools.list_ports
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import threading
import logging, logging.handlers
import turtle

class CalculateApp():
    # 程序初始化函数
    def __init__(self):
        self.root = Tk()  # 调用Tk()函数声明主窗口
        self.root.title('间隔条定长裁切折弯计算软件')  # 设置主窗口标题
        self.root.iconphoto(False, PhotoImage(file='D:\data\calculator.png'))  # 添加主窗口Logo
        self.root.resizable(0, 0)  # 主窗口尺寸无法调整
        self.creat_widgets()  # 调用组件生成函数
        self.root.update()  # 主窗口尺寸更新
        self.win_width = self.root.winfo_width()  # 读取主窗口宽度
        self.win_height = self.root.winfo_height()  # 读取主窗口长度
        self.screen_width = self.root.winfo_screenwidth()  # 读取电脑屏幕宽度
        self.screen_height = self.root.winfo_screenheight()  # 读取电脑屏幕长度
        # 根据屏幕尺寸和窗口尺寸，设置主窗口在屏幕上显示的位置
        self.root.geometry(
            f"+{int((self.screen_width - self.win_width) / 2)}+{int((self.screen_height - self.win_height) / 2)-40}")
        self.logger = modbus_tk.utils.create_logger("dummy")  # 调用modubus_tk模块内的Logger方法
        self.com_state = False  # 默认串口为关闭状态
        self.radSel = 2  # 默认为离线操作
        self.send_data['state'] = 'disabled'  # 数据发送按钮状态默认无效
        self.Init = 0  # 设备默认未完成初始化状态
        self.cut_achieve = 0  # 裁切设备默认未就绪状态
        self.com_datamonitor_win_run = False  # 通讯数据监控窗口默认未打开状态
        self.com_config_win_run = False  # 串口设置窗口默认未打开状态
        self.sketch_map_run = False  # 组框示意图窗口默认未打开状态
        self.operator_manual_run = False  # 操作说明窗口默认未打开状态
        self.about_run = False  # 关于窗口默认未打开状态
        self.set_cell_value_win_run = False  # 窗框生产数据设置窗口默认未打开状态
        self.calculated_confirm = False  # 间隔条计算开始确认

    produceNo_list = []  # 窗框生产编号
    produceNo = 0
    width = []  # 间隔条窗框的宽度
    length = []  # 间隔条窗框的长度
    number = []  # 间隔条窗框的数量
    state = []  # 间隔条窗框的状态
    remain_num = []  # 剩余窗框数量
    k = 0  # 窗框设置表格新建行计数
    k_list = []  # 记录K数值

    total_length = []  # 裁切间隔条的总长
    width_length = []  # 裁切间隔条的宽度
    bend_length = []  # 裁切间隔条的折弯长度
    specification = []  # 裁切间隔条的规格
    remain_length = []  # 裁切间隔条的余长
    remain_num_list = []  # 剩余间隔条列表
    frame_No = []  # 生产窗框编号列表
    warehouse_no = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # 缓存仓编号
    warehouse_length = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 缓存仓存料情况
    specifications = [1800, 2200, 2600, 3000, 3600, 4600, 6000]  # 间隔条的规格
    i, j, n = 0, 0, -1  # i：间隔条生产数量计数 j:窗框生产数量列表编号 n：自动计算指示
    i_list = []
    j_list = []
    filename0 = 'D:\data\data0.csv'
    data0 = [produceNo_list, width, length, number, state]
    filename1 = 'D:\data\data1.csv'
    data1 = [frame_No, total_length, width_length, bend_length, specification, remain_length, remain_num_list]
    filename2 = 'D:\data\data2.csv'
    data2 = [warehouse_no, warehouse_length]
    filename3 = 'D:\data\data3.csv'
    data3 = [i_list, j_list, k_list, remain_num]

    # 窗框参数修改窗口
    def set_cell_value_fun(self):
        if self.state[self.rn-1] == '未完成':
            if self.calculated_confirm == False:
                if self.set_cell_value_win_run == False:
                    self.set_cell_value_win = Toplevel()
                    self.set_cell_value_win.title('窗框参数修改')
                    self.set_cell_value_win.transient(self.root)
                    self.root.update()
                    self.set_cell_value_win.geometry(f"+{self.root.winfo_x() + 260}+{self.root.winfo_y() + 80}")
                    self.set_cell_value_win.resizable(0, 0)
                    rowno_label = Label(self.set_cell_value_win, text=f'正在修改编号{self.rn}的数据',
                                        font=('微软雅黑', 10, "bold"), background="DarkCyan", foreground='white')
                    rowno_label.grid(row=0, columnspan=2, padx=4, pady=4)
                    width_label = Label(self.set_cell_value_win, text='窗框宽度设定：')
                    width_label.grid(row=1, column=0, sticky='W', padx=4, pady=4)
                    width_entry = Entry(self.set_cell_value_win, width=10)
                    width_entry.grid(row=1, column=1, sticky='W', padx=4, pady=4)
                    width_entry.insert(0, self.width[self.rn-1])
                    length_label = Label(self.set_cell_value_win, text='窗框长度设定：')
                    length_label.grid(row=2, column=0, sticky='W', padx=4, pady=4)
                    length_entry = Entry(self.set_cell_value_win, width=10)
                    length_entry.grid(row=2, column=1, sticky='W', padx=4, pady=4)
                    length_entry.insert(0, self.length[self.rn - 1])
                    number_label = Label(self.set_cell_value_win, text='窗框数量设定：')
                    number_label.grid(row=3, column=0, sticky='W', padx=4, pady=4)
                    number_entry = Entry(self.set_cell_value_win, width=10)
                    number_entry.grid(row=3, column=1, sticky='W', padx=4, pady=4)
                    number_entry.insert(0, self.number[self.rn - 1])
                    # 保存输入的窗框设置数值
                    def saveedit():
                        self.treeview.set(self.item, column=1, value=width_entry.get())
                        self.treeview.set(self.item, column=2, value=length_entry.get())
                        self.treeview.set(self.item, column=3, value=number_entry.get())
                        for item1 in self.treeview.selection():
                            item_text1 = self.treeview.item(item1, "values")
                        self.width[self.rn-1] = int(item_text1[1].split('\n')[0])
                        self.length[self.rn-1] = int(item_text1[2].split('\n')[0])
                        self.number[self.rn-1] = int(item_text1[3].split('\n')[0])
                        self.remain_num[self.rn - 1] = self.number[self.rn - 1]
                        self.set_cell_value_win.destroy()
                    save_button = ttk.Button(self.set_cell_value_win, text='保存修改', width=10, command=saveedit)  # 数值保存按钮
                    save_button.grid(row=4, columnspan=2, padx=4, pady=4)
                    self.set_cell_value_win_run = True
                else:
                    self.set_cell_value_win_run = False
                    self.set_cell_value_win.destroy()
                    self.set_cell_value_fun()
            else:
                tkinter.messagebox.showwarning(title='操作提示', message='本次生产数据已经开始计算无法进行修改！！')
        else:
            tkinter.messagebox.showwarning(title='操作提示', message='该生产数据已完成，无法进行修改，请添加新的生产数据！！')

    # 双击弹出本行窗框参数修改窗口
    def set_cell_value(self, event):
        global k
        for self.item in self.treeview.selection():
            item_text = self.treeview.item(self.item, "values")
            #print(item_text[0:2])  # 输出所选行的值
        column = self.treeview.identify_column(event.x)  # 列
        row = self.treeview.identify_row(event.y)  # 行
        self.cn = int(str(column).replace('#', ''), 16)  # 计算列编号
        self.rn = int(str(row).replace('I', ''), 16)-self.k  # 计算行编号
        self.set_cell_value_fun()

    # 新建窗框设置表格行
    def newrow(self):
        self.produceNo += 1
        self.produceNo_list.append(self.produceNo)
        self.width.append(800)
        self.length.append(1500)
        self.number.append(20)
        self.state.append('未完成')
        self.remain_num.append(self.number[len(self.number)-1])
        self.treeview.insert('', len(self.width)-1, values=(self.produceNo_list[len(self.width)-1],
                                                            self.width[len(self.width)-1],
                                                            self.length[len(self.width)-1],
                                                            self.number[len(self.width)-1],
                                                            self.state[len(self.width)-1]))
        self.treeview.update()
        self.treeview.yview_moveto(1.0)  # 自动移动到滑动条最底部

        fo0 = open(self.filename0, "w")
        fo0.truncate()  # 清空Excel数据
        fo0.close
        fo1 = open(self.filename1, "w")
        fo1.truncate()
        fo1.close
        fo2 = open(self.filename2, "w")
        fo2.truncate()
        fo2.close
        fo3 = open(self.filename3, "w")
        fo3.truncate()
        fo3.close
        self.i_list.append(self.i)
        self.j_list.append(self.j)
        self.k_list.append(self.k)
        with open(self.filename0, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.data0)

        with open(self.filename1, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.data1)

        with open(self.filename2, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.data2)
        with open(self.filename3, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.data3)

    # 间隔条裁切折弯算法程序
    def calculated_value(self):
        if bool(self.width and self.length and self.number) == False:
            tkinter.messagebox.showwarning(title='操作提示', message='请添加窗框生产数据再进行计算！！')
        elif (self.radSel == 0 or self.radSel == 1) and self.Init == 0:
            tkinter.messagebox.showwarning(title='操作提示', message='请等待设备初始化完成再开始计算！')
        elif (self.radSel == 0 or self.radSel == 1) and self.com_state == False:
            tkinter.messagebox.showerror(title='错误', message='没有与PLC建立连接不能进行计算！！')
        else:
            if self.remain_num[self.j] > 0:
                if self.calculated_confirm == False:
                    self.calculated_confirm = tkinter.messagebox.askokcancel(title='操作提示', message='请确认本次生产数据正误，'
                                                                                               '计算开始后当前生产数据将无法更改！！！\n'
                                                                                               '确定开始计算吗？')
                if self.calculated_confirm == True:
                    if self.radSel == 0:
                        self.cal_start['state'] = 'disabled'
                        self.send_data['state'] = 'normal'
                        self.auto_Rad['state'] = 'disabled'
                        self.offline_Rad['state'] = 'disabled'
                    if (self.radSel == 1) and (self.n < 0):
                        self.cal_start['state'] = 'disabled'
                        self.send_data['state'] = 'disabled'
                        self.manual_Rad['state'] = 'disabled'
                        self.offline_Rad['state'] = 'disabled'
                    if self.radSel == 2:
                        self.manual_Rad['state'] = 'disabled'
                        self.auto_Rad['state'] = 'disabled'
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
                        self.remain_num_list.append(self.remain_num[self.j])
                        self.frame_No.append(self.i//2 + 1)
                        self.treeview1.insert('', len(self.total_length) - 2,
                                              values=(self.frame_No[len(self.total_length) - 2],
                                                      self.total_length[len(self.total_length) - 2],
                                                      self.width_length[len(self.total_length) - 2],
                                                      self.bend_length[len(self.total_length) - 2],
                                                      self.specification[len(self.total_length) - 2],
                                                      self.remain_length[len(self.total_length) - 2],
                                                      self.remain_num_list[len(self.total_length) - 2]))
                        self.total_length.append((self.length[self.j] - self.bend_length[self.i]) * 2 + self.width[self.j])
                        for s in self.specifications:
                            if (s - self.total_length[self.i + 1]) >= (self.width[self.j] + 200):
                                self.specification.append(s)
                                break
                        self.width_length.append(self.width[self.j])
                        self.bend_length.append((self.total_length[self.i + 1] - self.width_length[self.i + 1]) // 2)
                        self.remain_length.append(self.specification[self.i + 1] - self.total_length[self.i + 1])
                        self.warehouse_length[self.i + 1] = self.remain_length[self.i + 1]
                        self.remain_num[self.j] -= 1
                        self.remain_num_list.append(self.remain_num[self.j])
                        self.frame_No.append(self.i // 2 + 1)
                        self.treeview1.insert('', len(self.total_length) - 1,
                                              values=(self.frame_No[len(self.total_length) - 1],
                                                      self.total_length[len(self.total_length) - 1],
                                                      self.width_length[len(self.total_length) - 1],
                                                      self.bend_length[len(self.total_length) - 1],
                                                      self.specification[len(self.total_length) - 1],
                                                      self.remain_length[len(self.total_length) - 1],
                                                      self.remain_num_list[len(self.total_length) - 1]))
                        self.treeview1.update()
                    else:
                        self.width_length.append(self.width[self.j])
                        for p in range(len(self.warehouse_length)):
                            if (self.warehouse_length[p] > self.width[self.j] + 160) and (
                                    self.warehouse_length[p] < self.width[self.j] + (self.length[self.j] * 2) - 160):
                                self.total_length.append(self.warehouse_length[p])
                                self.warehouse_length[p] = 0
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
                            for q in range(len(self.warehouse_length)):
                                if self.warehouse_length[q] == 0:
                                    self.warehouse_length[q] = self.remain_length[self.i]
                                    break
                        self.bend_length.append((self.total_length[self.i] - self.width_length[self.i]) // 2)
                        self.frame_No.append(self.i//2 + 1)
                        self.remain_num_list.append(self.remain_num[self.j])
                        self.treeview1.insert('', len(self.total_length) - 1,
                                           values=(self.frame_No[len(self.total_length) - 1],
                                                   self.total_length[len(self.total_length) - 1],
                                                   self.width_length[len(self.total_length) - 1],
                                                   self.bend_length[len(self.total_length) - 1],
                                                   self.specification[len(self.total_length) - 1],
                                                   self.remain_length[len(self.total_length) - 1],
                                                   self.remain_num_list[len(self.total_length) - 1]))
                        self.treeview1.update()
                        self.width_length.append(self.width[self.j])
                        self.total_length.append((self.length[self.j] - self.bend_length[self.i]) * 2 + self.width[self.j])
                        self.bend_length.append((self.total_length[self.i + 1] - self.width_length[self.i + 1]) // 2)
                        for s in self.specifications:
                            if (s - self.total_length[self.i + 1]) >= (self.width[self.j] + 200):
                                self.specification.append(s)
                                break
                        self.remain_length.append(self.specification[self.i + 1] - self.total_length[self.i + 1])
                        for p in range(len(self.warehouse_length)):
                            if self.warehouse_length[p] == 0:
                                self.warehouse_length[p] = self.remain_length[self.i + 1]
                                break
                        self.remain_num[self.j] -= 1
                        self.remain_num_list.append(self.remain_num[self.j])
                        self.frame_No.append(self.i//2 + 1)
                        if self.remain_num[self.j] == 0:
                            self.state[self.j] = ('完成')
                            self.k += len(self.width)
                            for _ in map(self.treeview.delete, self.treeview.get_children("")):
                                pass
                            for p in range(len(self.width)):  # 写入数据
                                self.treeview.insert('', p,
                                                     values=(self.produceNo_list[p], self.width[p], self.length[p],
                                                             self.number[p], self.state[p]))

                        self.treeview1.insert('', len(self.total_length) - 1,
                                              values=(self.frame_No[len(self.total_length) - 1],
                                                      self.total_length[len(self.total_length) - 1],
                                                      self.width_length[len(self.total_length) - 1],
                                                      self.bend_length[len(self.total_length) - 1],
                                                      self.specification[len(self.total_length) - 1],
                                                      self.remain_length[len(self.total_length) - 1],
                                                      self.remain_num_list[len(self.total_length) - 1]))
                        self.treeview1.update()

                    fo0 = open(self.filename0, "w")
                    fo0.truncate() #清空Excel数据
                    fo0.close
                    fo1 = open(self.filename1, "w")
                    fo1.truncate()
                    fo1.close
                    fo2 = open(self.filename2, "w")
                    fo2.truncate()
                    fo2.close

                    with open(self.filename0, 'a', errors='ignore', newline='') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerows(self.data0)

                    with open(self.filename1, 'a', errors='ignore', newline='') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerows(self.data1)

                    with open(self.filename2, 'a', errors='ignore', newline='') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerows(self.data2)

                    for _ in map(self.treeview2.delete, self.treeview2.get_children("")):
                        pass
                    for p in range(min(len(self.warehouse_no), len(self.warehouse_length))):  # 写入数据
                        self.treeview2.insert('', p, values=(self.warehouse_no[p], self.warehouse_length[p]))
                    self.scr.config(state=NORMAL)  # 将计算数据显示在文本框中
                    self.scr.insert(INSERT,
                                    '********************************************************************************\n\n' +
                                    f"第{self.i + 1}根间隔条，总长{self.total_length[self.i]}mm，"
                                    f"全边长{self.width_length[self.i]}mm，"
                                    f"折边长{self.bend_length[self.i]}mm，"
                                    f"余长{self.remain_length[self.i]}mm\n第{self.i + 2}根间隔条，"
                                    f"总长{self.total_length[self.i + 1]}mm，"
                                    f"全边长{self.width_length[self.i + 1]}mm，"
                                    f"折边长{self.bend_length[self.i + 1]}mm，余长{self.remain_length[self.i + 1]}mm\n\n" +
                                    '********************************************************************************\n')
                    self.scr.see(END)
                    self.scr.config(state=DISABLED)

                    self.logger.info('***********************************************************************************'
                                     '***********************************')
                    self.logger.info(f'当前窗框型号：宽度={self.width[self.j]}mm，长度={self.length[self.j]}mm，'
                                     f'剩余数量={self.number[self.j]}根，'f'状态={self.state[self.j]}')
                    self.logger.info(f'当前计算值：第{self.i + 1}根间隔条，总长={self.total_length[self.i]}mm，'
                                     f'全边长={self.width_length[self.i]}mm，'f'折边长={self.bend_length[self.i]}mm，'
                                     f'余长={self.remain_length[self.i]}mm')
                    self.logger.info(f'当前计算值：第{self.i + 2}根间隔条，总长={self.total_length[self.i + 1]}mm，'
                                     f'全边长={self.width_length[self.i + 1]}mm，'f'折边长={self.bend_length[self.i + 1]}mm，'
                                     f'余长={self.remain_length[self.i + 1]}mm)')
                    self.logger.info(f'当前缓存仓存料：'
                                     f'1#：{self.warehouse_length[0]}mm,'
                                     f'2#：{self.warehouse_length[1]}mm,'
                                     f'3#：{self.warehouse_length[2]}mm,'
                                     f'4#：{self.warehouse_length[3]}mm,'
                                     f'5#：{self.warehouse_length[4]}mm,'
                                     f'6#：{self.warehouse_length[5]}mm,'
                                     f'7#：{self.warehouse_length[6]}mm,'
                                     f'8#：{self.warehouse_length[7]}mm,'
                                     f'9#：{self.warehouse_length[8]}mm,'
                                     f'10#：{self.warehouse_length[9]}mm,'
                                     f'11#：{self.warehouse_length[10]}mm,'
                                     f'12#：{self.warehouse_length[11]}mm,'
                                     f'13#：{self.warehouse_length[12]}mm,')
                    self.logger.info('***********************************************************************************'
                                     '***********************************\n')
                    self.i += 2
                    self.n = self.remain_num[self.j]
            else:
                if self.j < len(self.number)-1:
                    self.j += 1
                    self.calculated_value()
                else:
                    self.calculated_confirm = False
                    self.n -= 1
                    self.manual_Rad['state'] = 'normal'
                    self.auto_Rad['state'] = 'normal'
                    self.offline_Rad['state'] = 'normal'
                    tkinter.messagebox.showinfo(title='完成提示', message='计算完成，请添加新的窗框型号和数量！！')
            self.i_list.append(self.i)
            self.j_list.append(self.j)
            self.k_list.append(self.k)
            fo3 = open(self.filename3, "w")
            fo3.truncate()
            fo3.close
            with open(self.filename3, 'a', errors='ignore', newline='') as f:
                f_csv = csv.writer(f)
                f_csv.writerows(self.data3)
            self.treeview1.yview_moveto(1.0)

    # 清空表格和文本框数据
    def clear_table(self):
        global i, j, k
        self.k += len(self.width)
        #print('k=', self.k)
        self.frame_No.clear()
        self.total_length.clear()
        self.width_length.clear()
        self.bend_length.clear()
        self.specification.clear()
        self.remain_length.clear()
        self.remain_num_list.clear()
        self.produceNo_list.clear()
        self.produceNo = 0
        self.width.clear()
        self.length.clear()
        self.number.clear()
        self.state.clear()
        self.remain_num.clear()
        self.i_list.clear()
        self.j_list.clear()
        self.k_list.clear()
        self.data0 = [self.produceNo_list, self.width, self.length, self.number, self.state]
        self.data1 = [self.frame_No,self.total_length, self.width_length, self.bend_length, self.specification,
                      self.remain_length, self.remain_num_list]
        self.data2 = [self.warehouse_no, self.warehouse_length]
        self.data3 = [self.i_list, self.j_list, self.k_list, self.remain_num]
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

        fo0 = open(self.filename0, "w")
        fo0.truncate()  # 清空csv文件数据
        fo0.close
        fo1 = open(self.filename1, "w")
        fo1.truncate()
        fo1.close
        fo2 = open(self.filename2, "w")
        fo2.truncate()
        fo2.close
        fo3 = open(self.filename3, "w")
        fo3.truncate()
        fo3.close

    # 读取csv表格内的数据
    def read_table(self):
        try:
            # 通过with语句读取，以列表类型读取
            with open(self.filename0, 'r') as fp:  # 使用列表推导式，将读取到的数据装进列表
                data_list0 = [i for i in csv.reader(fp)]  # csv.reader 读取到的数据是list类型，
            self.produceNo_list = [int(a) for a in data_list0[-5]]  # 将data_list0列表内的produceNo装进列表
            self.width = [int(a) for a in data_list0[-4]]  # 将data_list0列表内的width装进列表
            self.length = [int(a) for a in data_list0[-3]]  # 将data_list0列表内的length装进列表
            self.number = [int(a) for a in data_list0[-2]]  # 将data_list0列表内的number装进列表
            self.state = data_list0[-1]  # 将data_list0列表内的state装进列表
            self.produceNo = self.produceNo_list[-1]
            for _ in map(self.treeview.delete, self.treeview.get_children("")):  # 清空表格
                pass
            for p in range(len(self.width)):  # 往表格中写入新数据
                self.treeview.insert('', p, values=(self.produceNo_list[p], self.width[p], self.length[p],
                                                    self.number[p], self.state[p]))
            # 通过with语句读取，以列表类型读取
            with open(self.filename1, 'r') as fp:  # 使用列表推导式，将读取到的数据装进列表
                data_list1 = [i for i in csv.reader(fp)]  # csv.reader 读取到的数据是list类型
            self.frame_No = [int(a) for a in data_list1[-7]]
            self.total_length = [int(a) for a in data_list1[-6]]
            self.width_length = [int(a) for a in data_list1[-5]]
            self.bend_length = [int(a) for a in data_list1[-4]]
            self.specification = [int(a) for a in data_list1[-3]]
            self.remain_length = [int(a) for a in data_list1[-2]]
            self.remain_num_list = [int(a) for a in data_list1[-1]]

            for _ in map(self.treeview1.delete, self.treeview1.get_children("")):
                pass
            for n in range(len(self.total_length)):  # 写入数据
                self.treeview1.insert('', n, values=(
                self.frame_No[n], self.total_length[n], self.width_length[n], self.bend_length[n],
                self.specification[n], self.remain_length[n], self.remain_num_list[n]))
            # 通过with语句读取，以列表类型读取
            with open(self.filename2, 'r') as fp:  # 使用列表推导式，将读取到的数据装进列表
                data_list2 = [i for i in csv.reader(fp)]  # csv.reader 读取到的数据是list类型
            self.warehouse_no = data_list2[-2]
            self.warehouse_length = [int(a) for a in data_list2[-1]]
            for _ in map(self.treeview2.delete, self.treeview2.get_children("")):
                pass
            for n in range(len(self.warehouse_no)):  # 写入数据
                self.treeview2.insert('', n, values=(self.warehouse_no[n], self.warehouse_length[n]))
            # 通过with语句读取，以列表类型读取
            with open(self.filename3, 'r') as fp:  # 使用列表推导式，将读取到的数据装进列表
                data_list3 = [b for b in csv.reader(fp)]  # csv.reader 读取到的数据是list类型
            self.i = int(data_list3[-4][-1])
            self.j = int(data_list3[-3][-1])
            # self.k = int(data_list3[-2][-1])
            self.i_list = [int(a) for a in data_list3[-4]]
            self.j_list = [int(a) for a in data_list3[-3]]
            self.k_list = [int(a) for a in data_list3[-2]]
            self.remain_num = [int(a) for a in data_list3[-1]]
            self.data0 = [self.produceNo_list, self.width, self.length, self.number, self.state]
            self.data1 = [self.frame_No, self.total_length, self.width_length, self.bend_length, self.specification,
                          self.remain_length, self.remain_num_list]
            self.data2 = [self.warehouse_no, self.warehouse_length]
            self.data3 = [self.i_list, self.j_list, self.k_list, self.remain_num]
        except Exception as e:
            tkinter.messagebox.showerror(title='错误', message=str(e))

    # 软件退出
    def _quit(self):
        if tkinter.messagebox.askyesno("操作确认", "确认软件退出吗!"):
            self.root.quit()
            self.root.destroy()
            exit()

    # 输入数据转换为Int类型并返回数据
    def convert(self, entrydata):
        data = entrydata.get()
        try:
            data = int(data)
        except Exception as e:
            tkinter.messagebox.showerror(title='错误', message=str(e))
        return data

    # 读取comboxlist内的数据并返回数据
    def getdata(self, comboxlist, comvalue):
        comvalue.set(comboxlist.get())
        data = comboxlist.get()
        return data

    # 获取电脑可用串口列表
    def Port_list(self):
        SerialName = []
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            tkinter.messagebox.showerror(title="错误", message="未发现电脑存在可用串口！！")
        else:
            for plist_children in plist:
                port_info = list(plist_children)
                SerialName.append(port_info[0])
        return SerialName

    # 设置Modbus通讯串口参数并打开串口
    def mb_port_open(self):
        self.mbComPort = self.getdata(self.comboxlist_port, self.comvalue_port)
        self.baudrate = self.getdata(self.comboxlist_baud, self.comvalue_baud)
        self.databit = int(self.getdata(self.comboxlist_databit, self.comvalue_databit))
        self.parity = self.getdata(self.comboxlist_parity, self.comvalue_parity)
        self.stopbit = int(self.getdata(self.comboxlist_stopbit, self.comvalue_stopbit))
        self.mbTimeout = self.convert(self.entrydata_timeout)  # ms
        self.mbId = self.convert(self.entrydata_id)
        try:
            self.mb_port = serial.Serial(port=self.mbComPort, baudrate=self.baudrate, bytesize=self.databit,
                                         parity=self.parity, stopbits=self.stopbit)
            self.master = modbus_rtu.RtuMaster(self.mb_port)
            self.master.set_timeout(self.mbTimeout / 1000.0)
            self.master.set_verbose(True)  # 关闭debug的log输出
            self.com_state = self.mb_port.is_open
            self.com_open["state"] = "disabled"
            self.com_state_label["text"] = "软件与PLC连接成功！"
            self.com_state_label["foreground"] = 'green'
            self.com_parameter = [self.mbComPort, self.baudrate, self.databit, self.parity, self.stopbit]
            self.t1 = threading.Thread(target=self.read_coils())
            self.t2 = threading.Thread(target=self.read_holding_registers())
            self.t1.start()
            self.t2.start()
        except Exception as e:
            tkinter.messagebox.showerror(title='错误', message='Modbus通讯错误:' + str(e))
        self.com_close["state"] = "normal"

    # 通过Modbus写入寄存器模块往PLC写书数据
    def write_multiple_registers(self):
        if bool(self.total_length and self.width_length and self.bend_length )==False:
            tkinter.messagebox.showwarning(title='操作提示', message='未发现计算数据不能进行数据传送！！')
        elif self.Init == 0:
            tkinter.messagebox.showwarning(title='操作提示', message='请等待设备初始化完成再开始计算！')
        elif self.cut_achieve == 0:
            tkinter.messagebox.showwarning(title="提示", message="裁切设备正在工作，暂不允许传送数据！")
        else:
            try:
                data_cal = [self.frame_No[self.i-2], self.total_length[self.i-2], self.width_length[self.i-2],
                            self.bend_length[self.i-2], self.specification[self.i-2], self.remain_length[self.i-2],
                            self.remain_num_list[self.i-2],
                            self.frame_No[self.i-2], self.total_length[self.i - 1], self.width_length[self.i - 1],
                            self.bend_length[self.i - 1], self.specification[self.i - 1], self.remain_length[self.i - 1],
                            self.remain_num_list[self.i - 1]]
                self.logger.info("<--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <-->")
                self.logger.info("connected")
                self.logger.info(self.master.execute(self.mbId, cst.WRITE_MULTIPLE_REGISTERS, 4000,
                                                     output_value=data_cal))
                self.logger.info("<--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <--> <-->\n")
                self.master.execute(1, cst.WRITE_SINGLE_COIL, 3001, output_value=0)
                self.cut_achieve = 0
                if self.radSel == 0:
                    self.cal_start["state"] = "normal"
                    self.send_data["state"] = "disabled"
            except Exception as e:
                logging.error(str(e))
                tkinter.messagebox.showerror(title='错误', message='Modbus通讯错误:' + str(e))

    read_states = []
    # 通过Modbus读取线圈模块读取PLC线圈信号
    def read_coils(self):
        try:
            self.logger.info("--> --> --> --> --> --> --> --> --> --> --> --> --> --> --> --> --> --> -->")
            self.logger.info("connected")
            self.read_states = self.master.execute(self.mbId, cst.READ_COILS, 3000, 10)
            self.Init = self.read_states[0]  # 读取设备初始化状态
            self.cut_achieve = self.read_states[1]  # 读取裁切设备当前运行状态
            if self.Init == 1:
                self.Init_label["text"] = "设备完成初始化！"
                self.Init_label["foreground"] = "green"
            else:
                self.Init_label["text"] = "设备未完成初始化！"
                self.Init_label["foreground"] = "red"
            if self.cut_achieve == 1:
                self.cut_achieve_label["text"] = "裁切就绪，请传送数据！"
                self.cut_achieve_label["foreground"] = "green"
            else:
                self.cut_achieve_label["text"] = "裁切进行中，暂不传送数据！"
                self.cut_achieve_label["foreground"] = "red"
            self.logger.info(self.read_states)
            self.logger.info("<-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <--\n")
            # 裁切设备就绪并且需生产窗框数量>0，将数据发送到PLC
            if (self.cut_achieve == 1) and (self.n >= 0) and (self.radSel == 1):
                self.write_multiple_registers()
                self.calculated_value()
            elif self.n < 0:
                self.cal_start['state'] = 'normal'  # 生产窗框数量<=0时停止自动计算和发送数据
            self.read_coils_job = self.root.after(500, self.read_coils)
        except Exception as e:
            logging.error(str(e))
            tkinter.messagebox.showerror(title='错误', message='Modbus通讯错误:' + str(e))

    read_data = []
    # 通过Modbus读取寄存器模块读取PLC数据
    def read_holding_registers(self):
        try:
            self.logger.info("--> --> --> --> --> --> --> --> --> --> --> --> --> --> --> --> --> -->")
            self.logger.info("connected")
            self.read_data = self.master.execute(self.mbId, cst.READ_HOLDING_REGISTERS, 4000, 20)
            self.logger.info(self.read_data)
            self.logger.info("<-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- <--\n")
            self.read_holding_registers_job = self.root.after(500, self.read_holding_registers)
        except Exception as e:
            logging.error(str(e))
            tkinter.messagebox.showerror(title='错误', message='Modbus通讯错误:' + str(e))

    # 关闭Modbu通讯串口
    def mb_port_close(self):
        try:
            self.mb_port.close()
            self.master._do_close()
            self.com_state = self.mb_port.is_open
            self.com_close["state"] = "disabled"
            self.com_state_label["text"] = "软件与PLC未连接！"
            self.com_state_label["foreground"] = 'red'
            self.root.after_cancel(self.read_coils_job)
            self.read_coils_job = None
            self.root.after_cancel(self.read_holding_registers_job)
            self.read_holding_registers_job = None
            self.t1.join()
            self.t2.join()
        except Exception as e:
            tkinter.messagebox.showerror(title='错误', message='Modbus通讯错误:' + str(e))
        self.com_open["state"] = "normal"

    com_parameter = ["COM-", 19200, 8, "E", 1]
    # Modbus通讯串口参数设置窗口
    def com_config_win(self):
        if self.com_config_win_run == False:
            self.com_win = Toplevel()
            self.com_win.title('串口参数设置窗口')
            self.root.update()
            self.com_win.geometry(f"+{self.root.winfo_x()+20}+{self.root.winfo_y()+80}")
            self.com_win.resizable(0, 0)
            self.com_win.wm_attributes('-topmost', 1)  # 窗口置顶
            self.serial_name = self.Port_list()  # 获取电脑可用串口列表

            self.com_frame = ttk.LabelFrame(self.com_win, text='串口参数设置')
            self.com_frame.grid(column=0, row=0, padx=8, pady=4)
            self.label_port = ttk.Label(self.com_frame, text='端口号：')
            self.label_port.grid(row=0, column=0)
            self.comvalue_port = StringVar()
            self.comboxlist_port = ttk.Combobox(self.com_frame, width=6, textvariable=self.comvalue_port)
            self.comboxlist_port["values"] = self.serial_name
            self.comboxlist_port.set(self.com_parameter[0])
            self.comboxlist_port.grid(row=0, column=1, padx=4, pady=4)
            self.label_baud = ttk.Label(self.com_frame, text='波特率：')
            self.label_baud.grid(row=1, column=0)
            self.comvalue_baud = IntVar()
            self.comboxlist_baud = ttk.Combobox(self.com_frame, width=6, textvariable=self.comvalue_baud)
            self.comboxlist_baud["values"] = (2400, 4800, 9600, 19200, 38400)
            self.comboxlist_baud.set(self.com_parameter[1])
            self.comboxlist_baud.grid(row=1, column=1, padx=4, pady=4)
            self.label_databit = ttk.Label(self.com_frame, text='数据位：')
            self.label_databit.grid(row=2, column=0, padx=4, pady=4)
            self.comvalue_databit = IntVar()
            self.comboxlist_databit = ttk.Combobox(self.com_frame, width=6, textvariable=self.comvalue_databit)
            self.comboxlist_databit["values"] = (5, 6, 7, 8)
            self.comboxlist_databit.set(self.com_parameter[2])
            self.comboxlist_databit.grid(row=2, column=1)
            self.label_parity = ttk.Label(self.com_frame, text='校验位')
            self.label_parity.grid(row=3, column=0, padx=4, pady=4)
            self.comvalue_parity = StringVar()
            self.comboxlist_parity = ttk.Combobox(self.com_frame, width=6, textvariable=self.comvalue_parity)
            self.comboxlist_parity["values"] = ("N", "E", "O")
            self.comboxlist_parity.set(self.com_parameter[3])
            self.comboxlist_parity.grid(row=3, column=1, padx=4, pady=4)
            self.label_stopbit = ttk.Label(self.com_frame, text='停止位：')
            self.label_stopbit.grid(row=0, column=2, padx=4, pady=4)
            self.comvalue_stopbit = IntVar()
            self.comboxlist_stopbit = ttk.Combobox(self.com_frame, width=6, textvariable=self.comvalue_stopbit)
            self.comboxlist_stopbit["values"] = (1, 2)
            self.comboxlist_stopbit.set(self.com_parameter[4])
            self.comboxlist_stopbit.grid(row=0, column=3, padx=4, pady=4)
            self.label_timeout = ttk.Label(self.com_frame, text='回复超时(ms)：')
            self.label_timeout.grid(row=1, column=2, padx=4, pady=4)
            self.entrydata_timeout = ttk.Entry(self.com_frame, width=9)
            self.entrydata_timeout.insert(0, '100')
            self.entrydata_timeout.grid(row=1, column=3, padx=4, pady=4)
            self.label_id = ttk.Label(self.com_frame, text='站号地址：')
            self.label_id.grid(row=2, column=2, padx=4, pady=4)
            self.entrydata_id = ttk.Entry(self.com_frame, width=9)
            self.entrydata_id.insert(0, '1')
            self.entrydata_id.grid(row=2, column=3, padx=4, pady=4)
            self.com_open = ttk.Button(self.com_frame, text='打开串口', command=self.mb_port_open)
            self.com_open.grid(row=3, column=2, padx=4, pady=4)
            self.com_close = ttk.Button(self.com_frame, text='关闭串口', command=self.mb_port_close)
            self.com_close.grid(row=3, column=3, padx=4, pady=4)
            if self.com_state:
                self.com_open["state"] = "disabled"
                self.com_close["state"] = "normal"
            else:
                self.com_open["state"] = "normal"
                self.com_close["state"] = "disabled"
            self.com_config_win_run = True
        else:
            self.com_config_win_run = False
            self.com_win.destroy()
            self.com_config_win()

    # 通讯数据监控窗口
    def com_datamonitor_win(self):
        if self.com_datamonitor_win_run == False:
            if self.com_state:
                self.datamonitor_win = Toplevel()
                self.datamonitor_win.title('通讯数据监控窗口')
                self.root.update()
                self.datamonitor_win.geometry(f"+{self.root.winfo_x()+20}+{self.root.winfo_y()+260}")
                self.datamonitor_win.resizable(0, 0)
                self.datamonitor_win.wm_attributes('-topmost', 1)
                self.read_states_frame = ttk.LabelFrame(self.datamonitor_win, text='线圈状态监控', height=120, width=150)
                self.read_states_frame.grid(column=0, row=0, padx=8, pady=4)
                self.read_data_frame = ttk.LabelFrame(self.datamonitor_win, text='寄存器数据监控', height=120, width=350)
                self.read_data_frame.grid(column=1, row=0, padx=8, pady=4)
                #显示线圈通讯数据
                self.read_state_num_0 = ttk.Label(self.read_states_frame, text='Bit0')
                self.read_state_label_0 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[0]))
                self.read_state_num_0.grid(column=0, row=0, padx=2, pady=4)
                self.read_state_label_0.grid(column=1, row=0, padx=2, pady=4)
                self.read_state_num_1 = ttk.Label(self.read_states_frame, text='Bit1')
                self.read_state_label_1 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[1]))
                self.read_state_num_1.grid(column=0, row=1, padx=2, pady=4)
                self.read_state_label_1.grid(column=1, row=1, padx=2, pady=4)
                self.read_state_num_2 = ttk.Label(self.read_states_frame, text='Bit2')
                self.read_state_label_2 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[2]))
                self.read_state_num_2.grid(column=0, row=2, padx=2, pady=4)
                self.read_state_label_2.grid(column=1, row=2, padx=2, pady=4)
                self.read_state_num_3 = ttk.Label(self.read_states_frame, text='Bit3')
                self.read_state_label_3 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[3]))
                self.read_state_num_3.grid(column=0, row=3, padx=2, pady=4)
                self.read_state_label_3.grid(column=1, row=3, padx=2, pady=4)
                self.read_state_num_4 = ttk.Label(self.read_states_frame, text='Bit4')
                self.read_state_label_4 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[4]))
                self.read_state_num_4.grid(column=0, row=4, padx=2, pady=4)
                self.read_state_label_4.grid(column=1, row=4, padx=2, pady=4)
                self.read_state_num_5 = ttk.Label(self.read_states_frame, text='Bit5')
                self.read_state_label_5 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[5]))
                self.read_state_num_5.grid(column=2, row=0, padx=2, pady=4)
                self.read_state_label_5.grid(column=3, row=0, padx=2, pady=4)
                self.read_state_num_6 = ttk.Label(self.read_states_frame, text='Bit6')
                self.read_state_label_6 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[6]))
                self.read_state_num_6.grid(column=2, row=1, padx=2, pady=4)
                self.read_state_label_6.grid(column=3, row=1, padx=2, pady=4)
                self.read_state_num_7 = ttk.Label(self.read_states_frame, text='Bit7')
                self.read_state_label_7 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[7]))
                self.read_state_num_7.grid(column=2, row=2, padx=2, pady=4)
                self.read_state_label_7.grid(column=3, row=2, padx=2, pady=4)
                self.read_state_num_8 = ttk.Label(self.read_states_frame, text='Bit8')
                self.read_state_label_8 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[8]))
                self.read_state_num_8.grid(column=2, row=3, padx=2, pady=4)
                self.read_state_label_8.grid(column=3, row=3, padx=2, pady=4)
                self.read_state_num_9 = ttk.Label(self.read_states_frame, text='Bit9')
                self.read_state_label_9 = ttk.Label(self.read_states_frame, relief="sunken",
                                                    text=str(self.read_states[9]))
                self.read_state_num_9.grid(column=2, row=4, padx=2, pady=4)
                self.read_state_label_9.grid(column=3, row=4, padx=2, pady=4)
                #显示寄存器通讯数据
                self.read_data_num_0 = ttk.Label(self.read_data_frame, text='Data0')
                self.read_data_label_0 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[0]))
                self.read_data_num_0.grid(column=0, row=0, padx=2, pady=4)
                self.read_data_label_0.grid(column=1, row=0, padx=2, pady=4)
                self.read_data_num_1 = ttk.Label(self.read_data_frame, text='Data1')
                self.read_data_label_1 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[1]))
                self.read_data_num_1.grid(column=0, row=1, padx=2, pady=4)
                self.read_data_label_1.grid(column=1, row=1, padx=2, pady=4)
                self.read_data_num_2 = ttk.Label(self.read_data_frame, text='Data2')
                self.read_data_label_2 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[2]))
                self.read_data_num_2.grid(column=0, row=2, padx=2, pady=4)
                self.read_data_label_2.grid(column=1, row=2, padx=2, pady=4)
                self.read_data_num_3 = ttk.Label(self.read_data_frame, text='Data3')
                self.read_data_label_3 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[3]))
                self.read_data_num_3.grid(column=0, row=3, padx=2, pady=4)
                self.read_data_label_3.grid(column=1, row=3, padx=2, pady=4)
                self.read_data_num_4 = ttk.Label(self.read_data_frame, text='Data4')
                self.read_data_label_4 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[4]))
                self.read_data_num_4.grid(column=0, row=4, padx=2, pady=4)
                self.read_data_label_4.grid(column=1, row=4, padx=2, pady=4)
                self.read_data_num_5 = ttk.Label(self.read_data_frame, text='Data5')
                self.read_data_label_5 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[5]))
                self.read_data_num_5.grid(column=2, row=0, padx=2, pady=4)
                self.read_data_label_5.grid(column=3, row=0, padx=2, pady=4)
                self.read_data_num_6 = ttk.Label(self.read_data_frame, text='Data6')
                self.read_data_label_6 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[6]))
                self.read_data_num_6.grid(column=2, row=1, padx=2, pady=4)
                self.read_data_label_6.grid(column=3, row=1, padx=2, pady=4)
                self.read_data_num_7 = ttk.Label(self.read_data_frame, text='Data7')
                self.read_data_label_7 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[7]))
                self.read_data_num_7.grid(column=2, row=2, padx=2, pady=4)
                self.read_data_label_7.grid(column=3, row=2, padx=2, pady=4)
                self.read_data_num_8 = ttk.Label(self.read_data_frame, text='Data8')
                self.read_data_label_8 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[8]))
                self.read_data_num_8.grid(column=2, row=3, padx=2, pady=4)
                self.read_data_label_8.grid(column=3, row=3, padx=2, pady=4)
                self.read_data_num_9 = ttk.Label(self.read_data_frame, text='Data9')
                self.read_data_label_9 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[9]))
                self.read_data_num_9.grid(column=2, row=4, padx=2, pady=4)
                self.read_data_label_9.grid(column=3, row=4, padx=2, pady=4)
                self.read_data_num_10 = ttk.Label(self.read_data_frame, text='Data10')
                self.read_data_label_10 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[10]))
                self.read_data_num_10.grid(column=4, row=0, padx=2, pady=4)
                self.read_data_label_10.grid(column=5, row=0, padx=2, pady=4)
                self.read_data_num_11 = ttk.Label(self.read_data_frame, text='Data11')
                self.read_data_label_11 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[11]))
                self.read_data_num_11.grid(column=4, row=1, padx=2, pady=4)
                self.read_data_label_11.grid(column=5, row=1, padx=2, pady=4)
                self.read_data_num_12 = ttk.Label(self.read_data_frame, text='Data12')
                self.read_data_label_12 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[12]))
                self.read_data_num_12.grid(column=4, row=2, padx=2, pady=4)
                self.read_data_label_12.grid(column=5, row=2, padx=2, pady=4)
                self.read_data_num_13 = ttk.Label(self.read_data_frame, text='Data13')
                self.read_data_label_13 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[13]))
                self.read_data_num_13.grid(column=4, row=3, padx=2, pady=4)
                self.read_data_label_13.grid(column=5, row=3, padx=2, pady=4)
                self.read_data_num_14 = ttk.Label(self.read_data_frame, text='Data14')
                self.read_data_label_14 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[14]))
                self.read_data_num_14.grid(column=4, row=4, padx=2, pady=4)
                self.read_data_label_14.grid(column=5, row=4, padx=2, pady=4)
                self.read_data_num_15 = ttk.Label(self.read_data_frame, text='Data15')
                self.read_data_label_15 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[15]))
                self.read_data_num_15.grid(column=6, row=0, padx=2, pady=4)
                self.read_data_label_15.grid(column=7, row=0, padx=2, pady=4)
                self.read_data_num_16 = ttk.Label(self.read_data_frame, text='Data16')
                self.read_data_label_16 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[16]))
                self.read_data_num_16.grid(column=6, row=1, padx=2, pady=4)
                self.read_data_label_16.grid(column=7, row=1, padx=2, pady=4)
                self.read_data_num_17 = ttk.Label(self.read_data_frame, text='Data17')
                self.read_data_label_17 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[17]))
                self.read_data_num_17.grid(column=6, row=2, padx=2, pady=4)
                self.read_data_label_17.grid(column=7, row=2, padx=2, pady=4)
                self.read_data_num_18 = ttk.Label(self.read_data_frame, text='Data18')
                self.read_data_label_18 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[18]))
                self.read_data_num_18.grid(column=6, row=3, padx=2, pady=4)
                self.read_data_label_18.grid(column=7, row=3, padx=2, pady=4)
                self.read_data_num_19 = ttk.Label(self.read_data_frame, text='Data19')
                self.read_data_label_19 = ttk.Label(self.read_data_frame, width=6, relief="sunken",
                                                   text=str(self.read_data[19]))
                self.read_data_num_19.grid(column=6, row=4, padx=2, pady=4)
                self.read_data_label_19.grid(column=7, row=4, padx=2, pady=4)

                self.t4 = threading.Thread(target=self.com_data_update())
                self.t4.start()
                self.com_datamonitor_win_run = True
            else:
                tkinter.messagebox.showerror(title='错误', message='通讯串口未打开，无法读取数据！！')
        else:
            self.com_datamonitor_win_run = False
            self.datamonitor_win.destroy()
            self.com_datamonitor_win()

    # 通讯数据监控窗口中数据更新
    def com_data_update(self):
        self.read_state_label_0['text'] = str(self.read_states[0])
        if self.read_states[0] == 1:
            self.read_state_label_0['background'] = "green"
        else:
            self.read_state_label_0['background'] = "red"
        self.read_state_label_1['text'] = str(self.read_states[1])
        if self.read_states[1] == 1:
            self.read_state_label_1['background'] = "green"
        else:
            self.read_state_label_1['background'] = "red"
        self.read_state_label_2['text'] = str(self.read_states[2])
        if self.read_states[2] == 1:
            self.read_state_label_2['background'] = "green"
        else:
            self.read_state_label_2['background'] = "red"
        self.read_state_label_3['text'] = str(self.read_states[3])
        if self.read_states[3] == 1:
            self.read_state_label_3['background'] = "green"
        else:
            self.read_state_label_3['background'] = "red"
        self.read_state_label_4['text'] = str(self.read_states[4])
        if self.read_states[4] == 1:
            self.read_state_label_4['background'] = "green"
        else:
            self.read_state_label_4['background'] = "red"
        self.read_state_label_5['text'] = str(self.read_states[5])
        if self.read_states[5] == 1:
            self.read_state_label_5['background'] = "green"
        else:
            self.read_state_label_5['background'] = "red"
        self.read_state_label_6['text'] = str(self.read_states[6])
        if self.read_states[6] == 1:
            self.read_state_label_6['background'] = "green"
        else:
            self.read_state_label_6['background'] = "red"
        self.read_state_label_7['text'] = str(self.read_states[7])
        if self.read_states[7] == 1:
            self.read_state_label_7['background'] = "green"
        else:
            self.read_state_label_7['background'] = "red"
        self.read_state_label_8['text'] = str(self.read_states[8])
        if self.read_states[8] == 1:
            self.read_state_label_8['background'] = "green"
        else:
            self.read_state_label_8['background'] = "red"
        self.read_state_label_9['text'] = str(self.read_states[9])
        if self.read_states[9] == 1:
            self.read_state_label_9['background'] = "green"
        else:
            self.read_state_label_9['background'] = "red"

        self.read_data_label_0['text'] = str(self.read_data[0])
        self.read_data_label_1['text'] = str(self.read_data[1])
        self.read_data_label_2['text'] = str(self.read_data[2])
        self.read_data_label_3['text'] = str(self.read_data[3])
        self.read_data_label_4['text'] = str(self.read_data[4])
        self.read_data_label_5['text'] = str(self.read_data[5])
        self.read_data_label_6['text'] = str(self.read_data[6])
        self.read_data_label_7['text'] = str(self.read_data[7])
        self.read_data_label_8['text'] = str(self.read_data[8])
        self.read_data_label_9['text'] = str(self.read_data[9])
        self.read_data_label_10['text'] = str(self.read_data[10])
        self.read_data_label_11['text'] = str(self.read_data[11])
        self.read_data_label_12['text'] = str(self.read_data[12])
        self.read_data_label_13['text'] = str(self.read_data[13])
        self.read_data_label_14['text'] = str(self.read_data[14])
        self.read_data_label_15['text'] = str(self.read_data[15])
        self.read_data_label_16['text'] = str(self.read_data[16])
        self.read_data_label_17['text'] = str(self.read_data[17])
        self.read_data_label_18['text'] = str(self.read_data[18])
        self.read_data_label_19['text'] = str(self.read_data[19])

        self.com_data_update_job = self.datamonitor_win.after(500, self.com_data_update)

    # RadioButton选择
    def rad_call(self):
        self.radSel = self.radVar.get()
        if self.radSel == 0:
            self.cal_start['state'] = 'normal'
            self.send_data['state'] = 'normal'
        if self.radSel == 1:
            self.cal_start['state'] = 'normal'
            self.send_data['state'] = 'disabled'
        if self.radSel == 2:
            self.cal_start['state'] = 'normal'
            self.send_data['state'] = 'disabled'

    # 使用Turtle绘制组框示意图
    def draw_sketch(self):
        theScreen = turtle.TurtleScreen(self.sketch_canvas)  # Turtle嵌套进Canvas
        theScreen.bgcolor("DarkSlateGray")
        path = turtle.RawTurtle(theScreen)
        frame_num = int(self.frameval)*2  # 根据窗框编号获取间隔条编号
        # 开始绘制窗框
        path.speed(0)
        path.color("Red")
        path.pensize(4)
        path.up()
        path.goto(self.width_length[frame_num-2]/-10, 150)
        path.down()
        path.speed(1)
        path.setheading(270)
        path.forward(self.bend_length[frame_num-2]/5)
        path.up()
        path.goto(self.width_length[frame_num - 2] / -10, 150)
        path.down()
        path.setheading(0)
        path.forward(self.width_length[frame_num-2]/5)
        path.right(90)
        path.forward(self.bend_length[frame_num-2]/5)
        path.speed(0)
        path.up()
        path.goto(self.width_length[frame_num-2]/-10, 150)
        path.down()
        path.pensize(0.5)
        path.color("GhostWhite")
        path.setheading(90)
        path.forward(30/3)
        path.backward(15/3)
        path.right(60)
        path.forward(15/3)
        path.backward(15/3)
        path.right(60)
        path.forward(15/3)
        path.backward(15/3)
        path.left(30)
        path.forward(self.width_length[frame_num-2]/5)
        path.right(30)
        path.backward(15/3)
        path.forward(15/3)
        path.left(60)
        path.backward(15/3)
        path.forward(15/3)
        path.setheading(90)
        path.forward(15/3)
        path.backward(30/3)
        path.up()
        path.goto(0, 155)
        path.color("GhostWhite")
        path.write(f"全边：{self.width_length[frame_num-2]}mm", align='center', font=('Arial', 8, 'normal'))
        path.goto(self.width_length[frame_num-2]/-10, 150)
        path.down()
        path.setheading(180)
        path.color("GhostWhite")
        path.forward(15/3)
        path.left(60)
        path.forward(15/3)
        path.backward(15/3)
        path.left(60)
        path.forward(15/3)
        path.backward(15/3)
        path.right(120)
        path.forward(15/3)
        path.backward(15/3)
        path.left(90)
        path.forward(self.bend_length[frame_num-2]/5)
        path.left(30)
        path.backward(15/3)
        path.forward(15/3)
        path.right(60)
        path.backward(15/3)
        path.forward(15/3)
        path.setheading(180)
        path.forward(15/3)
        path.backward(30/3)
        path.up()
        path.goto((self.width_length[frame_num-2]/-10)+5, 150-self.length[self.j]/5+self.bend_length[frame_num-1]/5
                  + self.bend_length[frame_num-2]/10-8)
        path.color("GhostWhite")
        path.write(f"折边：{self.bend_length[frame_num-2]}mm", align='left', font=('Arial', 8, 'normal'))

        path.goto(self.width_length[frame_num-1]/10, 150-self.bend_length[frame_num-2]/5)
        path.down()
        path.pensize(4)
        path.speed(1)
        path.color("MediumBlue")
        path.setheading(270)
        path.forward(self.bend_length[frame_num-1]/5)
        path.right(90)
        path.forward(self.width_length[frame_num-1]/5)
        path.right(90)
        path.forward(self.bend_length[frame_num-1]/5)
        path.setheading(180)
        path.pensize(0.5)
        path.speed(0)
        path.color("GhostWhite")
        path.forward(15/3)
        path.left(60)
        path.forward(15/3)
        path.backward(15/3)
        path.left(60)
        path.forward(15/3)
        path.backward(15/3)
        path.right(120)
        path.forward(15/3)
        path.backward(15/3)
        path.left(90)
        path.forward(self.bend_length[frame_num-1]/5)
        path.left(30)
        path.backward(15/3)
        path.forward(15/3)
        path.right(60)
        path.backward(15/3)
        path.forward(15/3)
        path.setheading(180)
        path.forward(15/3)
        path.backward(30/3)
        path.up()
        path.goto((self.width_length[frame_num-1]/-10)+5, 150-self.length[self.j]/5+self.bend_length[frame_num-1]/10-8)
        path.color("GhostWhite")
        path.write(f"折边：{self.bend_length[frame_num-1]}mm", align='left', font=('Arial', 8, 'normal'))
        path.hideturtle()
        theScreen.mainloop()

    # 获取窗框编号
    def spin_cb(self):
        self.frameval = self.spinval.get()

    # 组框示意图窗口
    def sketch_map(self):
        if self.sketch_map_run == False:
            if len(self.i_list) <= 0:
                tkinter.messagebox.showerror(title='错误', message='请先计算间隔条数据！！！')
            else:
                self.sketch_win = Toplevel()
                self.sketch_win.title('间隔条组框示意图')
                self.root.update()
                self.sketch_win.geometry(f"450x450+{self.root.winfo_x()+790}+{self.root.winfo_y()+80}")
                self.sketch_win.resizable(0, 0)
                self.sketch_win.wm_attributes('-topmost', 1)

                self.sketch_frame = ttk.Frame(self.sketch_win, borderwidth=5, relief='sunken')
                self.sketch_frame.pack()
                self.sketch_canvas = Canvas(self.sketch_frame, width=400, height=400, background="DarkSlateGray")
                self.sketch_canvas.pack()

                self.show_sketch = ttk.Button(self.sketch_win, text="显示组框", command=self.draw_sketch)
                self.show_sketch.place(x=110, y=420, height=25)

                self.frame_label = ttk.Label(self.sketch_win, text='选择图框编号：')
                self.frame_label.place(x=200, y=420, height=25)

                self.frame_num_list = sorted([int(n/2) for n in set(self.i_list) if n > 0])
                self.spinval = StringVar()
                self.sketch_spin = Spinbox(self.sketch_win, values=self.frame_num_list, textvariable=self.spinval,
                                           command=self.spin_cb, width=8, state='readonly')
                self.spinval.set(self.frame_num_list[len(self.frame_num_list)-1])
                self.frameval = self.spinval.get()
                self.sketch_spin.place(x=280, y=420, height=25)
                self.sketch_map_run = True
        else:
            self.sketch_map_run = False
            self.sketch_win.destroy()
            self.sketch_map()

    # 操作说明窗口
    def operator_manual(self):
        if self.operator_manual_run == False:
            self.manual_win = Toplevel()
            self.manual_win.title('间隔条裁切折弯计算软件操作说明')
            self.root.update()
            self.manual_win.geometry(f"+{self.root.winfo_x() + 220}+{self.root.winfo_y() + 80}")
            self.manual_win.resizable(0, 0)
            self.title_label = Label(self.manual_win, text='操作手册', bg='LightSteelBlue1', font=("微软雅黑", 18, 'bold'),
                                     relief='ridge', width=15, height=1)
            self.title_label.grid(column=0, row=0, pady=4)
            self.manual_scr = scrolledtext.ScrolledText(self.manual_win, width=80, height=15, bg='LightSteelBlue1', relief='sunken',
                                                        font=("微软雅黑", 10, 'bold'), wrap=WORD)
            self.manual_scr.grid(column=0, row=1, padx=4, pady=4)

            file = open("D:\data\operation.txt", "r", encoding='utf-8')
            lines = file.readlines()
            for data in lines:
                self.manual_scr.config(state=NORMAL)
                self.manual_scr.insert(INSERT, data)
                self.manual_scr.config(state=DISABLED)
            file.close()
            self.operator_manual_run = True
        else:
            self.operator_manual_run = False
            self.manual_win.destroy()
            self.operator_manual()

    # 关于窗口
    def about(self):
        if self.about_run == False:
            self.about_win = Toplevel()
            self.about_win.title('关于')
            self.about_win.transient(self.root)
            self.root.update()
            self.about_win.geometry(f"+{self.root.winfo_x() + 220}+{self.root.winfo_y() + 80}")
            self.about_win.resizable(0, 0)
            global logo
            self.logo = PhotoImage(file='D:\data\logo.png')
            self.logo_label = Label(self.about_win, image=self.logo)
            self.logo_label.grid(column=0, row=0, padx=4, pady=4)
            self.text_label = Label(self.about_win, text='间隔条定长裁切折弯计算软件\n版本：V0.8 2020-12-21\n'
                                                         'Copyright(C) 2003-2020\n山东能特异能源科技有限公司',
                                    font=("微软雅黑", 10))
            self.text_label.grid(column=0, row=1)
            self.about_run = True
        else:
            self.about_run = False
            self.about_win.destroy()
            self.about()

    # 创建主画面组件
    def creat_widgets(self):
        # 创建窗口型号显示表格
        columns = ("编号", "宽度", "长度", "数量", "状态")
        self.mighty = ttk.LabelFrame(self.root, text='窗框生产数据')
        self.mighty.grid(column=0, row=0, padx=8, pady=4)
        self.ybar = Scrollbar(self.mighty, orient='vertical')  # 创建滑动条
        self.treeview = ttk.Treeview(self.mighty, show="headings", height=18, columns=columns,
                                     yscrollcommand=self.ybar.set)  # 创建窗口型号显示表格
        self.ybar['command'] = self.treeview.yview
        self.treeview.column("编号", width=40, anchor='center')  # 表示列,不显示
        self.treeview.column("宽度", width=80, anchor='center')
        self.treeview.column("长度", width=80, anchor='center')
        self.treeview.column("数量", width=80, anchor='center')
        self.treeview.column("状态", width=80, anchor='center')
        self.treeview.heading("编号", text="编号")  # 显示表头
        self.treeview.heading("宽度", text="宽度")
        self.treeview.heading("长度", text="长度")
        self.treeview.heading("数量", text="数量")
        self.treeview.heading("状态", text="状态")
        self.treeview.grid(row=0, column=0)
        self.ybar.grid(row=0, column=1, sticky='ns')

        self.treeview.bind('<Double-1>', self.set_cell_value)  # 双击左键进入编辑
        self.newb = ttk.Button(self.mighty, text='新建窗框型号', width=15, command=self.newrow)
        self.newb.grid(row=1, column=0, sticky='s')

        # 创建间隔条裁切折弯计算结果显示表格
        self.columns1 = ("编号", "总长", "全边", "折边", "规格", "余长", "剩余")
        self.mighty1 = ttk.LabelFrame(self.root, text='裁切折弯间隔条计算值')
        self.mighty1.grid(column=1, row=0, padx=8, pady=4)
        self.ybar1=Scrollbar(self.mighty1, orient='vertical')    # 创建滑动条
        self.treeview1 = ttk.Treeview(self.mighty1, show="headings", height=18, columns=self.columns1,
                                      yscrollcommand=self.ybar1.set)    # 创建表格
        self.ybar1['command'] = self.treeview1.yview
        self.treeview1.column("编号", width=40, anchor='center')  # 表示列,不显示
        self.treeview1.column("总长", width=80, anchor='center')
        self.treeview1.column("全边", width=80, anchor='center')
        self.treeview1.column("折边", width=80, anchor='center')
        self.treeview1.column("规格", width=80, anchor='center')
        self.treeview1.column("余长", width=80, anchor='center')
        self.treeview1.column("剩余", width=80, anchor='center')
        self.treeview1.heading("编号", text="编号")  # 显示表头
        self.treeview1.heading("总长", text="总长")
        self.treeview1.heading("全边", text="全边")
        self.treeview1.heading("折边", text="折边")
        self.treeview1.heading("规格", text="规格")
        self.treeview1.heading("余长", text="余长")
        self.treeview1.heading("剩余", text="剩余")
        self.treeview1.grid(row=0, columnspan=4)
        self.ybar1.grid(row=0, column=4, sticky='ns')

        # 创建缓存仓存料情况显示表格
        self.columns2 = ("仓号", "料长")
        self.mighty2 = ttk.LabelFrame(self.root, text='缓存仓存料情况')
        self.mighty2.grid(column=2, row=0, padx=8, pady=4)
        self.ybar2 = Scrollbar(self.mighty2, orient='vertical')
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
        self.send_data = ttk.Button(self.mighty1, text='发送数据', width=15, command=self.write_multiple_registers)
        self.send_data.grid(row=1, column=1, sticky='s')

        self.mighty3 = ttk.LabelFrame(self.root, text='计算信息')
        self.mighty3.grid(row=1, columnspan=2, padx=8, pady=4, sticky='W')
        self.scr = scrolledtext.ScrolledText(self.mighty3, width=153, height=14, wrap=WORD)
        self.scr.grid(column=0, row=0, sticky='WE')

        self.mighty4 = ttk.LabelFrame(self.root, text='相关操作')
        self.mighty4.grid(column=2, row=1, sticky='N', padx=4, pady=4, ipady=40)
        self.clear_table = ttk.Button(self.mighty4, text='清空列表', width=15, command=self.clear_table)
        self.clear_table.grid(row=0, column=0, padx=2, pady=2)
        self.read_table = ttk.Button(self.mighty4, text='读取列表', width=15, command=self.read_table)
        self.read_table.grid(row=0, column=1, padx=2, pady=2)
        self.radVar = IntVar()
        self.radVar.set(2)
        self.manual_Rad = ttk.Radiobutton(self.mighty4, text='手动计算', variable=self.radVar, value=0,
                                          command=self.rad_call)
        self.manual_Rad.grid(row=1, column=0, sticky='W', padx=2, pady=2)
        self.auto_Rad = ttk.Radiobutton(self.mighty4, text='自动计算', variable=self.radVar, value=1,
                                          command=self.rad_call)
        self.auto_Rad.grid(row=1, column=1, sticky='W', padx=2, pady=2)
        self.offline_Rad = ttk.Radiobutton(self.mighty4, text='离线计算', variable=self.radVar, value=2,
                                          command=self.rad_call)
        self.offline_Rad.grid(row=2, column=0, sticky='W', padx=2, pady=2)
        self.com_state_label = ttk.Label(self.mighty4, text='软件与PLC未连接！', foreground='red', font=("微软雅黑", 10))
        self.com_state_label.place(x=2, y=80)
        self.Init_label = ttk.Label(self.mighty4, text='设备未完成初始化！', foreground='red', font=("微软雅黑", 10))
        self.Init_label.place(x=2, y=100)
        self.cut_achieve_label = ttk.Label(self.mighty4, text='裁切进行中，暂不传送数据！', foreground='red', font=("微软雅黑", 10))
        self.cut_achieve_label.place(x=2, y=120)

        self.menu_bar = Menu(self.root)  # 创建菜单
        self.root.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="通讯设置", command=self.com_config_win)
        self.menu_bar.add_command(label="数据监控", command=self.com_datamonitor_win)
        self.menu_bar.add_command(label="组框示意图", command=self.sketch_map)
        self.menu_bar.add_command(label="操作帮助", command=self.operator_manual)
        self.menu_bar.add_command(label="软件退出", command=self._quit)
        self.menu_bar.add_command(label="关于", command=self.about)

# 日志的输出格式及方式做相关配置
def TimedRotatingFileHandler():
    fmt_str = '%(asctime)s\t[level-%(levelname)s][%(module)s.%(funcName)s][%(name)s]:%(message)s'  # 定义日志输出格式
    fileshandle = logging.handlers.TimedRotatingFileHandler('D:\Logger\Data_Log', when='M', interval=5, backupCount=3)
    fileshandle.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt_str)
    fileshandle.setFormatter(formatter)
    logging.getLogger('').addHandler(fileshandle)

if __name__ == '__main__':
    TimedRotatingFileHandler()
    cal = CalculateApp()
    cal.root.mainloop()  # 进入消息循环