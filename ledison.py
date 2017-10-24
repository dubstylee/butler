from tkinter import Tk, Label, Button, Canvas

class Circle:
    def __init__(self, pos, x, y, r, fill, outline, width):
        self.pos = pos
        self.x = x
        self.y = y
        self.r = r
        self.fill = fill
        self.outline = outline
        self.width = width

    def __str__(self):
        return "Circle <%d,%d> radius (%d)" % (self.x, self.y, self.r)

class Ledison:
    leds = []

    def draw_circle(self, c):
        return self.draw_circle_internal(c.x, c.y, c.r, fill=c.fill,
            outline=c.outline, width=c.width)

    def draw_circle_internal(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def __init__(self, master):
        master.title("LEDison")
        self.master = master

        self.canvas = Canvas(master, width=360, height=80, borderwidth=0,
            highlightthickness=0, bg="#DDD")
        self.canvas.grid()


root = Tk()
gui = Ledison(root)
for i in range(0,8):
    gui.leds.append(Circle(i, 40+40*i, 40, 15, fill="#BBB", outline="white",
        width=1))
    gui.draw_circle(gui.leds[i])

for led in gui.leds:
    if led.pos == 0:
        led.fill="red"
        gui.draw_circle(led)

root.mainloop()
