import Tkinter as tk
from shared import exit_program, mqtt_client, mqtt_topic

a = {"begin": "", "phil[0].sitdown": "GOSITDOWN 0", "phil[1].arise": "ARISE 1"}


class Prop():
    def __init__(self, alpha):
        self.alpha = alpha
        self.status = "begin"


prop = Prop(a)


def on_message(client, userdata, msg):
    splits = msg.payload.split(' ')
    if splits[3] == "GOSITDOWN" and splits[4] == "0":
        if prop.status != "begin":
            print("property violation")
        else:
            prop.status = "phil[0].sitdown"
    elif splits[3] == "ARISE" and splits[4] == "1":
        if prop.status != "phil[0].sitdown":
            print("property violation")
        else:
            prop.status = "begin"


def main():
    mqtt_client.will_set(mqtt_topic, "___Will of SAFETY PROPERTY___", 0, False)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    root = tk.Tk()
    root.mainloop()
    exit_program()


if __name__ == "__main__":
    main()
