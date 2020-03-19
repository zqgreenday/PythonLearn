#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import tkinter
import tkinter.messagebox  # 要使用messagebox先要导入模块

"""
supported modbus functions:
READ_COILS = 1
READ_DISCRETE_INPUTS = 2
READ_HOLDING_REGISTERS = 3
READ_INPUT_REGISTERS = 4
WRITE_SINGLE_COIL = 5
WRITE_SINGLE_REGISTER = 6
READ_EXCEPTION_STATUS = 7
DIAGNOSTIC = 8
WRITE_MULTIPLE_COILS = 15
WRITE_HOLDING_REGISTERS = 16
READ_WRITE_MULTIPLE_REGISTERS = 23
DEVICE_INFO = 43
"""



def read_coils(mbId,addr,num):
    try:
        # FATEK的PLC把DI點放在DO的address中
        #-- FC01: Read multi-coils status (0xxxx) for DO
        rr1 = master.execute(mbId, cst.READ_COILS, addr, num)
        a = 0
        while a < num:
            label = tkinter.Label(root, text=str(rr1[a]))  # 生成标签
            label.grid(row=1, column=a+1)  # 将标签添加到主窗口
            a += 1
        root.after(1000, lambda: read_coils(mbId, addr, num))
    except Exception as e:
        tkinter.messagebox.showinfo(title='Error', message='Modbus Error: '+str(e))
        print("\nmodbus test Error: " + str(e))

def write_single_register(mbId,addr,data):
    try:
        master.execute(mbId, cst.WRITE_SINGLE_REGISTER, addr, output_value=data)
        rh = master.execute(mbId, cst.READ_HOLDING_REGISTERS, addr, 1)
        label = tkinter.Label(root, text=str(rh[0]))
        label.grid(row=3, column=1)

    except Exception as e:
        tkinter.messagebox.showinfo(title='Error', message='Modbus Error: ' + str(e))
        print("\nmodbus test Error: " + str(e))

def read_holding_registers(mbId,addr,num):
    try:
        rr2 = master.execute(mbId, cst.READ_HOLDING_REGISTERS, addr, num)
        a = 0
        while a < num:
            label = tkinter.Label(root, text=str(rr2[a]))  # 生成标签
            label.grid(row=5, column=a+1)  # 将标签添加到主窗口
            a += 1
        root.after(1000, lambda: read_holding_registers(mbId, addr, num))
    except Exception as e:
        tkinter.messagebox.showinfo(title='Error', message='Modbus Error: ' + str(e))
        print("\nmodbus test Error: " + str(e))

def write_single_coil(mbId,addr,data):
    try:
        master.execute(mbId, cst.WRITE_SINGLE_COIL, addr, output_value=data)
        rh = master.execute(mbId, cst.READ_COILS, addr, 1)
        label = tkinter.Label(root, text=str(rh[0]))
        label.grid(row=7, column=1)

    except Exception as e:
        tkinter.messagebox.showinfo(title='Error', message='Modbus Error: ' + str(e))
        print("\nmodbus test Error: " + str(e))

if __name__ == '__main__':
    mbComPort = 'COM3'
    baudrate = 19200
    databit = 8
    parity = 'E'
    stopbit = 1
    mbTimeout = 100  # ms
    mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
    master = modbus_rtu.RtuMaster(mb_port)
    master.set_timeout(mbTimeout / 1000.0)

    root = tkinter.Tk()  # 生成root主窗口
    root.title('Modbus Rtu test')
    root.geometry('250x250')

    def convert(entrydata):
        data = entrydata.get()
        try:
            data = int(data)
        except Exception as e:
            tkinter.messagebox.showinfo(title='Error', message='Modbus Error: ' + str(e))
        return data

    # Read Coils功能码测试
    label1 = tkinter.Label(root, text='线圈起始地址：')
    label1.grid(row=0, column=0)
    entrydata1 = tkinter.Entry(root, width=8)
    entrydata1.grid(row=0, column=1)
    label2 = tkinter.Label(root, text='读取数量：')
    label2.grid(row=0, column=2)
    entrydata2 = tkinter.Entry(root, width=5)
    entrydata2.grid(row=0, column=3)
    button1 = tkinter.Button(root, text='Read Coils',
                             command=lambda: read_coils(mbId, convert(entrydata1), convert(entrydata2)))
    button1.grid(row=1, column=0)  # 将button1添加到root主窗口

    # Write Single Register功能码测试
    label3 = tkinter.Label(root, text='寄存器地址：')
    label3.grid(row=2, column=0)
    entrydata3 = tkinter.Entry(root, width=5)
    entrydata3.grid(row=2, column=1)
    label4 = tkinter.Label(root, text='输入数据：')
    label4.grid(row=2, column=2)
    entrydata4 = tkinter.Entry(root, width=5)
    entrydata4.grid(row=2, column=3)
    button2 = tkinter.Button(root, text='Write Single Reg',
                             command=lambda: write_single_register(mbId, convert(entrydata3), convert(entrydata4)))
    button2.grid(row=3, column=0)

    #Read Holding Registers功能码测试
    label5 = tkinter.Label(root, text='寄存器起始地址：')
    label5.grid(row=4, column=0)
    entrydata5 = tkinter.Entry(root, width=8)
    entrydata5.grid(row=4, column=1)
    label6 = tkinter.Label(root, text='读取数量：')
    label6.grid(row=4, column=2)
    entrydata6 = tkinter.Entry(root, width=5)
    entrydata6.grid(row=4, column=3)
    button3 = tkinter.Button(root, text='Read Holding Reg',
                             command=lambda: read_holding_registers(mbId, convert(entrydata5), convert(entrydata6)))
    button3.grid(row=5, column=0)

    # Write Single Coil功能码测试
    label7 = tkinter.Label(root, text='线圈地址：')
    label7.grid(row=6, column=0)
    entrydata7 = tkinter.Entry(root, width=5)
    entrydata7.grid(row=6, column=1)
    label8 = tkinter.Label(root, text='输入状态：')
    label8.grid(row=6, column=2)
    entrydata8 = tkinter.Entry(root, width=5)
    entrydata8.grid(row=6, column=3)
    button4 = tkinter.Button(root, text='Write Single Coil',
                             command=lambda: write_single_coil(mbId, convert(entrydata7), convert(entrydata8)))
    button4.grid(row=7, column=0)

    button5 = tkinter.Button(root, text='Quit', command=root.quit)
    button5.place(x=10, y=220)

    master._do_close()
    root.mainloop()
