#!/usr/bin/env python  
# -*- coding: utf-8 -*  

import sys
import serial  
import serial.tools.list_ports
import time,threading
import string
sys.path.append('.');
from Menu_function import Menu_function;
from _Getch import _Getch;
#import msvcrt

def get_port_set():
    port_set = set()
    port_list = list(serial.tools.list_ports.comports())
    for comlist in port_list:
        port_set.add(comlist[0]) 
    return port_set

def set_menu(ser,mSerial):
    mymenu = Menu_function(ser)
    while 1:
        menu_num = input("请选择：1 设置CAN波特率 2 设置透传波特率 3 清空过滤器 4 初始化 5 测试CAN波特率 6 退出\r\n")
        menu_num = menu_num.replace('\r','').replace('\n','').strip()
        if menu_num == '1':
            print("    ",mymenu.set_baud())
        elif menu_num == '2':
            print("    ",mymenu.set_uart())
        elif menu_num == '3':
            print("    ",mymenu.clear_filter())
        elif menu_num == '4':
            print("    ",mymenu.init_sniffer())
        elif menu_num == '5':
            print("    ",mymenu.scan_can_baud(mSerial))
            getch = _Getch()
            
            while 1:
                ch = getch()
                if ord(ch) == ord('q'):
                    mSerial.stop_recv()
                    break
                elif ord(ch) == ord('a'):
                    mSerial.stop_recv()
                    print("    ",mymenu.auto_set_can_baud(0))
                    mSerial.start_recv()
                elif ord(ch) == ord('s'):
                    mSerial.stop_recv()
                    print("    ",mymenu.auto_set_can_baud(1))
                    mSerial.start_recv()
            del getch
        else:
            break

class MSerialPort:  
    message=''
    thread_run = True
    def __init__(self,ser):  
        self.ser=ser  
        if not self.ser.isOpen():  
            self.ser.open()
    def stop_recv(self):
        self.thread_run = False
    def start_recv(self):
        self.thread_run = True
        t = threading.Thread(target=self.read_data)
        t.start()
    def port_open(self):  
        if not self.ser.isOpen():  
            self.ser.open()  
    def port_close(self):  
        self.ser.close()  
    def send_data(self,data):  
        number=self.ser.write(data)  
        return number  
    def read_data(self):
        while self.thread_run:
            data = b''
            while self.ser.inWaiting() > 0:
                #data += self.ser.read(1);
                data += self.ser.readline()
            #self.message+=data
            #print(self.message)
            #self.message = ''
            if len(data)>0:
                print(data)
            
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
        mSerial = MSerialPort(ser)
        set_menu(ser,mSerial)
        mSerial.stop_recv()
        ser.close()
        print("再见！")
        break
        

