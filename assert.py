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

from shared import *

#  These arrays gives a way to maintain an assert per
#  philosopher, or to have a common assert for all
#  philosophers.

class Status(Enum) :
  ERROR = -1
  BEGIN = 0
  HOMEFREE = 1

#  Since we have a weak until in the property, we have
#  a valid BEGIN state where the assert passes for all
#  philosophers
assertStatus = [Status.BEGIN, Status.BEGIN, 
                Status.BEGIN, Status.BEGIN, 
                Status.BEGIN]

def on_message(client, userdata, msg):
  global COUNT
  message = msg.payload
  split = message.split(' ')
  action = split[3]
  identifier = int(split[4])
  if "EATING" == action :
    if assertStatus[identifier] == Status.BEGIN
      assertStatus[identifier] = Status.ERROR
    send_message("UPDATEA %s" %message)
  elif "ARISE" == action :
    if assertStatus[identifier] == Status.BEGIN
      status = Status.HOMEFREE
    send_message("UPDATEA %s" %message)

def main():
  mqtt_client.on_message = on_message
  mqtt_client.will_set(mqtt_topic, "Will of Validator %s\n\n", 0, False)
  mqtt_client.loop_start()  
  while True:
    time.sleep(1)
    #Check assert status and control the LED accordingly
    if Status.ERROR in assertStatus
      sendmessage("UPDATEA ASSERTFAILED")

if __name__ == "__main__": main()  
