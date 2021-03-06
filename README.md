# CAN总线嗅探器说明

## 简介
魔豆CAN总线嗅探器cansniffer是一款用于研究车载CAN总线通信的数据调试工具，通常情况下使用我们需要一块能够读取CAN总线上的通信数据的数据采样板来将车载CAN网络中的数据发送到电脑上，然后利用电脑的数据分析能力对接收到的CAN总线数据包进行分类。\
![image](https://github.com/zshchance/cansniffer/blob/master/img/can_s1.jpg)
### 模块淘宝地址：
[购买连接 85元](https://item.taobao.com/item.htm?spm=0.7095261.0.0.57231deblznqvF&id=567000108428)


## 接线
魔豆can总线嗅探器通过CANH CANL两根线接入车载CAN总线网络，将CAN总线数据通过串口发送给电脑，魔豆CAN总线嗅探器自带USB-TTL，采用高性能FT232RL转串芯片，这款转串芯片几乎是市场上最贵的USB-TTL芯片了，我们使用这款USB-TTL芯片的原因之一主要是出于稳定性考虑，测试过程中我们尝试过PL2303\CP2102\CH340G\FT232RL等多款USB-TTL芯片，测试发现FT232RL和CP2102的次品率最低，CH340G次之，PL2303次品率最高，而稳定性上测试发现长时间使用PL2303表现很差，最终为了兼容各种平台的驱动，我们选择了FT232RL作为嗅探器的转串芯片。\
![image](https://github.com/zshchance/cansniffer/blob/master/img/can_s2.jpg)

## 下位机协议
在魔豆can总线探测器通电的前10s内处于AT指令响应状态，可以通过串口向模块发送ATmode on\r\n来使模块本次通电过程中一直保留在AT指令响应状态，注意模块在AT指令响应状态下依然可以接收CAN总线上的数据。
模块在AT指令响应状态下，可以响应以下AT指令：（指令必须以\r\n结尾）


---

### ATmode [on]\r\n
#### 对是模块在本次通电状态停留或退出AT指令响应状态
#### 参数说明：
##### on： 模块停留在AT指令响应状态
##### 无或其他： 模块退出AT指令响应状态
#### 返回信息：
##### can sniffer atmode: 状态码\r\n
##### 状态吗：0 已退出AT指令响应状态 2 已进入AT指令响应状态

---


### ATbaud [同步位数] [时间段1] [时间段2] [时间单位长度]\r\n
#### 查询或设置模块的CAN总线波特率通信采样特性，最终的CAN波特率为36000/(同步位数+时间段1+时间段2)/时间单位长度kbps，例如当设置ATbaud 1 4 4 8，代表设置同步使用1个时间单位，时间段1使用4个时间单位，时间段2使用4个时间单位，一个CAN采样电平一共消耗1+4+4=9个时间单位，每个时间单位消耗8个时钟，最终CAN总线采样波特率为36000/(1+4+4)/8=500kbps，注意：只发送ATbaud\r\n不含参数，则为查询当前CAN总线设置的参数状态，该设置会被模块记忆
#### 参数说明：
##### 同步位数:范围1-4
##### 时间段1：范围1-16
##### 时间段2：范围1-8
##### 时间单位：范围1-1024
#### 返回信息：
##### canbaud:CAN波特率\r\n can paras:同步位数 时间段1 时间段2 时间单位长度\r\n

---

### ATuart [串口波特率]\r\n
#### 查询或设置模块的串口波特率，该设置仅在退出AT指令响应状态下生效，在AT指令响应状态中串口波特率始终是115200，防止因意外设置导致电脑无法和模块进行通信！注意：只发送ATuart\r\n不含参数，则为查询当前模块串口波特率参数状态，该设置会被模块记忆
#### 参数说明：
##### 串口波特率 推荐范围4800-256000，可以是非标准的串口波特率
#### 返回信息：
##### uart baud:串口波特率\r\n

---

### ATrst\r\n
#### 重启模块
#### 参数说明：
##### 无
#### 返回信息：
##### 模块被重新启动时候默认的启动信息

---

### ATfh [CAN嗅探过滤位高16位]\r\n
#### 查询或设置模块的过滤为寄存器！注意：只发送ATfh\r\n不含参数，则为查询当前模块屏蔽位高16位，该设置会被模块记忆
#### 参数说明：
##### CAN嗅探过滤位高16位 不需要前导0x字符，比如需要设置为0xabcd，只需要发送明令ATfh abcd\r\n 参数不用区分大小写
#### 返回信息：
##### can filter high:过滤位高16位值\r\n

---

### ATfl 设置CAN过滤位底16位值，用法雷同ATfh，返回信息为can filter low:过滤位低16位值\r\n

---

### ATmh 设置CAN屏蔽位高16位值，用法雷同ATfh，返回信息为can mask high:屏蔽位高16位值\r\n
### 不需要开启屏蔽功能可以设置为0

---

### ATml 设置CAN屏蔽位低16位值，用法雷同ATfh，返回信息为can mask low:屏蔽位低16位值\r\n
### 不需要开启屏蔽功能可以设置为0

---

### 过滤器和屏蔽器各位值含义
![image](https://github.com/zshchance/cansniffer/blob/master/img/filter_mask.jpg)

---

### 模块接收到CAN数据传输格式
#### [stdID_h stdID_l] [extID_h2 extID_h1 extID_l1 extID_l2] [ide] [rtr] [dlc] [data0 data1 data2 data3 data4 data5 data6 data7] [0x0d 0x0a]
stdID_h: 标准帧高8位 16进制\
stdID_l: 标准帧第8位 16进制\
extID_h2：扩展帧高32-25位 16进制\
extID_h1：扩展帧高24-17位 16进制\
extID_l1: 扩展帧高16-9位 16进制\
extID_l2：扩展帧低8位 16进制\
ide：帧ID类型 0 标准帧 4 扩展帧 16进制\
rtr：帧类型 0 数据帧 2 远程帧 16进制\
dlc：数据长度 0-8 16进制\
data0-7:携带的数据位值 16进制

## 使用python设置can总线嗅探器参数
1. 安装python
2. 安装依赖模块serial serialtool
> pip install serial\
> pip install serialtool
3. 运行sniffer_init.py
4. 在电脑usb插入can嗅探器模块

sniffer_init.py可以对模块各种参数进行设置如图\
![image](https://github.com/zshchance/cansniffer/blob/master/img/python_menu.jpg)
![image](https://github.com/zshchance/cansniffer/blob/master/img/python_help.jpg)

## 使用winform程序分析can总线数据
![image](https://github.com/zshchance/cansniffer/blob/master/img/data_recv.jpg)
![image](https://github.com/zshchance/cansniffer/blob/master/img/data_save.jpg)