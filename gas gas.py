from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice
import time

bz = OutputDevice(18)
gas = DigitalInputDevice(17)

try:
    while True:
        if gas.value == 0:
            print("gas gas")
            bz.on()
        else:
            print("Ture")
            bz.off()
            
        time.sleep(0.2)
        
except KeyboardInterrupt:
    pass

bz.off()



