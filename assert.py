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

#  1 : assert is valid, 0 : assert is invalid
#  Starting out with all 1s because of the weak until
assertStatus = [1, 1, 1, 1, 1]

#  1 means the philosopher is at the table
philosopherStatus = [0, 0, 0, 0, 0]

def checkAssert(identifier)
  #  Perform validations over here
  if philosopherStatus[identifier] == 0
    #  Means the philosopher is not at the table and is 
    #  eating, in which case the assert is valid.
    assertStatus[identifier] = 1
  elif philosopherStatus[identifier] == 1
    #  Means the philosopher is at the table and is eating,
    #  in which case the assert is invalid.
    assertStatus[identifier] = 0

def on_message(client, userdata, msg):
  global COUNT
  message = msg.payload
  split = message.split(' ')
  action = split[3]
  identifier = int(split[4])
  if "SITDOWN" == action :
    philosopherStatus[identifier] = 1
    send_message("UPDATEA %s" %message)
  elif "EATING" == action :
    checkAssert(identifier)
    send_message("UPDATEA %s" %message)
  elif "ARISE" == action :
    philosopherStatus[identifier] = 0
    send_message("UPDATEA %s" %message)

def main():
  mqtt_client.on_message = on_message
  mqtt_client.will_set(mqtt_topic, "Will of Validator %s\n\n", 0, False)
  mqtt_client.loop_start()  
  while True:
    time.sleep(1)
    #Check assert status and control the LED accordingly
    if 0 in assertStatus
      sendmessage("UPDATEA ASSERTFAILED")

if __name__ == "__main__": main()  
