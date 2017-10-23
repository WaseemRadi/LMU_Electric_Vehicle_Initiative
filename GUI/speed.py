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

class Speed(object):
    def __init__(self, root):

        self.root = root

        self.initializeValues()
        self.makeMainFrame()
        self.makeCanvas()

    def initializeValues(self):
        self.speedFont = "helvetica 50 bold"
        self.kphFont = "helvetica 20 bold"
        self.textColor = "white"

        self.backGroundColor = "#000000"
        self.outlineColor = "white"
        self.backGroundFillColor = "black"
        self.fillColor = "black"

        self.canvasWidth = 500
        self.canvasHeight = 500
        self.circleX1 = 25
        self.circleX2 = 475
        self.circleY1 = 25
        self.circleY2 = 475

        self.frame_rate = 80
        self.centerX = 250
        self.centerY = 350
        self.maxSpeed = 60

        self.speed = ""

        self.tempCounter = 0  # TODO m: this will be the charge count; for now its a temp counter

    def makeMainFrame(self):
        self.styleName = "TFrame"
        self.style = ttk.Style()
        self.style.configure(self.styleName, background="black")

        self.mainFrame = ttk.Frame(self.root, padding="0 0 0 0", style=self.styleName)
        self.mainFrame.grid(column=1, row=2, sticky=(N, E, W, S))

    def makeCanvas(self):
        self.canvas = Canvas(self.mainFrame, background=self.backGroundColor, width=self.canvasWidth, height=self.canvasHeight, bg="black")
        self.canvas.grid(column=0, row=0, sticky=(N, E, W, S))
        self.hubCircle = self.canvas.create_oval(self.circleX1, self.circleY1, self.circleX2, self.circleY2, outline=self.outlineColor, fill=self.backGroundFillColor)
        self.display = self.canvas.create_oval(25, 25, 475, 475, fill = '#C0C0C0')
        self.display2 = self.canvas.create_oval(50, 50, 450, 450, fill = 'Black')
        self.speedText = self.canvas.create_text(self.centerX, self.centerY, text=self.speed, fill=self.textColor, font=self.speedFont)
        self.kphLabel = self.canvas.create_text(self.centerX, self.centerY + 40, text="kph", fill=self.textColor, font=self.kphFont)
        self.speed_hand = self.canvas.create_line(250, 250, 250, 450, width = '4', fill = 'white')

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
          canvas_id = self.canvas.create_text(x1, y1, fill = 'white')
          self.canvas.itemconfig(canvas_id, text= str(count))
          count = count - 5

        for i in range(3,30):
          ang = i * math.pi / 16
          x = 225 * math.sin(ang) + 250
          y = 225 * math.cos(ang) + 250
          x1 = 212 * math.sin(ang) + 250
          y1 = 212 * math.cos(ang) + 250
          self.canvas.create_line(int(x), int(y), int(x1), int(y1))

    def updateSpeed(self, pSpeed=None):
        if pSpeed is None:
            try:
                self.tempCounter += 1

                if (self.tempCounter > self.maxSpeed):
                    self.tempCounter = self.maxSpeed
                if (self.tempCounter < 0):
                    self.tempCounter = 0

                self.speed = str(self.tempCounter)
                # self.canvas.itemconfigure(self.speedText, text=self.speed)
                # time.sleep(.025)
                # x = 200 * math.sin(math.pi * self.tempCounter*5.25/ 192) + 250
                # y = (200 * math.cos(math.pi * self.tempCounter*5.25/ 192)) + 250
                # self.canvas.coords(self.speed_hand, 250, 250, int(x), int(y))
                # self.canvas.update()

            except ValueError:
                pass
        else:
            try:
                self.canvas.itemconfigure(self.speedText, text=str(pSpeed))
                time.sleep(.05)
                x = 200 * math.sin(5.495-.0785*pSpeed) + 250
                y = (200 * math.cos(5.495-.0785*pSpeed)) + 250
                self.canvas.coords(self.speed_hand, 250, 250, int(x), int(y))
                self.canvas.update()
            except ValueError:
                pass
        self.root.after(self.frame_rate, self.updateSpeed)

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
                self.canvas.itemconfigure(self.kphLabel, text=str(pRPM))
                self.canvas.update()
            except ValueError:
                pass
        self.root.after(self.frame_rate, self.updateRPM)

dash = Speed(Tk())
dash.updateSpeed(pSpeed = 0)
dash.updateSpeed(pSpeed = 1)
dash.updateSpeed(pSpeed = 2)
dash.updateSpeed(pSpeed = 5)
dash.updateSpeed(pSpeed = 8)
dash.updateSpeed(pSpeed = 10)
dash.updateSpeed(pSpeed = 13)
dash.updateSpeed(pSpeed = 15)
dash.updateSpeed(pSpeed = 20)
dash.updateSpeed(pSpeed = 24)
dash.updateSpeed(pSpeed = 27)
dash.updateSpeed(pSpeed = 30)
dash.updateSpeed(pSpeed = 33)
dash.updateSpeed(pSpeed = 35)
dash.root.mainloop()
