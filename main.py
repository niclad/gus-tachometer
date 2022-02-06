'''
  _____                                                  
 / ___/ __ __  ___                                       
/ (_ / / // / (_-<                                       
\___/__\_,_/ /___/   __                    __            
/_  __/ ___ _ ____  / /  ___   __ _  ___  / /_ ___   ____
 / /   / _ `// __/ / _ \/ _ \ /  ' \/ -_)/ __// -_) / __/
/_/    \_,_/ \__/ /_//_/\___//_/_/_/\__/ \__/ \__/ /_/   

A tachometer for a lil hedgehog
'''

import datetime
import math
import time
import RPi.GPIO as GPIO

# GLOBAL VARIABLES
GPIO_PIN = 17
IS_SWITCHED = False
REVOLUTIONS = 0
TIME_STAMPS = []
START_TIME = time.time()

def sensorCallback(channel):
    '''
    Called if the sensor output changes
    '''
    global IS_SWITCHED
    global REVOLUTIONS
    global TIME_STAMPS
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    if GPIO.input(channel):
        # No magnet
        print("Sensor HIGH " + stamp)
    else:
        if not IS_SWITCHED:
            REVOLUTIONS += 1
            TIME_STAMPS.append(time.time() - START_TIME)

        # Magnet
        print("Sensor LOW " + stamp)

def main():
    '''
    Run the tachometer set to the defined GPIO pin
    '''
    # Get initial reading
    sensorCallback(GPIO_PIN)

    # set up the timer
    secsInHr = 3600
    secsInDay = secsInHr * 24
    timeElapsed = time.time() - START_TIME

    wheelDiameter = 12 # in inches
    wheelCircum = wheelDiameter * math.pi * 2
    
    # loop checking for keyboard interrupt
    try:
        while True and (timeElapsed <= secsInDay):
            timeElapsed = time.time() - START_TIME
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Program interupted!')

    # Reset GPIO settings
    print('Cleaning GPIO')
    GPIO.cleanup()

if __name__ == "__main__":
    # Tell GPIO library to use GPIO references
    GPIO.setmode(GPIO.BCM)

    print(    
'''  _____                                                  
 / ___/ __ __  ___                                       
/ (_ / / // / (_-<                                       
\___/__\_,_/ /___/   __                    __            
/_  __/ ___ _ ____  / /  ___   __ _  ___  / /_ ___   ____
 / /   / _ `// __/ / _ \/ _ \ /  ' \/ -_)/ __// -_) / __/
/_/    \_,_/ \__/ /_//_/\___//_/_/_/\__/ \__/ \__/ /_/   

Setup GPIO pin as input on GPIO17
'''
    )

    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_PIN, GPIO.BOTH, callback=sensorCallback, bouncetime=200)
    main()