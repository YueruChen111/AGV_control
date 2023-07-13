from CO_command import*
from basic_functions import*
import time


#Demo
def test_demo():
    #PLCinit()
    #moveVW(0,0)
    softStartTimerMove(100,0,5)
    print(getLPos())
    time.sleep(3)
    posMove(100,1000)
    time.sleep(1)
    while(getLSpeed()!=0):
        print(getLPos())
        time.sleep(3)
    print(getLPos())
    #posMoveTo(100,1,1,0.1,10)
    #lockBase()
    #breakConnection()
    pass

test_demo()

