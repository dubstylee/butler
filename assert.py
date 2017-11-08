############################################################
#  In case of an Eating message, check if the philosopher
#  was sitting down, if he was, the fluent fails.
#  He must be in the state before sitting down to be Eating.
#  
#    assert TESTING = (!phil[0].eat W phil[0].arise)
#
#  In this case we have a weak until to verify, so it will
#  be true when a philosopher never eats, or if they eat, 
#  they only can if they are standing up. 
############################################################
from enum import Enum
from shared import *

# Enum to track the state of the system according to
# LTSA developed for the system.
class Status(Enum) :
  ERROR = -1
  BEGIN = 0
  HOMEFREE = 1

#  Since we have a weak until in the property, we have
#  a valid BEGIN state where the assert passes for all
#  philosophers
assertStatus = Status.BEGIN

eatIdentifier = 0
ariseIdentifier = 0

def on_message(client, userdata, msg):
  global assertStatus
  message = msg.payload
  print message
  if (not ("EATING" in message or "ARISE" in message)) or ("UPDATEA" in message):
    return
  split = message.split(' ')
  action = split[3]
  identifier = int(split[4])

  if "EATING" == action and identifier == eatIdentifier:   
    if assertStatus == Status.BEGIN:
      assertStatus = Status.ERROR
      send_message("UPDATEA ASSERTFAILED")
    send_message("UPDATEA %s" %message)

  elif "ARISE" == action and identifier == ariseIdentifier:
    if assertStatus == Status.BEGIN:
      assertStatus = Status.HOMEFREE
    send_message("UPDATEA %s" %message)

def main():
  global assertStatus
  global eatIdentifier
  global ariseIdentifier

  if len(sys.argv) < 3:
    print "Wrong number of arguments : assert.py <eat identifier> <arise identifier>"
    exit_program()

  eatIdentifier = int(sys.argv[1])
  ariseIdentifier = int(sys.argv[2])

  mqtt_client.on_message = on_message
  mqtt_client.will_set(mqtt_topic, "Will of Validator %s\n\n", 0, False)
  mqtt_client.loop_start() 
  while True:
    time.sleep(1) 

if __name__ == "__main__": main()  
