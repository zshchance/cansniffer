#!/usr/bin/env python  
# -*- coding: utf-8 -*  
   
import serial  
import serial.tools.list_ports
import time,threading
import string

class Menu_function(object):
    pre_set_baud = [[1,3,2,60,'100k'],[1,4,4,8,'500k']]
    def __init__(self,ser):
        self.ser = ser
        self.baudIndex = 0
        
    def set_baud(self):
        baud = input("请输入时间段设置参数,[同步 时间段1 时间段2 时间单位长度],不设置请直接按回车\r\n")
        self.ser.write(("ATbaud " + baud + "\r\n").encode())
        get_res = self.ser.readline()
        time.sleep(0.1)  
        get_res += self.ser.readline()
        return get_res
    
    def auto_set_can_baud(self,add_or_min):
        if add_or_min == 1:
            self.baudIndex += 1
        else:
            self.baudIndex -= 1
        
        if self.baudIndex > len(self.pre_set_baud)-1:
            self.baudIndex = 0
        elif self.baudIndex < 0:
            self.baudIndex = len(self.pre_set_baud)-1
            
        self.ser.write(("ATbaud " + str(self.pre_set_baud[self.baudIndex][0])\
                            + " " + str(self.pre_set_baud[self.baudIndex][1]) + " "\
                            + str(self.pre_set_baud[self.baudIndex][2]) + " "\
                            + str(self.pre_set_baud[self.baudIndex][3]) + "\r\n").encode())
        get_res = self.ser.readline()
        time.sleep(0.1)  
        get_res += self.ser.readline()
        return get_res

    def set_uart(self):
        baud = input("请输入要设定的透传波特率,例如115200,不设置请直接按回车\r\n")
        self.ser.write(("ATuart " + baud + "\r\n").encode())
        get_res = self.ser.readline()
        return get_res

    def clear_filter(self):
        print("    正在清除滤波器和屏蔽器...")
        self.ser.write("ATmh 0\r\n ".encode())
        get_res = self.ser.readline()
        self.ser.write("ATml 0\r\n ".encode())
        get_res += self.ser.readline()
        self.ser.write("ATfh 0\r\n ".encode())
        get_res += self.ser.readline()
        self.ser.write("ATfl 0\r\n ".encode())
        get_res += self.ser.readline()
        print("    清除完毕")
        return get_res

    def init_sniffer(self):
        print("1，设备透传波特率被设置为115200")
        self.ser.write("ATuart 115200\r\n ".encode())
        print("    ",self.ser.readline())
        print("2，清除过滤器")
        print("    ",self.clear_filter())
        print("3，can总线特征被设置为1 4 4 8 -500kbps")
        self.ser.write("ATbaud 1 4 4 8\r\n ".encode())
        print("    ",self.ser.readline())
        time.sleep(0.1)
        print("    ",self.ser.readline())
        return "初始化完毕"

    def scan_can_baud(self,mSerial):
        print("    正在使用不同的CAN频率测试接收CAN总线数据\r\n")
        print("    按q退出测试，按a、s分别切换上一个、下一个波特率\r\n")
        mSerial.start_recv()
        return ""

