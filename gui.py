import Tkinter as tk
from shared import exit_program, mqtt_client, mqtt_topic


def part_a(gui):
    # part A Abhishek assert
    print("Abhi assert")


def part_b(gui):
    # part B Brian property
    print("Brian property")


# placeholder for GUI
def main():
    root = tk.Tk()
    top_frame = tk.Frame(root)
    top_frame.pack()

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM)

    part_a(top_frame)
    part_b(bottom_frame)

    root.mainloop()


if __name__ == "__main__":
    main()
