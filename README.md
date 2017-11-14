# RPi_UPS
A simple UPS can be created for the raspberry pi using a USB battery bank to provide back up and a python script
that checks when the power has gone off and the shuts the pi down some time later i.e. before the battery has gone flat.
Using a transistor circuit the pi can be switched back on when the power resumes.

Shutting down the Pi:
Use the python script which checks the status of GPIO 3 and either shuts the RPi down or does nothing.

Turning the Pi on when power is restored:
A simple transistor switch was set up using a PN2222 transistor. The input signal (b) was 5V from a USB cable which is plugged
into the mains. If the mains goes so does the input signal therefore the transistor switch is open. The switch of the transistor
(c and e) was connects GPIO3 (pin 5) of the RPi to ground. 
If the Pi is switched off and GPIO3 is connected to GND the Pi will turn on.

Connect a 100k ohm resistor in series with the 5V input signal. This prevents false triggering when the pin is floating.
Connect a 330 ohm resistor in series with the switching circuit. This limits the current if GPIO3 was set high by mistake. Otherwise
3.3V would be shorted with GND. The current is limited to 0.01 amps. GPIO3 has an internal pull up resistor. This means there is a 
potential divider. 3.3V at the top and GND at the bottom with a 1800 ohm and 330 ohms resistor. This gives 0.51V at GPIO3.


Logic Test:
Pi turned on = GPIO is shorted to GND by transistor. Python script reads 0 and does nothing.
Power goes off = Transistor switch goes off. GPIO3 is pulled high by internal resistor. Python script read 1 and shuts pi down.
Power comes on: Transistor switch comes on. GPIO3 is shorted to GND which in turn starts the pi.

The python script should be set to run as cron job. The time interval should be set according to how long your back up battery
will last. Using a USB current meter I recorded that the RPi used around 160 mAh over a 25 minute period which means my 1600 mAh
battery will last around 4 hours.
I used a cron job of every hour i.e. at minute 0:

0 * * * * /home/pi/RPi_UPS/rpi_shutdown.py
