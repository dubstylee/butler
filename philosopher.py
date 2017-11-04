import sys
import mraa
from enum import Enum
from shared import *
from random import *

class Status(Enum):
  ARISE     = 0
  SIT_DOWN  = 1
  HAS_LEFT  = 2
  HAS_RIGHT = 3
  EATING    = 5

forks = {0 : 'a', 1 : 'b' , 2 : 'c', 3 : 'd', 4 : 'e'}

class Philosopher:
  state = Status.ARISE
  identifier = 0
  led = None
  left = 0
  right = 0

  def updateForks(self):
    self.left = self.identifier
    self.right = (self.identifier + 1) % 5

  def changeState(self):
    self.state = Status(self.state.value + 1)
    print "Philosopher %d %s" %(self.identifier,self.state.value)
p = Philosopher()

def control_c_handler(signum, frame):
  p.led.write(OFF)
  exit_program()
signal.signal(signal.SIGINT, control_c_handler)

def on_message(client, userdata, msg):
  # Based on the message received the Philosopher
  # will go through state changes
  # Messages are sent to change states from the
  # main. The received messages are mostly ACKs to
  # those messages
  message = msg.payload
  #print("message %s \n" %message)
  split = message.split(' ')
  if "GOSITDOWN" in split[3] and \
    p.identifier == int(split[4]) and \
    p.state == Status.ARISE :
    p.state = Status.SIT_DOWN
    p.led.write(ON)
  elif "FORKAVAIL" in split[3] and \
    forks[p.left] == split[4] and \
    p.identifier == int(split[5]) and \
    p.state == Status.SIT_DOWN :
    p.state = Status.HAS_LEFT
  elif "FORKAVAIL" in split[3] and \
    forks[p.right] == split[4] and \
    p.identifier == int(split[5]) and \
    p.state == Status.HAS_LEFT :
    p.state = Status.HAS_RIGHT

def main():
  if len(sys.argv) != 2:
    print "Invalid number of arguments"
    exit_program()
  else:
    p.identifier = int(sys.argv[1])
    p.updateForks()
    p.led = mraa.Gpio(p.identifier+2)
    p.led.dir(mraa.DIR_OUT)
    p.led.write(OFF)
  mqtt_client.on_message = on_message
  mqtt_client.will_set(mqtt_topic, "Will of Philosopher %s\n\n", 0, False)
  mqtt_client.loop_start()  
  
  while True:
    # Based on the state of the philosopher
    # send apporpriate messages to the butler
    # or the fork.
    # State transitions only happen on ACKs to
    # the messages.
    if p.state == Status.ARISE :
      send_message("SITDOWN %d" %p.identifier)
    elif p.state == Status.SIT_DOWN :
      send_message("REQUEST %c %d" %(forks[p.left],p.identifier))
    elif p.state == Status.HAS_LEFT :
      send_message("REQUEST %c %d" %(forks[p.right],p.identifier))
    elif p.state == Status.HAS_RIGHT :
      p.state = Status.EATING
      send_message("EATING %d" %p.identifier)
      # Blink while eating
      delay = randint(5, 10)
      iter = float(delay) / 0.5
      while iter > 0 :
        p.led.write(ON)
        time.sleep(0.25)
        p.led.write(OFF)
        time.sleep(0.25)
        iter = iter - 0.5
      p.led.write(ON)
      send_message("REPLACE %c %d" %(forks[p.right],p.identifier))
      send_message("REPLACE %c %d" %(forks[p.left],p.identifier))
      send_message("ARISE %d" %p.identifier)
      p.led.write(OFF)
      p.state = Status.ARISE
      time.sleep(2)
    time.sleep(1)

if __name__ == "__main__": main()
