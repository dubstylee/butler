import Tkinter as tk
from shared import exit_program, mqtt_client, mqtt_topic


class Gui(tk.Frame):
    def __init__(self, master, assert_frame, property_frame):
        tk.Frame.__init__(self, master)
        master.title("Something Cool")
        self.master = master
        self.assert_frame = assert_frame
        self.property_frame = property_frame

    def part_a(self):
        # uses assert_frame
        # part A Abhishek assert
        print("Abhi assert")

    def part_b(self):
        # part B Brian property
        label = tk.Label(self.property_frame, text="property description")
        label.pack()
        text = tk.Text(self.property_frame, width=200)
        text.pack()


# placeholder for GUI
def main():
    root = tk.Tk()
    top_frame = tk.Frame()
    top_frame.pack()
    bottom_frame = tk.Frame()
    bottom_frame.pack(side=tk.BOTTOM)
    gui = Gui(root, top_frame, bottom_frame)

    gui.part_a()
    gui.part_b()

    root.mainloop()


if __name__ == "__main__":
    main()
