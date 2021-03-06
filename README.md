# butler
Implement dining philosophers on Intel Edison

Video of the project running:
https://www.dropbox.com/s/dbfhnjb7ovx815o/butler.mov?dl=0

<b>LEDison</b></br>
<p>The LEDison is a graphical interface that simulates an Intel Edison with 8 LED light board attached. In this project, it is used to display the fluents representing the status of the philosophers. When philosopher 0 sits at the table, fluent 0 on LED 0 will turn on. Once that philosopher finishes eating and replaces his forks and stands up, the LED will turn off.</p>
<b>Butler</b></br>
<p>The butler controls the table and determines whether or not a philosopher may sit down. Our implementation allows a maximum of 4 philosophers at the table at once to avoid deadlock. Once a spot becomes available, the butler will allow the next waiting philosopher to take a seat.</p>
<b>Philosopher</b></br>
<p>Each philosopher wants to sit at the table to eat. When they get permission from the butler, they will sit down and try to acquire the left fork followed by the right fork. If the left fork is not available, they will keep trying until the fork becomes available, then try for the right fork. Once a philosopher has acquired both forks, they will eat for a random interval, then replace forks and stand up. The LED for a philosopher will be solid once he has sat down, and will be flashing once the philosopher has both forks and is eating. Once the forks are replaced, the LED will be solid once again, and turn off once the philosopher leaves the table.</p>
<b>Fork</b></br>
<p>The fork is a simple process that keeps track of whether it is in use or available. While the fork is available, the LED will turn on. If a philosopher requests the fork when it is not in use, it will respond to the philosopher that it is available, then it will begin flashing to indicate it is in use. If the fork is already in use, it will respond accordingly to the requesting philosopher and the philosopher will keep requesting the fork until it becomes available.</p>

<hr>

<b>Property</b>
<p>The property monitor runs in conjunction with the above butler system to watch for safety violations as specified by the properties. Only actions that are part of a property will be logged, and if a property violation is detected, a message will be sent out. The GUI process will display the status of the property monitor. If a property violation is detected, that property will stop listening to messages.</p>
<b>Assert</b>
<p>The assert process gives the user to assert and check some conditions during the execution of the dining philosopher system. The current assert process is made to assert the case `!phil[i].eat W phil[j].arise` where i and j can be passed in from the command line to the process to make the desired assert. Only EAT and ARISE actions are tracked by the current assert process. If the assert process notices the assert has failed, it reports the failure to the GUI process at which point the GUI no more listens to messages from the assert process</p>
<b>GUI</b>
<p>The GUI process just listens for messages from the property and assert monitors. The status of the others processes is displayed in the GUI. If a property violation is detected, the status label will turn red to indicate the violation.</p>
