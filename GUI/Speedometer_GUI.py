from tkinter import *
import math
import time

class speedometer(object):
  def __init__(self):
    self.root = Tk()
    self.canvas = Canvas(self.root, width = 500, height = 500)
    self.canvas.pack() 
    self.display = self.canvas.create_oval(50, 50, 450, 450)
    self.speed_hand = self.canvas.create_line(250, 250, 250, 450)
    self.root.after(1 , self.animation)
    self.root.mainloop()  
  def animation(self):
    for angle in range(400, 0, -1):
      time.sleep(.025)
      x = 200 * math.sin(math.pi * angle / 192) + 250
      y = (200 * math.cos(math.pi * angle / 192)) + 250
      print(x, y)
      self.canvas.coords(self.speed_hand, 250, 250, int(x), int(y))
      self.canvas.update()
        
speedometer()
