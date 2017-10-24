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

from tkinter import *
import time
import RPi.GPIO as GPIO
import time
import math


class speedometer(object):
  def __init__(self):
    self.root = Tk()
    self.canvas = Canvas(self.root, width = 500, height = 500, bg = 'black')
    self.canvas.pack() 
    self.display = self.canvas.create_oval(25, 25, 475, 475, fill = '#C0C0C0')
    self.display2 = self.canvas.create_oval(50, 50, 450, 450, fill = 'white')
    self.speed_hand = self.canvas.create_line(250, 250, 250, 450, width = '4', fill = 'red')  
    
    self.canvas.create_text(250, 210, text = 'MPH', font = 'helvetica 20 bold')

    for i in range(2,15):
      ang = i * math.pi / 8 
      x = 225 * math.sin(ang) + 250
      y = 225 * math.cos(ang) + 250 
      x1 = 202 * math.sin(ang) + 250 
      y1 = 202 * math.cos(ang) + 250
      self.canvas.create_line(int(x), int(y), int(x1), int(y1))   
    
    count = 60
    for i in range(2,15):
      ang = i * math.pi / 8 
      x1 = 185 * math.sin(ang) + 250 
      y1 = 185 * math.cos(ang) + 250 
      self.canvas.create_text(x1, y1, text= str(count), font = 'helvetica 10 bold') 
      count = count - 5    
    
    for i in range(4,29): 
      ang = i * math.pi / 16 
      x = 225 * math.sin(ang) + 250
      y = 225 * math.cos(ang) + 250 
      x1 = 212 * math.sin(ang) + 250 
      y1 = 212 * math.cos(ang) + 250
      self.canvas.create_line(int(x), int(y), int(x1), int(y1))      

    self.root.after(1 , self.animation)
    self.root.mainloop()   
  
  def animation(self):
    hall = 18
    start = 0
    end = 0
    wheel_c = 82   #in for wheel circumference
    in2mi = 63360  #inches in a mile
    sec2hr = 3600  #seconds in an hour
    velocity = 0
    t1 = self.canvas.create_text(250, 300, font = 'helvetica 20 bold')

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
          x = 200 * math.sin(5.495-.0785*velocity) + 250
          y = (200 * math.cos(5.495-.0785*velocity)) + 250
          self.canvas.coords(self.speed_hand, 250, 250, int(x), int(y))
          
          self.canvas.itemconfig(t1, text = str(velocity))
          self.canvas.update()
              
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
      GPIO.cleanup()        # cleanup all GPIO

speedometer()
