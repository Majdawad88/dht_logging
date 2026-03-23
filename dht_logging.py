#git clone https://github.com/Majdawad88/dht_logging.git

import RPi.GPIO as GPIO
import dht11
import time
from datetime import datetime

dataPin = 4
# Create filename once at start
fileName = 'dhtlog_' + datetime.now().strftime("%m-%d-%y-%H-%M-%S") + '.txt'

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialize sensor ONCE outside the loop
instance = dht11.DHT11(pin=dataPin)

# Initial header write
with open(fileName, 'a') as f:
    f.write('timestamp, temp, humid\n')

print(f"Logging data to {fileName}...")

try:
    while True:
        result = instance.read()

        if result.is_valid():
            # SUCCESS: Process and log data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            temp = result.temperature
            humid = result.humidity

            print(f"[{timestamp}] Temp: {temp:.1f} C | Humid: {humid:.1f}%")

            # Write to log file
            with open(fileName, 'a') as f:
                f.write(f'{timestamp}, {temp:.1f}, {humid:.1f}\n')

            # Wait the full 5 seconds ONLY after a successful read
            time.sleep(5)

        else:
          
            # Try again in 0.1s to get a valid reading ASAP.
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nLogging stopped by user. Cleaning up GPIO...")
    GPIO.cleanup()

   # Wait 1 seconds before taking the next sensor reading
   time.sleep(1)

