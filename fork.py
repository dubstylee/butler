import time

from shared import *

class Fork():
	name = "fork"
	led_no = 0

	def __init__(self, name, led_no):
		self.name = name
		self.led_no = led_no

def on_message(client, userdata, msg):
	# we only listen for messages from CONTROL
	print msg.payload

def main():
	if len(sys.argv) != 3:
		print "Usage: fork <name> <led_no>"
		exit_program()

	if not sys.argv[2].isdigit():
		print "Usage: fork <name> <led_no>\nled_no must be a number between 0 and 7"
		exit_program()

	led = int(sys.argv[2])
	if led < 0 or led > 7:
		print "Usage: fork <name> <led_no>\nled_no must be a number between 0 and 7"
		exit_program()

	mqtt_client.will_set(mqtt_topic, '___Will of FORK___', 0, False)
	mqtt_client.on_message = on_message
	mqtt_client.loop_start()

	fork = Fork(sys.argv[1], led)
	send_message("Fork %s running on led #%d" % (fork.name, fork.led_no))

	while True:
		print "I'm a fork named %s" % fork.name
		time.sleep(5.0)

if __name__ == '__main__': main()