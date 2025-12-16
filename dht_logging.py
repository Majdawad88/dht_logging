#git clone https://github.com/Majdawad88/dht_logging.git

import RPi.GPIO as GPIO
import dht11
import time
from datetime import datetime

dataPin = 4

fileName = 'dhtlog_' + datetime.now().strftime("%m-%d-%y-%H-%M-%S") + '.txt'

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Initial header write
with open(fileName, 'a') as f:
   f.write('timestamp, temp, humid')

while True:

   # read data using pin 4
   instance = dht11.DHT11(pin = dataPin)
   result = instance.read()

   if result.is_valid():
       # Timestamp to record the temporal information of the reading.
       # Format: Month-Day-Year-Hour-Minute-Second.
       timestamp = datetime.now().strftime("%m-%d-%y-%H-%M-%S")

       # Unpack the reading.
       temp = result.temperature
       humid = result.humidity
       
       # Output only if the reading was successful
       print("Temperature: %-3.1f C" % temp)
       print("Humidity: %-3.1f %%" % humid)
       
       # Write the readings to a log file
       with open(fileName, 'a') as f:
           f.write('\n%s,%s,%s' % (timestamp, temp, humid))
  
   else:
       print("Error: %d" % result.error_code)

   # Wait 5 seconds before taking the next sensor reading
   time.sleep(5)

