import socket, os
import subprocess 
import time

leftID = 2
rightID = 3
filePath = "/home"
circumference = 518.1
# initialize PLC
def PLCinit():
    activate = "sudo ip link set up can0 type can bitrate 500000\n" 
    os.system("gnome-terminal -e 'bash -c \""+activate+";bash\"'")
    time.sleep(1)    

    # makefile
    make = "cd "+filePath+"/CANopenLinux\n" + "make" 
    os.system("gnome-terminal -e 'bash -c \""+make+";bash\"'")
    time.sleep(5)

    
    openClient = "canopend can0 -i 1 -c 'local-/tmp/CO_command_socket'" 
    process0 = subprocess.Popen(
        "gnome-terminal -e 'bash -c \""+openClient+";bash\"'",
        stdout=subprocess.PIPE,
        stderr=None,
        shell=True
    )

#send cocomm message
def sendMsg(msg): 
    if os.path.exists("/tmp/CO_command_socket"):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect("/tmp/CO_command_socket")
        x = "[1] " + msg + "\r\n"
        if "" != x:
            print("SEND:", x.encode("utf-8"))
            client.send(x.encode("utf-8"))
            recv = bytes()
            while True:
                data = client.recv(1024)
                recv += data
                if len(data) < 1024:
                    break
        
            print("RECEIVE:", recv)
        
        client.close()
        
    else:
        print("Couldn't Connect!")
        recv = "Couldn't Connect"
    return recv


# speed mode via SDO, n for node_id, v on rpm 
def speedMode(n, v): 
    sendMsg("set node "+str(n))
    sendMsg("w 0x6060 00 i8 -3")
    sendMsg("w 0x6040 00 u16 0xF")
    sendMsg("w 0x60FF 00 i32 "+str(int(v*2731)))

# soft start mode
def speedMode_soft(n, v):
    sendMsg("set node "+str(n))
    sendMsg("w 0x6060 00 i8 3")
    sendMsg("w 0x6040 00 u16 0xF")
    sendMsg("w 0x60FF 00 i32 "+str(int(v*2731)))
  
    # sendMsg("w 0x6083 00 i64 100")
    # sendMsg("w 0x6084 00 i64 100")

# position mode via SDO, n for node_id, v on rpm, dis on mm
def positionMode(n, v, dis):
    pos = getPos(n)
    sendMsg("set node "+str(n))
    sendMsg("w 0x6060 00 i8 1")
    sendMsg("w 0x6040 00 u16 0x103F")
    sendMsg("w 0x6081 00 i32 273100") 
    sendMsg("w 0x60FF 00 i32 "+str(int(v*2731))) 
    sendMsg("w 0x607A 00 i32 "+str(int((dis+pos)/circumference*90000))) 

# set speed
def setSpeed(vl,vr):
    speedMode(leftID,vl)
    speedMode(rightID,vr)

# set speed on soft-start-mode
def softsetSpeed(vl,vr):
    speedMode_soft(leftID,vl)
    speedMode_soft(rightID,vr)

# brake
def lockBase():
    sendMsg("set node " + str(leftID))
    sendMsg("w 0x6040 00 u16 0x6")
    sendMsg("set node " + str(rightID))
    sendMsg("w 0x6040 00 u16 0x6")

def getPos(n):
    sendMsg("set node " + str(n))
    pos_msg = sendMsg("r 0x6063 00 i32")
    pos = (int(pos_msg[4:-1]))*circumference/90000
    return pos

# left wheel actual position(mm)
def getLPos():
    sendMsg("set node " + str(leftID))
    pos_msg = sendMsg("r 0x6063 00 i32")
    pos = (int(pos_msg[4:-1]))*circumference/90000
    return pos

# left wheel actual speed(rpm)
def getLSpeed():
    sendMsg("set node " + str(leftID))
    speed_msg = sendMsg("r 0x606C 00 i32")
    speed = (int(speed_msg[4:-1]))/2731
    return speed

# right wheel actual position(mm)
def getRPos():
    sendMsg("set node " + str(rightID))
    pos_msg = sendMsg("r 0x6063 00 i32")
    pos = (int(pos_msg[4:-1]))*circumference/90000
    return pos

# right wheel actual speed(rpm)
def getRSpeed():
    sendMsg("set node " + str(rightID))
    speed_msg = sendMsg("r 0x606C 00 i32")
    speed = (int(speed_msg[4:-1]))/2731
    return speed

# break connection safely (don't stop Terminal directly!)
def breakConnection():
    sendMsg("0 reset node")


# sendMsg("set node 2")
# sendMsg("r 0x6063 00 i32")
# sendMsg("w 0x6060 00 i8 1")
# sendMsg("w 0x6040 00 u16 0x103F")
# sendMsg("w 0x6081 00 i32 273100") 
# sendMsg("w 0x60FF 00 i32 273100") 
# sendMsg("w 0x607A 00 i32 1899381") 

