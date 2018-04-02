#!/usr/bin/env python  
# -*- coding: utf-8 -*  
   
import serial  
import serial.tools.list_ports
import time,threading
import string


def get_port_set():
    port_set = set()
    port_list = list(serial.tools.list_ports.comports())
    for comlist in port_list:
        port_set.add(comlist[0]) 
    return port_set

def set_baud(ser):
    baud = input("请输入时间段设置参数,[同步 时间段1 时间段2 时间单位长度],不设置请直接按回车\r\n")
    ser.write(("ATbaud " + baud + "\r\n").encode())
    get_res = ser.readline()
    time.sleep(0.1)  
    get_res += ser.readline()
    return get_res

def set_uart(ser):
    baud = input("请输入要设定的透传波特率,例如115200,不设置请直接按回车\r\n")
    ser.write(("ATuart " + baud + "\r\n").encode())
    get_res = ser.readline()
    return get_res

def clear_filter(ser):
    print("    正在清除滤波器和屏蔽器...")
    ser.write("ATmh 0\r\n ".encode())
    get_res = ser.readline()
    ser.write("ATml 0\r\n ".encode())
    get_res += ser.readline()
    ser.write("ATfh 0\r\n ".encode())
    get_res += ser.readline()
    ser.write("ATfl 0\r\n ".encode())
    get_res += ser.readline()
    print("    清除完毕")
    return get_res

def init_sniffer(ser):
    print("1，设备透传波特率被设置为115200")
    ser.write("ATuart 115200\r\n ".encode())
    print("    ",ser.readline())
    print("2，清除过滤器")
    print("    ",clear_filter(ser))
    print("3，can总线特征被设置为1 4 4 8 -500kbps")
    ser.write("ATbaud 1 4 4 8\r\n ".encode())
    print("    ",ser.readline())
    time.sleep(0.1)
    print("    ",ser.readline())
    return "初始化完毕"

def set_menu(ser):
    while 1:
        menu_num = input("请选择：1 设置CAN波特率 2 设置透传波特率 3 清空过滤器 4 初始化 5 退出\r\n")
        menu_num = menu_num.replace('\r','').replace('\n','').strip()
        if menu_num == '1':
            print("    ",set_baud(ser))
        elif menu_num == '2':
            print("    ",set_uart(ser))
        elif menu_num == '3':
            print("    ",clear_filter(ser))
        elif menu_num == '4':
            print("    ",init_sniffer(ser))
        else:
            break
            
old_port_set = set()
new_port_set = set()
old_port_set = get_port_set()
print("请插入can嗅探器模块:")
while 1:    
    time.sleep(0.5)  
    new_port_set = get_port_set()
    diff_set = new_port_set - old_port_set
    if len(diff_set)>0 :
        get_port = diff_set.pop();
        #print("find new port:",get_port)
        print("检测到新设备插入，正在进入设置模式")
        time.sleep(0.5)  
        ser=serial.Serial(get_port,115200,timeout=0.5)
        ser.write("ATmode on\r\n".encode())
        print("    ",ser.readline())
        set_menu(ser)
        ser.close()
        print("再见！")
        break
        

