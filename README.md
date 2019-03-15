# Project Name: Aries-Project-Control-System-Hybrid-Rocket-Engine,  Fall 2017 to Spring 2018
//Author Demetrios Doumas   11/12/18
//Aries Project


# Description
Design a control system for a hybrid rocket engine. The control system is made of two software; the user interface and the engine's software. The user interface is written in python 2.7.14. The engine is written in C/C++ Arduino code.

Electrical Engineer group: Developed circuits to power multiple valves and the heater circuit that ignites the fuel. They also developed the entire PCB board.

My Role: Read a telemetry string from the engine that indicates its health. Also send commands to fill two tanks, launch, and perform an abort sequence. The engine itself also has some autonomous actions that automatically abort during any emergencies that can happen during the filling and launch procedures. The data is plotted and saved in real time. The communication connection between the GUI and the engine is wireless. The xBee radio modules 3B 900 MHz series were used. The ground station was a directional antenna and the engine’s antenna is omnidirectional. The microcontroller used for the engine is an Arduino Mega 2560 Rev 3. 

# Instructions
1.) Download AriesControlSystemFinalSpring2018 and the GroundStationGUIProjectAriesSpring2018 files.

# Usage
1.) Upload the Arduino code to the Arduino Mega 2560  
2.) Disconnect the microcontroller from the PC.
3.) Apply the power source to the microcontroller.
4.) Open the GUI software on your laptop.
5.) Type the baud rate and serial port number where your xBee radio module is connected to your USB serial port.
6.) Click connect to open the serial port connection between your GUI and the engine.
7.) Press the appropriate button to fill the tanks of the engine.


Warnings:

Close the serial connection before exiting the application by pressing the disconnect button.

A video demonstration can be found in this link below:
https://www.youtube.com/watch?v=jyF8A0nIojg&feature=youtu.be

# Credits
Team Members:

Electrical Engineers:

Tyrell Williams
Johann Rosario
Kevin Panata

Computer Engineer:

Demetrios Doumas
