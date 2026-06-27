import time
import subprocess
from gpiozero import Button #helper for reading GPIO input

"""
Shutdown Wacher
- watches GPIO17 and shuts the Pi down after ignition off

GPIO Pinout
1: 3.3V to ADS
3: SDA
5: SCL
6: SDA pair gnd
9: SDA pair gnd
11: GPIO17 (opto OUT)
14: opto pair gnd
17: 3.3V to opto VCC
"""

#==Constants==
IGN_GPIO = 17    #trigger pin
IGN_ON_VALUE = 1 #NEED TO CONFIRM high or low w/ koeo/r

#wait times (in seconds)
STARTUP_GRACE_TIME = 20
OFF_CONFIRM_TIME = 5

igntion = Button(IGN_GPIO, pull_up=True) #set GPIO17 to known default

print("Ignition shutdown watcher starting.")
time.sleep(STARTUP_GRACE_TIME)

off_start = None #instantiate var to hold time off

#signal watcher loop
while True:
    current_value = igntion.value

    #ign off check
    if current_value != IGN_ON_VALUE:
        #begin timer before shut down
        if off_start is None:
            off_start = time.time()
            print("Igniton appears off. Confirming.")

        #begin shutdown after wait period
        elif time.time() - off_start >= OFF_CONFIRM_TIME:
            print("Ignition OFF confirmed. Sutting down.")
            subprocess.run(["sudo", "shutdown", "now"])
            break

    else:
        off_start = None

    time.sleep(1) #check once per second