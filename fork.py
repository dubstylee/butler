import mraa
import signal
import time
import sys
from shared import exit_program, mqtt_client, mqtt_topic, send_message, ON, OFF


class Fork():
    name = "fork"
    led_no = 0
    in_use = False


fork = Fork()


def on_message(client, userdata, msg):
    # we only listen for messages from
    # print msg.payload
    splits = msg.payload.split(' ')
    if splits[3] == "REQUEST":
        if splits[4] == fork.name:
            if fork.in_use:
                send_message("FORKBUSY %s %d" % (fork.name, int(splits[5])))
            else:
                print(msg.payload)
                send_message("FORKAVAIL %s %d" % (fork.name, int(splits[5])))
                fork.in_use = True
    elif splits[3] == "REPLACE":
        if splits[4] == fork.name:
            print(msg.payload)
            send_message("FORKREPL %s" % fork.name)
            fork.in_use = False


def control_c_handler(signum, frame):
    mraa.Gpio(fork.led_no + 2).write(OFF)
    exit_program()

signal.signal(signal.SIGINT, control_c_handler)


def main():
    if len(sys.argv) != 2:
        print "Usage: fork <label>"
        exit_program()

    led_no = int(ord(sys.argv[1].lower()) - ord('a'))
    if led_no < 0 or led_no > 7:
        print "Usage: fork <label>\nlabel must be a letter between a and h"
        exit_program()

    mqtt_client.will_set(mqtt_topic, '___Will of FORK %s___' % fork.name, 0,
                         False)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    fork.name = sys.argv[1]
    fork.led_no = led_no

    send_message("FORK '%s' is in da house (on led %d)" % (fork.name,
                 fork.led_no))

    led = mraa.Gpio(fork.led_no + 2)
    led.dir(mraa.DIR_OUT)
    led.write(ON)

    while True:
        while fork.in_use:
            led.write(OFF)
            time.sleep(0.1)
            led.write(ON)
            time.sleep(0.1)

        # send_message("FORK %s stayin' alive" % fork.name)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
