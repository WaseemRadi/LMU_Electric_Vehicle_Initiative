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
import smbus
import serial
import re
import RPi.GPIO as GPIO
import random
import Adafruit_ADS1x15
import sys
import Adafruit_DHT


class Speed(object):
    def __init__(self, root):
        self.root = root
        self.initializeValues()
        self.makeMainFrame()
        self.makeCanvas()
        self.clock()
        self.change_time()
        self.date()
        self.change_date()
        self.updateVoltage()
        self.updateTemperature()
        self.isError()
        self.updateSpeed()
        

    def initializeValues(self):
        self.speedFont = "helvetica 45 bold"
        self.mphFont = "helvetica 10 bold"
        self.textColor = "white"
        self.markerFont = "helvetica 15 bold"
        self.backGroundColor = "#000000"
        self.outlineColor = "white"
        self.backGroundFillColor = "black"
        self.fillColor = "black"
        self.errorColor = "yellow"

        self.canvasWidth = 800 
        self.canvasHeight = 450
        self.circleX1 = 225   
        self.circleX2 = 575
        self.circleY1 = 50
        self.circleY2 = 400

        self.frame_rate = 80
        self.centerX = 400
        self.centerY = 240
        self.maxSpeed = 60

        self.speed = "0"
        self.power = "0"
        self.degree = u'\N{DEGREE SIGN}' + "F"
        self.voltage = "00.0"
        self.temperature = "000"
        self.range = "000"

        self.tempCounter = 0
        
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1

    def makeMainFrame(self):
        self.styleName = "TFrame"
        self.style = ttk.Style()
        self.style.configure(self.styleName, background="black")

        self.mainFrame = ttk.Frame(self.root, padding="0 0 0 0", style=self.styleName)
        self.mainFrame.grid(column=3, row=1, sticky=(N, E, W, S))

    def makeCanvas(self):
        self.canvas = Canvas(self.mainFrame, background=self.backGroundColor, width=self.canvasWidth, height=self.canvasHeight, bg="black")
        self.canvas.grid(column=0, row=0, sticky=(N, E, W, S))
        self.leftDialBorder = self.canvas.create_oval(25, 50, 375, 400, fill = '#C0C0C0')
        self.leftDialCenter = self.canvas.create_oval(50, 75, 350, 375, fill = 'Black') 
        self.rightDialBorder = self.canvas.create_oval(425, 50, 775, 400, fill = '#C0C0C0')
        self.rightDialCenter =  self.canvas.create_oval(450, 75, 750, 375, fill = 'Black')
        self.centerDialBorder = self.canvas.create_oval(self.circleX1, self.circleY1, self.circleX2, self.circleY2, fill = '#C0C0C0')
        self.centerDialCenter = self.canvas.create_oval(self.circleX1+25, self.circleY1+25, self.circleX2-25, self.circleY2-25, fill = 'Black')

        self.speedBox = self.canvas.create_rectangle(self.centerX-40, self.centerY-103, self.centerX+40, self.centerY-28, fill='#702B0B', outline='#C0C0C0')

        self.speedText = self.canvas.create_text(self.centerX, self.centerY - 72, text=self.speed, fill=self.textColor, font=self.speedFont)
        self.mphLabel = self.canvas.create_text(self.centerX, self.centerY - 42, text="mph", fill=self.textColor, font=self.mphFont)
        
        self.powerText = self.canvas.create_text(self.centerX-200, self.centerY + 60, text=self.power, fill=self.textColor, font=self.speedFont)
        self.kwLabel = self.canvas.create_text(self.centerX-200, self.centerY + 90, text="kW", fill=self.textColor, font=self.mphFont)

        self.power_hand = self.canvas.create_line(200, 225, 150*math.sin(5.495) + 200, 150*math.cos(5.495) + 225, width = '4', fill = 'blue')
        self.speed_hand = self.canvas.create_line(400, 225, 150 * math.sin(5.495) + 400,  150 * math.cos(5.495) + 225, width = '4', fill = 'red')

        self.timeBox = self.canvas.create_rectangle(self.centerX-52, self.centerY+55, self.centerX+52, self.centerY+120, fill='#702B0B', outline='#C0C0C0')
        self.errorText = self.canvas.create_text(self.centerX, self.centerY + 70, text = '', fill = self.errorColor, font = "helvetica 12 bold")
        
        self.voltageBox = self.canvas.create_rectangle(570, 105, 670, 145, fill='#702B0B', outline='#C0C0C0')
        self.voltageText = self.canvas.create_text(607, 125, text = self.voltage, fill = self.textColor, font = "helvetica 24 bold")
        self.voltageSymbol = self.canvas.create_text(655, 125, text = "V", fill = self.textColor, font = "helvetica 24 bold")

        self.temperatureBox = self.canvas.create_rectangle(605, 165, 705, 205, fill='#702B0B', outline='#C0C0C0')
        self.temperatureText = self.canvas.create_text(638, 185, text = self.temperature, fill = self.textColor, font = "helvetica 24 bold")
        self.temperatureSymbol = self.canvas.create_text(685, 185, text = self.degree, fill = self.textColor, font = "helvetica 24 bold")

        self.rangeBox = self.canvas.create_rectangle(590, 225, 735, 265, fill='#702B0B', outline='#C0C0C0')
        self.rangeText = self.canvas.create_text(630, 245, text = "Range: ", fill = self.textColor, font = "helvetica 16")
        self.rangeValue = self.canvas.create_text(685, 245, text = self.range, fill = self.textColor, font = "helvetica 18 bold")
        self.rangeSymbol = self.canvas.create_text(720, 245, text = "mi", fill = self.textColor, font = "helvetica 16")
 
        count = 60
        for i in range(2,15):
            ang = i * math.pi / 8 
            x = 175 * math.sin(ang) + 400
            y = 175 * math.cos(ang) + 225 
            x1 = 149 * math.sin(ang) + 400 
            y1 = 149 * math.cos(ang) + 225
            x2 = 135 * math.sin(ang) + 400 
            y2 = 135 * math.cos(ang) + 225 
          
            self.canvas.create_line(int(x), int(y), int(x1), int(y1)) 
            self.canvas.create_text(x2, y2, text= str(count), font = 'helvetica 22 bold', fill = 'white')   
            count -= 5

        for i in range(4,29):
            ang = i * math.pi / 16
            x = 175 * math.sin(ang) + 400
            y = 175 * math.cos(ang) + 225
            x1 = 160 * math.sin(ang) + 400
            y1 = 160 * math.cos(ang) + 225
            self.canvas.create_line(int(x), int(y), int(x1), int(y1))

        count = 60
        for i in range(1, 8):
            ang = i * math.pi / 4
            x = 175 * math.sin(ang) + 200
            y = 175 * math.cos(ang) + 225 
            x1 = 149 * math.sin(ang) + 200
            y1 = 149 * math.cos(ang) + 225
            x2 = 135 * math.sin(ang) + 200 
            y2 = 135 * math.cos(ang) + 225 
          
            self.canvas.create_line(int(x), int(y), int(x1), int(y1)) 
            if i > 3:
                self.canvas.create_text(x2, y2, text= str(count), font = 'helvetica 25 bold', fill = 'white')   
            count -= 10


        for i in range(16,29):
            ang = i * math.pi / 16
            x = 175 * math.sin(ang) + 200
            y = 175 * math.cos(ang) + 225
            x1 = 160 * math.sin(ang) + 200
            y1 = 160 * math.cos(ang) + 225
            self.canvas.create_line(int(x), int(y), int(x1), int(y1))

    def clock(self):
        self.time = time.strftime('%m/%d/%Y     %I:%M')
        self.watch = self.canvas.create_text(self.centerX, self.centerY+90, text = self.time, font = 'helvetica 14 bold', fill = 'white')
        self.root.after(80, self.change_time)

    def change_time(self):
        self.time2 = time.strftime('%I:%M')
        self.canvas.itemconfig(self.watch, text = self.time2)
        self.root.after(80, self.change_time)

    def date(self):
        self.day = time.strftime('%m/%d/%Y')
        self.calendar = self.canvas.create_text(self.centerX, self.centerY+110, text = self.day, font = 'helvetica 14 bold', fill = 'white')
        self.root.after(80, self.change_date)

    def change_date(self):
        self.day2 = time.strftime('%m/%d/%Y')
        self.canvas.itemconfig(self.day, text = self.day2)
        self.root.after(80, self.change_date)
    
    def updateVoltage(self):
        value = float(self.adc.read_adc(0, gain=self.GAIN))
        self.voltage = (value / 8032) * 10

        self.canvas.itemconfigure(self.voltageText, text=("%.1f" % self.voltage))
        self.canvas.update()
        self.root.after(30, self.updateVoltage)
        
    def updateTemperature(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(11,4)
        self.temperature = self.temperature * 9 / 5 + 32
        self.canvas.itemconfigure(self.temperatureText, text=('{0:0.1f}'.format(self.temperature)))
        self.canvas.update()
        self.root.after(60, self.updateTemperature)    
    
    def isError(self):
        
        
        if self.voltage <= 9.5 and self.temperature >=75.0:
            self.canvas.itemconfigure(self.errorText, text = 'Low V High T', font = "helvetica 11 bold")
        elif self.temperature >= 75.0:
            self.canvas.itemconfigure(self.errorText, text = 'High Temp')
        elif self.voltage <= 9.5:
            self.canvas.itemconfigure(self.errorText, text = 'Low Voltage')
        else:
            self.canvas.itemconfigure(self.errorText, text = '')
        self.canvas.update()
        self.root.after(60, self.isError)
        
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
            tempStart = time.time()
            
            i = 0
            while i < 50:
##                
                
                if GPIO.input(hall) == 0: # Hall effect is triggered
                    end = time.time()
                    elapsedTime = (end - start)
                    
                    start = end
                    print(elapsedTime)

                    if elapsedTime < 0.040:
                        velocity = 0
                        print(velocity)
                        x = 150 * math.sin(5.495) + 400
                        y = 150 * math.cos(5.495) + 225
                        self.canvas.coords(self.speed_hand, 400, 225, int(x), int(y))
                        self.canvas.itemconfigure(self.speedText, text=str(math.floor(velocity)))
                        self.canvas.update()

                    else:
                        
                        velocity = round((sec2hr/elapsedTime * wheel_c )/in2mi,2)
                        print(velocity)
                        x = 150 * math.sin(5.495-.0785*velocity) + 400
                        y = 150 * math.cos(5.495-.0785*velocity) + 225
                        self.canvas.coords(self.speed_hand, 400, 225, int(x), int(y))
                        self.canvas.itemconfigure(self.speedText, text=str(math.floor(velocity)))
                        #time.sleep(.05)
                        self.canvas.update()
                    i+=1    
                    time.sleep(0.015)
                else:
                    tempEnd = time.time()    
                    tempElapsed = tempEnd - start
                    if tempElapsed > 3.0:
                        velocity = 0
                        x = 150 * math.sin(5.495) + 400
                        y = 150 * math.cos(5.495) + 225
                        self.canvas.coords(self.speed_hand, 400, 225, int(x), int(y))
                        self.canvas.itemconfigure(self.speedText, text=str(math.floor(velocity)))
                        self.canvas.update()
                
                
            self.root.after(10,self.updateSpeed)    
                       
        except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
            GPIO.cleanup()        # cleanup all GPIO

        except ValueError:
            pass
    

root = Tk()
#root.tk.call('tk','scaling',1.85)
dash = Speed(root)
print("Lets begin! Press CTRL+C to exit")
##dash.root.after(1,dash.updateVoltage)
dash.root.mainloop()

