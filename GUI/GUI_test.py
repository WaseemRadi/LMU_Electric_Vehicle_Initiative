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
from tkinter import ttk
import math
import time
#import RPi.GPIO as GPIO


class Speed(object):
    def __init__(self, root):


        self.root = root

        self.initializeValues()
        self.makeMainFrame()
        self.makeCanvas()
        self.clock()
        self.change_time()

    def initializeValues(self):
        self.speedFont = "helvetica 50 bold"
        self.mphFont = "helvetica 20 bold"
        self.textColor = "white"
        self.markerFont = "helvetica 20 bold"
        self.backGroundColor = "#000000"
        self.outlineColor = "white"
        self.backGroundFillColor = "black"
        self.fillColor = "black"

        self.voltageFont = "helvetica 30 bold"
        self.degree = u'\N{DEGREE SIGN}' + "F"
        self.rangeFont = "helvetica 25 bold"

        self.canvasWidth = 1200
        self.canvasHeight = 500
        self.circleX1 = 325
        self.circleX2 = 775
        self.circleY1 = 25
        self.circleY2 = 475

        self.frame_rate = 80
        self.centerX = 550
        self.centerY = 350
        self.maxSpeed = 60

        self.speed = "0"
        self.power = "0"

        self.voltage = "00.0"
        self.temperature = "000"
        self.range = "000"

        self.tempCounter = 0

        self.scalingFactor = 0.5

    def makeMainFrame(self):
        self.styleName = "TFrame"
        self.style = ttk.Style()
        self.style.configure(self.styleName, background="black")

        self.mainFrame = ttk.Frame(self.root, padding="0 0 0 0", style=self.styleName)
<<<<<<< HEAD
        self.mainFrame.grid(column=1, row=1, sticky=(N, E, W, S))
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.pack(fill = BOTH)
=======
        self.mainFrame.grid(column=3, row=1, sticky=(N, E, W, S))
        self.mainFrame.pack(fill = BOTH, expand = 1)
>>>>>>> fd14045936aaadab14eb4c985643932a167ed7a6

    def makeCanvas(self):
        self.canvas = Canvas(self.mainFrame, background=self.backGroundColor, width=self.canvasWidth, height=self.canvasHeight, bg="black")
        self.canvas.grid(column=0, row=0, sticky=(N, E, W, S))
<<<<<<< HEAD
        self.canvas.bind()
        self.canvas.pack(fill = BOTH)
=======
        self.canvas.pack(fill = BOTH, expand = 1)
>>>>>>> fd14045936aaadab14eb4c985643932a167ed7a6
        # self.hubCircle = self.canvas.create_oval(self.circleX1, self.circleY1, self.circleX2, self.circleY2, outline=self.outlineColor, fill=self.backGroundFillColor)
        self.left_arc = self.canvas.create_arc(75, 40, 500, 465 , start = 55, extent = 250, fill = '#C0C0C0')
        self.left_art2 = self.canvas.create_arc(100, 65, 475, 440, start = 55, extent = 250 ,fill = 'Black')
        self.right_arc = self.canvas.create_arc(600, 40, 1025, 465 , start = -125, extent = 250, fill = '#C0C0C0')
        self.right_art2 = self.canvas.create_arc(625, 65, 1000, 440, start = -125, extent = 250 ,fill = 'Black')
        self.display = self.canvas.create_oval(self.circleX1 , self.circleY1, self.circleX2, self.circleY2, fill = '#C0C0C0')
        self.display2 = self.canvas.create_oval(self.circleX1+25, self.circleY1+25, self.circleX2-25, self.circleY2-25, fill = 'Black')

        self.speedBox = self.canvas.create_rectangle(self.centerX-70, self.centerY-25, self.centerX+70, self.centerY+80, fill='#702B0B', outline='#C0C0C0')

        self.speedText = self.canvas.create_text(self.centerX, self.centerY, text=self.speed, fill=self.textColor, font=self.speedFont)
        self.mphLabel = self.canvas.create_text(self.centerX, self.centerY + 28, text="mph", fill=self.textColor, font='helvetica 16 bold')
        self.powerText = self.canvas.create_text(self.centerX-275, self.centerY, text=self.power, fill=self.textColor, font=self.speedFont)
        self.kwLabel = self.canvas.create_text(self.centerX-275, self.centerY + 28, text="kW", fill=self.textColor, font='helvetica 16 bold')
        self.power_hand = self.canvas.create_line(275, 250, 180*math.sin(5.590) + 275, 180*math.cos(5.590) + 250, width = '4', fill = 'blue')
        self.speed_hand = self.canvas.create_line(550, 250,  200 * math.sin(5.495) + 550,  200 * math.cos(5.495) + 250, width = '4', fill = 'red')

        self.voltageMeter = self.canvas.create_rectangle(775, 105, 875, 145, fill='#702B0B', outline='#C0C0C0')
        self.voltageText = self.canvas.create_text(813, 125, text = self.voltage, fill = self.textColor, font = self.voltageFont)
        self.voltageSymbol = self.canvas.create_text(860, 125, text = "V", fill = self.textColor, font = self.voltageFont)

        self.temperatureMeter = self.canvas.create_rectangle(835, 168, 935, 208, fill='#702B0B', outline='#C0C0C0')
        self.temperatureText = self.canvas.create_text(870, 188, text = self.temperature, fill = self.textColor, font = self.voltageFont)
        self.temperatureSymbol = self.canvas.create_text(915, 188, text = self.degree, fill = self.textColor, font = self.voltageFont)

        self.rangeMeter = self.canvas.create_rectangle(800, 230, 975, 270, fill='#702B0B', outline='#C0C0C0')
        self.rangeText = self.canvas.create_text(870, 250, text = "Range: " + self.range, fill = self.textColor, font = self.rangeFont)
        self.rangeSymbol = self.canvas.create_text(955, 250, text = "mi", fill = self.textColor, font = self.rangeFont)

        self.canvas.add_tag("all")
        for i in range(2,15):
          ang = i * math.pi / 8
          x = 212 * math.sin(ang) + 550
          y = 212 * math.cos(ang) + 250
          x1 = 200 * math.sin(ang) + 550
          y1 = 200 * math.cos(ang) + 250
          x_arc = 200 * math.sin(ang) + 290
          y_arc = 212 * math.cos(ang) + 255
          x1_arc = 200 * math.sin(ang) + 290
          y1_arc = 200 * math.cos(ang) + 255
        #   if i > 6:
        #       self.canvas.create_line(int(x_arc), int(y_arc), int(x1_arc), int(y1_arc), fill ='white')
          self.canvas.create_line(int(x), int(y), int(x1), int(y1), fill ='white')

        count = 60
        power_count = 30
        for i in range(2,15):
          ang = i * math.pi / 8
          x1 = 185 * math.sin(ang) + 550
          y1 = 185 * math.cos(ang) + 250
          x_arc = 175 * math.sin(ang) + 290
          y_arc = 175 * math.cos(ang) + 255
          if i > 7:
              self.canvas.create_text(x_arc, y_arc, fill = 'white', text = str(count), font = self.markerFont)
          canvas_id = self.canvas.create_text(x1, y1, fill = 'white', font = self.markerFont)
          self.canvas.itemconfig(canvas_id, text= str(count))
          count = count - 5

        for i in range(3,30):
          ang = i * math.pi / 16
          x = 222 * math.sin(ang) + 550
          y = 222 * math.cos(ang) + 250
          x1 = 210 * math.sin(ang) + 550
          y1 = 210 * math.cos(ang) + 250
          x_arc = 212 * math.sin(ang) + 290
          y_arc = 212 * math.cos(ang) + 255
          x1_arc = 200 * math.sin(ang) + 290
          y1_arc = 200 * math.cos(ang) + 255
          if i > 13:
              self.canvas.create_line(int(x_arc), int(y_arc), int(x1_arc), int(y1_arc), fill ='white')
          self.canvas.create_line(int(x), int(y), int(x1), int(y1),fill='white')

    def clock(self):
        self.time = time.strftime('%m/%d/%Y     %I:%M')
        self.watch = self.canvas.create_text(self.centerX, self.centerY+70, text = self.time, font = 'helvetica 15 bold', fill = 'white')
        self.root.after(200, self.change_time)

    def change_time(self):
        self.time2 = time.strftime('%m/%d/%Y     %I:%M')
        self.canvas.itemconfig(self.watch, text = self.time2)
        self.root.after(200, self.change_time)

    def updateSpeed(self):
        hall = 18
        start = 0
        end = 0
        wheel_c = 82   #in for wheel circumference
        in2mi = 63360  #inches in a mile
        sec2hr = 3600  #seconds in an hour
        velocity = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(hall, GPIO.IN) # Hall effect sensor as input
        try:
            start = time.time()
            while True:
                if GPIO.input(hall) == 0: # Hall effect is triggered
                    end = time.time()
                    elapsedTime = (end - start)
                    start = end
                    if elapsedTime < 0.08:
                        velocity = 0
                        #print(velocity)
                        x = 200 * math.sin(5.495) + 550
                        y = 200 * math.cos(5.495) + 250
                        time.sleep(.05)
                        self.canvas.coords(self.speed_hand, 550, 250, int(x), int(y))
                        self.canvas.itemconfigure(self.speedText, text=str(math.floor(velocity)))
                        self.canvas.update()
                    else:
                        velocity = round((sec2hr/elapsedTime * wheel_c )/in2mi,2)
                        print(velocity)
                        #print(elapsedTime)
                        time.sleep(0.025)
                        x = 200 * math.sin(5.495-.0785*velocity) + 550
                        y = 200 * math.cos(5.495-.0785*velocity) + 250
                        self.canvas.coords(self.speed_hand, 550, 250, int(x), int(y))
                        self.canvas.itemconfigure(self.speedText, text=str(math.floor(velocity)))
                        time.sleep(.05)
                        self.canvas.update()
        except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
            GPIO.cleanup()        # cleanup all GPIO

        except ValueError:
            pass

    def updateRPM(self, pRPM=None):
        if pRPM is None:
            try:
                self.tempCounter += 1

                if (self.tempCounter > self.maxSpeed):
                    self.tempCounter = self.maxSpeed
                if (self.tempCounter < 0):
                    self.tempCounter = 0

                self.speed = str(self.tempCounter)
                self.canvas.itemconfigure(self.speedText, text=self.speed)
                self.canvas.update()
            except ValueError:
                pass
        else:
            try:
                self.canvas.itemconfigure(self.mphLabel, text=str(pRPM))
                self.canvas.update()
            except ValueError:
                pass
        self.root.after(self.frame_rate, self.updateRPM)

root = Tk()
<<<<<<< HEAD
root.tk.call('tk','scaling',1)
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width,height))
=======
root.tk.call('tk','scaling',1.85)
>>>>>>> fd14045936aaadab14eb4c985643932a167ed7a6
dash = Speed(root)
print("Lets begin! Press CTRL+C to exit")
#dash.root.after(1,dash.updateSpeed)
dash.root.mainloop()
