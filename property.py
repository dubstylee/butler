from shared import exit_program, mqtt_client, mqtt_topic, send_message
import signal
import time

properties = {"TESTING2": [["GOSITDOWN 0", "phil[0].sitdown"],
                           ["ARISE 1", "phil[1].arise"]]}
'''
properties = {"TESTING2": [["GOSITDOWN 0", "phil[0].sitdown"],
                           ["ARISE 1", "phil[1].arise"]],
              "EXTRA": [["GOSITDOWN 0", "phil[0].sitdown"],
                        ["ARISE 1", "phil[1].arise"],
                        ["GOSITDOWN 0", "phil[0].sitdown"]]}
'''


class Prop():
    def __init__(self, name, alphabet):
        self.name = name
        self.alphabet = alphabet
        self.status = 0

    def __repr__(self):
        text = "property %s = (" % self.name
        for i in range(0, len(self.alphabet)):
            action = self.alphabet[i]
            if i == self.status:
                text = text + "[%s] -> " % action[1].upper()
            else:
                text = text + "%s -> " % action[1]
        text = text + "%s)" % self.name
        return text


property_list = []
for p in properties:
    prop = Prop(p, properties[p])
    property_list.append(prop)


def control_c_handler(signum, frame):
    exit_program()


signal.signal(signal.SIGINT, control_c_handler)


def on_message(client, userdata, msg):
    splits = msg.payload.split(' ', 3)

    for p in property_list:
        found = False
        actions = p.alphabet
        for i in range(0, len(actions)):
            if actions[i][0] == splits[3]:
                found = True
                break

        if found:
            send_message("UPDATEB %s %s %s: %s" %
                         (splits[0], splits[1], p.name, splits[3]))
            if actions[p.status][0] == splits[3]:
                p.status = (p.status + 1) % len(p.alphabet)
            else:
                send_message("UPDATEB VIOLATION OF PROPERTY %s" % p.name)

    update_properties()


def update_properties():
    label_str = ""

    for i in range(0, len(property_list)):
        if i != 0:
            label_str = label_str + "\n"
        label_str = label_str + ("%s" % property_list[i])

    send_message("LABELB %s" % label_str)


def main():
    mqtt_client.will_set(mqtt_topic, "___Will of SAFETY PROPERTY___", 0, False)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    update_properties()

    while True:
        time.sleep(1.0)

    exit_program()


if __name__ == "__main__":
    main()
