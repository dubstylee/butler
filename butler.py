from shared import *

COUNT = 4;
tracker = [0, 0, 0, 0, 0]
queue = Queue()

def on_message(client, userdata, msg):
  global COUNT
  message = msg.payload
  split = message.split(' ')
  if "SITDOWN" in split[3] and COUNT > 0: 
    identifier = int(split[4])
    if tracker[identifier] != 1 :
      print(message)
      send_message("GOSITDOWN %d" %identifier)
      tracker[identifier] = 1
      COUNT = COUNT - 1
  elif "SITDOWN" in split[3] and COUNT == 0:
      identifier = int(split[4])
      send_message("NOSITDOWN %d" %identifier)
      #queue.put_distinct(identifier)
  elif "ARISE" in split[3]:
    identifier = int(split[4])
    if tracker[identifier] == 1 :
      print(message)
      tracker[identifier] = 0
      COUNT = COUNT + 1
      if (not queue.is_empty()) and COUNT > 0:
        identifier = queue.get()
        send_message("GOSITDOWN %d" %identifier)
        tracker[identifier] = 1
        COUNT = COUNT - 1 

def main():
  mqtt_client.on_message = on_message
  mqtt_client.will_set(mqtt_topic, "Will of Philosopher %s\n\n", 0, False)
  mqtt_client.loop_start()  
  while True:
    time.sleep(1);

if __name__ == "__main__": main()  
