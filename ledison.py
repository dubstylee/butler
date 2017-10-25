import Tkinter as tk
from shared import mqtt_client, mqtt_topic, send_message, ON, OFF


leds = []


class Circle:
    off_color = "#BBB"
    status = OFF

    def __init__(self, gui, pos, x, y, r, fill, outline, width):
        self.gui = gui
        self.pos = pos
        self.x = x
        self.y = y
        self.r = r
        self.on_color = fill
        self.fill = fill
        self.outline = outline
        self.width = width

    def __str__(self):
        return "Circle <%d,%d> radius (%d)" % (self.x, self.y, self.r)

    def write(self, status):
        self.status = status
        if self.status == ON:
            self.fill = self.on_color
        elif status == OFF:
            self.fill = self.off_color
        self.gui.draw_circle(self)
        self.gui.update()


class Ledison(tk.Frame):
    def draw_circle(self, c):
        return self.draw_circle_internal(c.x, c.y, c.r, fill=c.fill,
                                         outline=c.outline, width=c.width)

    def draw_circle_internal(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("LEDison")
        self.master = master
        self.canvas = tk.Canvas(master, width=360, height=80, borderwidth=0,
                                highlightthickness=0, bg="#DDD")
        self.canvas.grid()
        self._job = None


def on_message(client, userdata, msg):
    print (msg.payload)

    splits = msg.payload.split(' ')

    if splits[3] == "Fork":
        led_no = int(splits[8][1:])
        if leds[led_no].status == ON:
            leds[led_no].write(OFF)
        else:
            leds[led_no].write(ON)

# def ledison_loop(gui):
#    for i in range(0,3):
#        for led in gui.leds:
#            led.write(0)
#        time.sleep(0.1)
#        for led in gui.leds:
#            led.write(1)
#        time.sleep(0.1)
#    time.sleep(1.0)

#    for led in gui.leds:
#        led.write(0)
#        time.sleep(0.1)
#        led.write(1)

#    gui._job = gui.after(500, ledison_loop, gui)


def main():
    mqtt_client.will_set(mqtt_topic, '___Will of LEDison___', 0, False)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    root = tk.Tk()
    gui = Ledison(root)
    for i in range(0, 8):
        c = Circle(gui, i, 40 + 40 * i, 40, 15, fill="#BBB", outline="white",
                   width=1)
        if i in range(0, 4):
            c.on_color = "green"
        elif i in range(4, 7):
            c.on_color = "yellow"
        else:
            c.on_color = "red"
        leds.append(c)
        c.write(1)

    # gui._job = root.after(500, ledison_loop, gui)
    send_message("LEDison online")
    root.mainloop()


if __name__ == "__main__":
    main()
