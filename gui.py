import Tkinter as tk
from shared import mqtt_client, mqtt_topic, exit_program

class Gui(tk.Frame):
    part_a_text = None
    part_b_text = None

    def __init__(self, master, assert_frame, property_frame):
        tk.Frame.__init__(self, master)
        master.title("Something Cool")
        self.master = master
        self.assert_frame = assert_frame
        self.property_frame = property_frame

    def part_a(self):
        # uses assert_frame
        # part A Abhishek assert
        toAssert = "(!phil[i].eat W phil[i].arise)"
        label = tk.Label(self.assert_frame, text=toAssert)
        label.pack()        
        self.part_a_text = tk.Listbox(self.assert_frame, width=200)
        self.part_a_text.pack()

    def part_b(self):
        # part B Brian property
        label = tk.Label(self.property_frame,
                         text="property TESTING2 = "
                         "(phil[0].sitdown -> phil[1].arise -> TESTING2).")
        label.pack()
        self.part_b_text = tk.Text(self.property_frame, width=200)
        self.part_b_text.pack()

    def update_part_a(self, text):
        self.part_a_text.insert(tk.END, text)

    def update_part_b(self, text):
        self.part_b_text.insert(tk.END, text)

gui = None

def on_message(client, userdata, msg):
    message = msg.payload
    splits = message.split(' ', 4)
    if splits[3] == "UPDATEA":
        gui.update_part_a(splits[4])
    elif splits[3] == "UPDATEB":
        gui.update_part_b(splits[4])

# placeholder for GUI
def main():
    global gui
    root = tk.Tk()
    top_frame = tk.Frame()
    top_frame.pack()
    bottom_frame = tk.Frame()
    bottom_frame.pack(side=tk.BOTTOM)
    gui = Gui(root, top_frame, bottom_frame)

    mqtt_client.will_set(mqtt_topic, '___Will of GUI___', 0, False)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    gui.part_a()
    gui.part_b()

    root.mainloop()
    exit_program()


if __name__ == "__main__":
    main()
