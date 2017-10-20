'''

Copyright (c) 2017 Keola Ramirez, Tony Nyguen, Waseem Radi

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import RPi.GPIO as GPIO
import time
import math

hall = 18
start = 0
end = 0
wheel_c = 82   #in for wheel circumference
in2mi = 63360  #inches in a mile
sec2hr = 3600  #seconds in an hour
velocity = 0

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(hall, GPIO.IN) # Hall effect sensor as input

print("Lets begin! Press CTRL+C to exit")

try:
    start = time.time()
    while True:
        
        if GPIO.input(hall) == 0: # Hall effect is triggered
            end = time.time()
            elapsedTime = (end - start)
            start = end
            if elapsedTime < 0.026:
                velocity = 0
                print(velocity)
            else:
                velocity = round((sec2hr/elapsedTime * wheel_c )/in2mi,2)
                print(velocity)
                #print(elapsedTime)
            time.sleep(0.025)
            
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()        # cleanup all GPIO
