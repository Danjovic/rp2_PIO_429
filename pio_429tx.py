# Danjovic 2024
# Released under GPL V3.0
# PIO code to send Arinc 429 data using HOLT HI-8585 drivers - 8 Instructions, 1 State Machine

# low speed: 12.500 bits/second
# high speed 100.000 bits/second
# every bit is half time on half time off
# at the end, there should be at least 3 bit bimes off

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

 
PIN_BASE = 28
FREQ=100000
 
@asm_pio(set_init=(rp2.PIO.OUT_LOW,rp2.PIO.OUT_LOW), out_shiftdir=PIO.SHIFT_LEFT, autopull=True)

# 4 cycles per half bit time, 8 cycles per bit
# frequ base for 12.5  kbps -> 8 * 12.5 KHz = 100KHz
#                100   kbps -> 8 * 100 Khz  = 800Khz   

def txA429():  
    set (y,31)  [31]              # wait at least 4 bit times before send (32 cycles)
    label("sendBit")                              
    out (x,1)                     #       3          
    jmp (not_x,"sendZero")        #       4          
    set (pins,0b01)       [2]     #   3           
    jmp ("turnOff")               #   4           
    label("sendZero")             #               
    set (pins,0b10)       [3]     #            4   
    label("turnOff")              #               
    set (pins,0b00)               #   1        1  
    jmp (y_dec,"sendBit")         #   2        2  

                                         

    
# Initialize State Machine, with base clock = 100kHz for Arinc Low Speed or 800KHz for Arinc High Speed.
sm = StateMachine(1, txA429, freq=FREQ, set_base=Pin(PIN_BASE) )
sm.active(1)

# calculate parity
def parity(x):
    res = 0
    while x:
        res ^= x & 1
        x >>= 1
    return res

   
# Send message. 
for i in range(5):
     sm.put(0x8e10c000)
   
    
