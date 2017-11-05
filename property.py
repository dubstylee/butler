from shared import exit_program, mqtt_client, mqtt_topic, send_message
import signal
import time

a = {"begin": "", "phil[0].sitdown": "GOSITDOWN 0", "phil[1].arise": "ARISE 1"}


class Prop():
    def __init__(self, alpha):
        self.alpha = alpha
        self.status = "begin"


prop = Prop(a)


def control_c_handler(signum, frame):
    exit_program()


signal.signal(signal.SIGINT, control_c_handler)


def on_message(client, userdata, msg):
    splits = msg.payload.split(' ')
    if splits[3] == "GOSITDOWN":
        send_message("UPDATEB %s %s: phil[%d].sitdown" %
                     (splits[0], splits[1], int(splits[4])))
        if splits[4] == "0":
            if prop.status != "begin":
                send_message("UPDATEB PROPERTY VIOLATION")
            else:
                prop.status = "phil[0].sitdown"
    elif splits[3] == "ARISE":
        send_message("UPDATEB %s %s: phil[%d].arise" %
                     (splits[0], splits[1], int(splits[4])))
        if splits[4] == "1":
            if prop.status != "phil[0].sitdown":
                send_message("UPDATEB PROPERTY VIOLATION")
            else:
                prop.status = "begin"


def main():
    mqtt_client.will_set(mqtt_topic, "___Will of SAFETY PROPERTY___", 0, False)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    while True:
        time.sleep(1.0)

    exit_program()


if __name__ == "__main__":
    main()
