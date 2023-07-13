## AVG_control简介
- 完成Kinco iWMC 集成式伺服轮基于cocomm的CanOpen通讯对接
- 搭建AGV双轮差速运动学模型
- 实现功能：控制小车双轮速度和行进距离，优化路径规划

## 使用方法

### PC端驱动伺服轮
CANopen通信详见https://github.com/CANopenNode/CANopenDemo/blob/master/tutorial

- 启动测试用can卡: can0连结主站和从站
ip link show
sudo ip link set up can0 type can bitrate 500000

- 使用CANopenLinux作为主站 
cd CANopenLinux
sudo make install
canopend can0 -i 1 -c "local-/tmp/CO_command_socket"

- 使用伺服轮作为从站
在上位机软件中修改左轮和右轮的ID

- 使用debug.py测试cocomm指令

### AGV小车测试
- 在main.py中调用basic_functions和CO_command中的控制函数，完成路径设计并运行
- 根据实际模型修改wheel_distance和circumstance