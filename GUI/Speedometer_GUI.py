from tkinter import *
import math
import time

class speedometer(object):
  def __init__(self):
    self.root = Tk()
    self.canvas = Canvas(self.root, width = 500, height = 500, bg = 'black')
    self.canvas.pack()
    self.display = self.canvas.create_oval(25, 25, 475, 475, fill = '#C0C0C0')
    self.display2 = self.canvas.create_oval(50, 50, 450, 450, fill = 'white')
    self.speed_hand = self.canvas.create_line(250, 250, 250, 450, width = '4', fill = 'blue')

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
      canvas_id = self.canvas.create_text(x1, y1)
      self.canvas.itemconfig(canvas_id, text= str(count))
      count = count - 5

    for i in range(3,30):
      ang = i * math.pi / 16
      x = 225 * math.sin(ang) + 250
      y = 225 * math.cos(ang) + 250
      x1 = 212 * math.sin(ang) + 250
      y1 = 212 * math.cos(ang) + 250
      self.canvas.create_line(int(x), int(y), int(x1), int(y1))

    self.root.after(1 , self.animation)
    self.root.mainloop()

  def animation(self):
    while 1 == 1:
      for angle in range(350, 35, -1):
        time.sleep(.025)
        x = 200 * math.sin(math.pi * angle / 192) + 250
        y = (200 * math.cos(math.pi * angle / 192)) + 250
        self.canvas.coords(self.speed_hand, 250, 250, int(x), int(y))
        self.canvas.update()

speedometer()
