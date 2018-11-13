# Aries-Project-Control-System-Hybrid-Rocket-Engine
#Author Demetrios Doumas   11/12/18
#Aries Project

Info:  Design a control system for a hybrid rocket engine.
       Control system is made of two software; the user interface and the engine's software.
       The user interface is written in python 2.7.14.
       The engine is written in C/C++ Arduino code.


Purpose: Read a telemetry string from the engine that indicates its health. Also send commands to fill two tanks, launch, and perform an abort sequence. The engine itself also has some autonomous actions that automatically abort during any emergencies that can happen during the filling and launch procedures. The data is plotted and saved in real time. The communication connection between the GUI and the engine is wireless. The xBee radio module 3B series were used. The microcontroller used for the engine is an Arduino Mega 2560 Rev 3. 

Instructions:
	1.) Upload the Arduino code to the Arduino Mega 2560 rev 3. 
	2.) Disconnect the microcontroller from the PC.
	3.) Apply the power source to the microcontroller.
	4.) Open the GUI software on your laptop.
	5.) Type the baud rate and serial port number where your xBee radio module is connected to your USB serial port.
	6.) Click connect to open the serial port connection between your GUI and the engine.
	7.) Press the appropriate button to fill the tanks of the engine.


Warnings:

Close the serial connection before exiting the application by pressing the disconnect button.
