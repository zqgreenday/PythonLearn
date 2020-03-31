#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import tkinter
from tkinter import ttk
import tkinter.messagebox  # 要使用messagebox先要导入模块


class Modbus_Rtu():
    def __init__(self,mbComPort,baudrate,databit,parity,stopbit,mbTimeout):
        self.mbComPort = mbComPort
        self.baudrate = baudrate
        self.databit = databit
        self.parity = parity
        self.stopbit = stopbit
        self.mbTimeout = mbTimeout # ms
    def mb_port_open(self):
        try:
            mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity,
                                    stopbits=stopbit)
            self.master = modbus_rtu.RtuMaster(mb_port)
            self.master.set_timeout(mbTimeout / 1000.0)
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message='Modbus Error: ' + str(e))

    def read_coils(self,mbId,addr,num):
        try:
            for widget in frame2.winfo_children():
                widget.destroy()
            if num <= 64:
                rc = self.master.execute(mbId, cst.READ_COILS, addr, num)
                label1 = tkinter.Label(frame2, text='读取的线圈数据：')
                label1.place(x=0, y=0)
                a = 0
                for y in range(num//8+1):
                    for x in range(8):
                        if a < num:
                            label2 = tkinter.Label(frame2, bd=2, relief="sunken", text=str(rc[a]))
                            if rc[a]==1:
                                label2['bg'] = "green"
                            else:
                                label2['bg'] = "red"
                            label2.place(x=x * 12, y=(y + 1) * 20)  # 将标签添加到主窗口
                            a += 1
                        else:
                            break
                root.after(1000, lambda: self.read_coils(mbId, convert(entrydata1), convert(entrydata2)))
            else:
                tkinter.messagebox.showwarning(title='Error', message='读取数量设定超范围，必须在64个以内！！')
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message='Modbus Error: '+str(e))

    def write_single_register(self,mbId,addr,data):
        try:
            self.master.execute(mbId, cst.WRITE_SINGLE_REGISTER, addr, output_value=data)
            wsr = self.master.execute(mbId, cst.READ_HOLDING_REGISTERS, addr, 1)
            label = tkinter.Label(frame1, width=5, bd=2, relief="sunken", text=str(wsr[0]))
            label.grid(row=5, column=1)
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message='Modbus Error: ' + str(e))

    def read_holding_registers(self,mbId,addr,num):
        try:
            for widget in frame3.winfo_children():
                widget.destroy()
            if num <= 24:
                rhg = self.master.execute(mbId, cst.READ_HOLDING_REGISTERS, addr, num)
                label1 = tkinter.Label(frame3, text='读取的寄存器数据：')
                label1.place(x=0, y=0)
                a = 0
                for y in range((num//3)+1):
                    for x in range(3):
                        if a < num:
                            label2 = tkinter.Label(frame3, width=5, bd=2, relief="sunken", text=str(rhg[a]))  # 生成标签
                            label2.place(x=x*40, y=(y+1)*20)  # 将标签添加到主窗口
                            a += 1
                        else:
                            break
                root.after(1000, lambda: self.read_holding_registers(mbId, convert(entrydata5), convert(entrydata6)))
            else:
                tkinter.messagebox.showwarning(title='Error', message='读取数量设定超范围，必须在24个以内！！')
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message='Modbus Error: ' + str(e))

    def write_single_coil(self,mbId,addr,data):
        try:
            self.master.execute(mbId, cst.WRITE_SINGLE_COIL, addr, output_value=data)
            wsc = self.master.execute(mbId, cst.READ_COILS, addr, 1)
            label = tkinter.Label(frame1, width=5, bd=2, relief="sunken", text=str(wsc[0]))
            label.grid(row=1, column=1)

        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message='Modbus Error: ' + str(e))

    def mb_port_close(self):
        self.master._do_close()

if __name__ == '__main__':

    root = tkinter.Tk()  # 生成root主窗口
    root.title('Modbus Rtu with XinJe')
    root.geometry('500x280')

    frame1 = tkinter.Frame(root, bd=3, relief="ridge")
    frame1.place(x=6, y=65, width=250, height=185)
    frame2 = tkinter.Frame(root, bd=3, relief="ridge")
    frame2.place(x=261, y=65, width=103, height=185)
    frame3 = tkinter.Frame(root, bd=3, relief="ridge")
    frame3.place(x=368, y=65, width=124, height=185)
    frame4 = tkinter.Frame(root, bd=3, relief="ridge")
    frame4.place(x=6, y=5, width=486, height=57)

    def convert(entrydata):
        data = entrydata.get()
        try:
            data = int(data)
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message='Error: ' + str(e))
        return data
    def getdata(comboxlist,comvalue):
        data = comboxlist.get()
        comvalue.set(comboxlist.get())
        return data

    # 通讯参数设置
    label9 = tkinter.Label(frame4, text='ID：')
    label9.grid(row=0, column=0)
    entrydata9 = tkinter.Entry(frame4, width=5)
    entrydata9.insert(0, '1')
    entrydata9.grid(row=0, column=1)
    label10 = tkinter.Label(frame4, text='Port：')
    label10.grid(row=0, column=2)
    comvalue1 = tkinter.StringVar()
    comboxlist1 = ttk.Combobox(frame4, width=5, textvariable=comvalue1)
    comboxlist1["values"] = ("COM1", "COM2", "COM3", "COM4", "COM5")
    comboxlist1.current(2)
    comboxlist1.grid(row=0, column=3)
    label11 = tkinter.Label(frame4, text='BandRate：')
    label11.grid(row=0, column=4)
    comvalue2 = tkinter.StringVar()
    comboxlist2 = ttk.Combobox(frame4, width=5, textvariable=comvalue2)
    comboxlist2["values"] = ("2400", "4800", "9600", "19200", "38400")
    comboxlist2.current(3)
    comboxlist2.grid(row=0, column=5)
    label11 = tkinter.Label(frame4, text='DataBit：')
    label11.grid(row=0, column=6)
    comvalue3 = tkinter.StringVar()
    comboxlist3 = ttk.Combobox(frame4, width=5, textvariable=comvalue3)
    comboxlist3["values"] = ("5", "6", "7", "8")
    comboxlist3.current(3)
    comboxlist3.grid(row=0, column=7)
    label12 = tkinter.Label(frame4, text='Parity：')
    label12.grid(row=1, column=2)
    comvalue4 = tkinter.StringVar()
    comboxlist4 = ttk.Combobox(frame4, width=5, textvariable=comvalue4)
    comboxlist4["values"] = ("N", "E", "O")
    comboxlist4.current(1)
    comboxlist4.grid(row=1, column=3)
    label13 = tkinter.Label(frame4, text='StopBit：')
    label13.grid(row=1, column=4)
    comvalue5 = tkinter.StringVar()
    comboxlist5 = ttk.Combobox(frame4, width=5, textvariable=comvalue5)
    comboxlist5["values"] = ("1", "2")
    comboxlist5.current(0)
    comboxlist5.grid(row=1, column=5)
    label14 = tkinter.Label(frame4, text='TimeOut：')
    label14.grid(row=1, column=6)
    entrydata10 = tkinter.Entry(frame4, width=9)
    entrydata10.insert(0, '100')
    entrydata10.grid(row=1, column=7)

    mbComPort = getdata(comboxlist1, comvalue1)
    baudrate = int(getdata(comboxlist2, comvalue2))
    databit = int(getdata(comboxlist3, comvalue3))
    parity = getdata(comboxlist4, comvalue4)
    stopbit = int(getdata(comboxlist5, comvalue5))
    mbTimeout = convert(entrydata10)  # ms

    # 通讯地址
    mbId = convert(entrydata9)

    modbusrtu = Modbus_Rtu(mbComPort,baudrate,databit,parity,stopbit,mbTimeout)

    button6 = tkinter.Button(frame4, text='打开串口', command=modbusrtu.mb_port_open)
    button6.grid(row=0, column=8, padx=5, pady=1)

    button6 = tkinter.Button(frame4, text='关闭串口', command=modbusrtu.mb_port_close)
    button6.grid(row=1, column=8, padx=5, pady=1)

    # Write Single Coil功能码测试
    label7 = tkinter.Label(frame1, text='线圈写入地址：')
    label7.grid(row=0, column=0)
    entrydata7 = tkinter.Entry(frame1, width=6)
    entrydata7.insert(0, '0')
    entrydata7.grid(row=0, column=1)
    label8 = tkinter.Label(frame1, text='输入状态：')
    label8.grid(row=0, column=2)
    entrydata8 = tkinter.Entry(frame1, width=5)
    entrydata8.insert(0, '0')
    entrydata8.grid(row=0, column=3)
    button4 = tkinter.Button(frame1, text='Write Single Coil', width=15,
                             command=lambda: modbusrtu.write_single_coil(mbId, convert(entrydata7),
                                                                          convert(entrydata8)))
    button4.grid(row=1, column=0)

    # Read Coils功能码测试
    label1 = tkinter.Label(frame1, text='线圈起始地址：')
    label1.grid(row=2, column=0)
    entrydata1 = tkinter.Entry(frame1, width=6)
    entrydata1.insert(0, '16384')
    entrydata1.grid(row=2, column=1)
    label2 = tkinter.Label(frame1, text='读取数量：')
    label2.grid(row=2, column=2)
    entrydata2 = tkinter.Entry(frame1, width=5)
    entrydata2.insert(0, '1')
    entrydata2.grid(row=2, column=3)
    button1 = tkinter.Button(frame1, text='Read Coils', width=15,
                             command=lambda: modbusrtu.read_coils(mbId, convert(entrydata1),
                                                                   convert(entrydata2)))
    button1.grid(row=3, column=0)  # 将button1添加到root主窗口

    # Write Single Register功能码测试
    label3 = tkinter.Label(frame1, text='寄存器写入地址：')
    label3.grid(row=4, column=0)
    entrydata3 = tkinter.Entry(frame1, width=6)
    entrydata3.insert(0, '0')
    entrydata3.grid(row=4, column=1)
    label4 = tkinter.Label(frame1, text='输入数据：')
    label4.grid(row=4, column=2)
    entrydata4 = tkinter.Entry(frame1, width=5)
    entrydata4.insert(0, '0')
    entrydata4.grid(row=4, column=3)
    button2 = tkinter.Button(frame1, text='Write Single Reg', width=15,
                             command=lambda: modbusrtu.write_single_register(mbId, convert(entrydata3),
                                                                   convert(entrydata4)))
    button2.grid(row=5, column=0)

    # Read Holding Registers功能码测试
    label5 = tkinter.Label(frame1, text='寄存器起始地址：')
    label5.grid(row=6, column=0)
    entrydata5 = tkinter.Entry(frame1, width=6)
    entrydata5.insert(0, '0')
    entrydata5.grid(row=6, column=1)
    label6 = tkinter.Label(frame1, text='读取数量：')
    label6.grid(row=6, column=2)
    entrydata6 = tkinter.Entry(frame1, width=5)
    entrydata6.insert(0, '1')
    entrydata6.grid(row=6, column=3)
    button3 = tkinter.Button(frame1, text='Read Holding Reg', width=15,
                             command=lambda: modbusrtu.read_holding_registers(mbId, convert(entrydata5),
                                                                    convert(entrydata6)))
    button3.grid(row=7, column=0)

    button5 = tkinter.Button(root, text='Quit', command=root.quit)
    button5.place(x=6, y=255, width=50)

    root.update()
    root.mainloop()

