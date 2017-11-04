from shared import *

#  These arrays gives a way to maintain an assert per
#  philosopher, or to have a common assert for all
#  philosophers.
assertStatus = [1, 1, 1, 1, 1]
philosopherStatus = [0, 0, 0, 0, 0]

#  In case of an Eating message, check if the philosopher
#  was sitting down, if he was, the fluent fails.
#  He must be in the state before sitting down to be Eating.
#  
#    assert TESTING = (!phil[0].eat W phil[0].arise)
#
#  In this case we have a weak until to verify, so it will
#  be true when a philosopher never eats, or if they eat, 
#  they only can if they are standing up. 


def checkAssert(identifier)
  global assertStatus
  #perform validations over here
  assertStatus = False

def on_message(client, userdata, msg):
  global COUNT
  message = msg.payload
  split = message.split(' ')
  action = split[3]
  identifier = int(split[4])
  if "SITDOWN" == action :
    philosopherStatus[identifier] = 1
  elif "EATING" == action :
    checkAssert(identifier)
  elif "ARISE" == action :
    philosopherStatus[identifier] = 0

def manageLEDs():
  print "Managing LEDs"

def main():
  global assertStatus
  mqtt_client.on_message = on_message
  mqtt_client.will_set(mqtt_topic, "Will of Validator %s\n\n", 0, False)
  mqtt_client.loop_start()  
  while True:
    time.sleep(1)
    manageLEDs()
    #Check fluent status and control the LED accordingly 

if __name__ == "__main__": main()  
