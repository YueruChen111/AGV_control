from https://class.kinco.cn/articledetail/138.html

# 上位机向伺服电机发送和收到的指令

## NMT管理报文

### NMT模块控制报文(主-->从)
- 0X0000 CS Node_ID(0则发给所有从节点)
- CS:
    0x1   Start Remote Node
    0x2   Stop Remote Node
    0x80  Enter Pre-operational State
    0x81  Reset Node
    0x82  Reset Communication

### NMT节点保护报文(主周期性发送，监视从节点当前状态)
- 主：0X700+Node_ID
- 从应答：0X700+Node_ID 6位状态 触发位0/1(交替)
- bit0-6状态表：
    0x0   Initialising (不会出现)
    0x1   Disconnected*
    0x2   Connecting*
    0x3   Preparing*
    0x4   Stopped
    0x5   Operational
    0x7F  Pre-operational
- 带*需要支持扩展BOOT-UP的节点才提供

### 心跳报文(每个节点都能发，通常从-->主)
- 0X700+Node_ID 状态
- 状态表：
    0x0   Boot-up
    0x4   Stopped
    0x5   Operational
    0x7F  Pre-operational
    不能和保护报文同时使用

### NMT Boot-up启动报文(从-->主，从init到pre-op)
- 0X700+Node_ID 0

## 紧急报文
- 0X080+Node_ID 应急错误代码 错误寄存器(对象1x1001) 制造商特定的错误区域
- 错误寄存器的位定义：
    0   Generic
    1   Current
    2   Voltage
    3   Temperature
    4   Communication
    5   Device profile specific
    6   Reserved(=0)
    7   Manufacturer specific

## SDO报文(配置参数)

### SDO读报文
- 请求报文：600+Node_ID 命令字 对象索引 对象子索引 00
- 应答报文：580+Node_ID 命令字 对象索引 对象子索引 **
- 命令字：
    读报文     0x40

    数据1个字节 0x4F
    数据2个字节 0x4B
    数据3个字节 0x47
    数据4个字节 0x43
    失败       0x80
- 伺服Object Dictionary(各目标对应的索引子索引)
- ex: 读取站号为1的伺服实际位置60630020，数据4个字节，为FFFFFD113HEX，转成十进制-12013
    发送：0x601 |40 |63 60 |00 |00 00 00 00 
    接收：0x581 |43 |63 60 |00 |13 D1 FF FF
- CANopne数据低字节在高字节后，注意高低字节调换

### SDO写报文
- 写报文：0x600+Node_ID 命令字 对象索引 对象子索引 数据
- 回应报文：0x580+Node_ID 命令字 对象索引 对象子索引 **(可缺省或原样返回数据)
- 命令字：
    数据1个字节 0x2F
    数据2个字节 0x2B
    数据3个字节 0x27
    数据4个字节 0x23

    成功       0x60
    失败       0x80
- ex：写站号为1的伺服目标位置607A0020，100000inc=000186A0HEX
    发送：0x601 |23 |7A 60 |00 |A0 86 01 00
    成功接收：0x581 |60 |7A 60 |00 |A0 86 01 00
    失败接收：0x581 |80 |7A 60 |00 |错误代码


## PDO报文
- 每个PDO在对象字典中用2个对象描述：
    PDO通讯参数：COB_ID,传输类型，禁止时间，定时器周期
    PDO映射参数：OD中的对象列表，数据长度
    报文内容预定义
- ex：(以伺服为中心)
    TX-PDO: 181 |13 D1 FF FF |31 02 
    RX-PDO: 201 |XX XX XX XX |XX XX |XX (COB_ID 目标速度 控制字 工作模式)


## 同步报文
- 运动控制领域，相当于timer
- 内容只有COB_ID: 0x80
- 伺服周期性同步位置模式CSP


## Demo based on cocomm
- Start Remote Node
    0X0000 0x1 0
- Enter Pre-operational State
    0X0000 0x80 0
- 发送节点保护报文
    0X700+Node_ID 0x70
