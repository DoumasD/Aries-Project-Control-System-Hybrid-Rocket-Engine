# Demetrios Doumas GUI           4/20/18
# Revised 3/25/19
# Senior Design Hybrid Rocket Engine Ground Station Software
# The software will read Data from the control System and be able to send commands as well to it.

#How does it Work?
'''
Description:

This software implementation of the control system relies on communication between two threads. The first thread called get_data receives data and places it on a queue. The thread is also responsible
for displaying the telemetry data on the GUI window below the three graphs. The second thread called thread_plot, pops the queue to retrieve the data and plots the data on the three graphs. 
The number of data points displayed on the graphs is determined by a counter called count.

Instructions:

1.) Make sure the Arduino Mega 2560 microcontroller is connected to your PC.
2.) Enter baud rate (115200) and com port number (look at device manager). Make sure that the baud rate in the electronics code, AriesControlSystemFinalSpring2018.ino, has the same
baud rate and make sure that the engine is communicating on the correct UART serial communication port. There are four communication ports, 0-3, on the Arduino Mega 2560.
3.) Click "Connect". The get_data function starts running in its own thread.
4.) Wait for 6 consecutive readings.
5.) Click "Start Plot" to see the data being plotted. The thread_plot function starts running in its own thread.
6.) Click any buttons to send commands to the engine.
7.) Click "Disconnect", in order to exit. 

Note: Save the excel file in a different name so that it will not be overwritten when the program is running again.
      The data being displayed on the Muiltithreading_Groundstation_Software_Output file is not real. The output is the result of connecting the microcontroller directly to the laptop without
      the connections to the PCB of the control system.
'''

import Tkinter
import tkMessageBox
import matplotlib.pyplot as plt
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from threading import Thread
import threading
import time
import os
import serial
import csv
import Queue
import numpy as np







Q=Queue.Queue() # Is used to share data between two threads.

# Creating empty arrays used for plotting data in MATLAB plots
mission_time=[]
pressurant_pressure=[]     
pressurant_temp=[]
oxidizer_pressure=[]
oxidizer_temp=[]
combustion_pressure=[]


filter_data =''     # Holds parsed telemetry array 
serial_object = None # Used as handler to serial port
x= 0   # Creating x as a global variable, used to control the infinte loop when disconnect button is pressed






# Create a File in excel with Headers that describe the telemetry 
RESULT = ['Mission_time','Temp1','Temp2','Pressure1', 'Pressure2','Temp3','Temp4','Pressure3', 'Pressure4','Temp5','Temp6','Pressure5', 'Pressure6', 'Pressurant_Fill_Indicator','Pressurant_Oxidizer_Indicator','Oxidizer_Fill_Indicator','Oxidizer_Combustion_Indicator']
with open("output.csv",'wb') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerow(RESULT)


'''
This function takes the baud rate and comport # that was typed by the user in the entry box on the GUI screen and opens a serial port connection. 
The code tries to open the connection, for any reason that the comport can't be open, then this function prints an error.
The error cab happen during run time for any reason. The person forgets to plug in the microntroller for debuggng purposes. Another issues would be the microcontroller isn't on.
This function calls another function "get_data()" that is responsible for retriving the data.
'''

def connect():

    global serial_object
    port = port_entry.get()
    print(port)
    baud = baud_rate.get()
    print(baud)
    try:
        serial_object=serial.Serial('COM' + str(port), baud,timeout=0)
       
    except ValueError:
        print("Enter Baud and Port")
        return
  
    #get_data()
    t1 = threading.Thread(target = get_data)
    t1.daemon = True
    t1.start()



'''
The get data is responsible for retrieving the data from the serial connection. Saves incoming data in a excel file. Shares the data by placing it on a queue for the thread_plot to use.'''



def get_data():
    """  Update all the labels based on telemetry string
        Mission_time, temp1, temp2, pressure1, pressure2, temp3, temp4, pressure3, pressure4, temp5,
        temp6, pressure5, pressure6, Pressurant_Fill_Indicator, Pressurant_Oxidizer_Indicator,
        Oxidizer_Fill_Indicator, and Oxidizer_Combustion_Indicator.
    """
    global x
    global serial_object
    global filter_data
    


    while(x==0):  ## Read data infinitley until the disconnect button is pressed.

       
        

        while (serial_object.inWaiting()==0): #Wait here until there is data.
            time.sleep(1) #1
            
            pass #do nothing
        

        try:       
            
            serial_data=serial_object.readline().strip('\n').strip('\r')
          
          
                                   
        
        
            filter_data = serial_data.split(',')
            
            Q.put(filter_data)  # put data on queue
       
            print(filter_data)

            
            if (filter_data):
              
                # Expand the label box to cover old repeated text in x and y directions
                # Storing data in variables
                # Display variables on the screen in text
                # Data Label 1                               temp1
                v=StringVar()                            
                DATALABEL1=Label(root, textvariable=v,  width=10)
                DATALABEL1.place(x=175,y=640)
                v.set(filter_data[1])
               
                # Data Label 2                               temp2
                v1=StringVar()
                DATALABEL2=Label(root, textvariable=v1,  width=10)
                DATALABEL2.place(x=175,y=660)
                v1.set(filter_data[2])

                # Data Label 3                            pressure1
                v2=StringVar()
                DATALABEL3=Label(root, textvariable=v2,  width=10)
                DATALABEL3.place(x=175,y=680)      
                v2.set(filter_data[3])

                # Data Label 4                          pressure2                            
                v3=StringVar()
                DATALABEL4=Label(root, textvariable=v3,  width=10)
                DATALABEL4.place(x=175,y=700)
                v3.set(filter_data[4])

                #Column 2 from the left
                ######################################

                # Data Label 5                          temp3
                v4=StringVar()
                DATALABEL5=Label(root, textvariable=v4, width=10)
                DATALABEL5.place(x=275,y=640)
                v4.set(filter_data[5])

                # Data Label 6                          temp4
                v5=StringVar()
                DATALABEL6=Label(root, textvariable=v5,  width=10)
                DATALABEL6.place(x=275,y=660)
                v5.set(filter_data[6])

                # Data Label 7                          pressure3
                v6=StringVar()
                DATALABEL7=Label(root, textvariable=v6,  width=10)
                DATALABEL7.place(x=275,y=680)
                v6.set(filter_data[7])

                # Data Label 8                         pressure4
                v7=StringVar()
                DATALABEL8=Label(root, textvariable=v7,  width=10)
                DATALABEL8.place(x=275,y=700)
                v7.set(filter_data[8])

                #Column 3 from the left
                #######################################
                # Data Label 9                          temp5
                v8=StringVar()
                DATALABEL9=Label(root, textvariable=v8,  width=10)
                DATALABEL9.place(x=375,y=640)
                v8.set(filter_data[9])

                # Data Label 10                         temp6
                v9=StringVar()
                DATALABEL10=Label(root, textvariable=v9,  width=10)
                DATALABEL10.place(x=375,y=660)
                v9.set(filter_data[10])

                # Data Label 11                         pressure5
                v10=StringVar()
                DATALABEL11=Label(root, textvariable=v10,  width=10)
                DATALABEL11.place(x=375,y=680)
                v10.set(filter_data[11])

                # Data Label 12                         pressure6
                v11=StringVar()
                DATALABEL12=Label(root, textvariable=v11,  width=10)
                DATALABEL12.place(x=375,y=700)
                v11.set(filter_data[12])

                #Column 4 Valves   Indicators
                ######################################

                # Data Pressurant_Fill Valve Indicator           Pressurant_Fill_Indicator
                v12=StringVar()
                DATALABEL13=Label(root, textvariable=v12,  width=10)
                DATALABEL13.place(x=815, y=640)
                v12.set(filter_data[13])

                # Data Pressurant_Oxidizer Valve Indicator       Pressurant_Oxidizer_Indicator
                v14=StringVar()
                DATALABEL15=Label(root, textvariable=v14,  width=10)
                DATALABEL15.place(x=815, y=660)
                v14.set(filter_data[14])

                # Data Oxidizer_fill Valve Indicator             Oxidizer_Fill_Indicator
                v15=StringVar()
                DATALABEL16=Label(root, textvariable=v15,  width=10)
                DATALABEL16.place(x=815, y=680)
                v15.set(filter_data[15])

                # Data Oxi_Combustion Valve Indicator            Oxidizer_Combustion_Indicator
                v17=StringVar()
                DATALABEL18=Label(root, textvariable=v17,  width=10)
                DATALABEL18.place(x=815, y=700)
                v17.set(filter_data[16])

                #######################################




                
                ############# Convert data into numbers for ploting 
                MissionTime=float(filter_data[0])
                PressurantTemp= float(filter_data[1])
                PressurantPressure = float(filter_data[3])
                OxidizerTemp= float(filter_data[5])
                OxidizerPressure = float(filter_data[7])
                CombustionPressure=float(filter_data[11])
                
            

                ################################
                ### Check
                ### Above pressurant pressure and temperature limit  
                ### Above oxidizer pressure and temperature limit
                ##Add Color Warnings 

                if (PressurantPressure >= 50.0):  
                     DATALABEL3.config(bg='red')
                     DATALABEL3.config(fg='white')
                elif ((PressurantPressure >=30) and (PressurantPressure < 50) ):
                     DATALABEL3.config(bg='yellow')
                     DATALABEL3.config(fg='black')
                else:
                     DATALABEL3.config(bg=None)
                     DATALABEL3.config(fg='black')

                if (PressurantTemp >= 40.0):
                     DATALABEL1.config(bg='red')
                     DATALABEL1.config(fg='white')
                elif ((PressurantTemp >=30) and (PressurantTemp < 40) ):
                     DATALABEL1.config(bg='yellow')
                     DATALABEL1.config(fg='black')
                else:
                     DATALABEL1.config(bg= None)
                     DATALABEL1.config(fg='black')


                if (OxidizerPressure >= 50.0):
                     DATALABEL7.config(bg='red')
                     DATALABEL7.config(fg='white')
                elif ((OxidizerPressure >=30) and (OxidizerPressure < 50)):
                     DATALABEL7.config(bg='yellow')
                     DATALABEL7.config(fg='black')
                else:
                     DATALABEL7.config(bg=None)
                     DATALABEL7.config(fg='black')


                if (OxidizerTemp >= 40.0):
                     DATALABEL5.config(bg='red')
                     DATALABEL5.config(fg='white')
                elif ((OxidizerTemp >=30) and (OxidizerTemp < 40) ):
                     DATALABEL5.config(bg='yellow')
                     DATALABEL5.config(fg='black')
                else:
                     DATALABEL5.config(bg=None)
                     DATALABEL5.config(fg='black')

                try:
                    with open("output.csv","a+") as resultFile:   # Save to the excel file
                        wr = csv.writer(resultFile, dialect='excel')
                        wr.writerow(filter_data)
                except:
                    pass
                
        except:
            pass

                

     

def send():    # Manually send numerical commands through typing in the text field.

    send_data = data_entry.get()

    if not send_data:
        print("Sent Nothing")

    serial_object.write(send_data)
    print(send_data)

def disconnect():   # Exit the program
    global x
    x=1
    
    try:
        serial_object.close()  # Close serial port connection
        
    except AttributeError:
        print("Closed without opening it")
   
    
    root.destroy()          # Destroy the GUI window








# Sending numerical commands to actuate the engine
def open_Pressurant_fill():
    global serial_object
    serial_object.write(b'1')
   

def close_Pressurant_fill():
    global serial_object
    serial_object.write(b'2')
    
def open_POIV():
    global serial_object
    serial_object.write(b'3')
    
def close_POIV():
    global serial_object
    serial_object.write(b'4')
    
def open_Oxidizer_fill():
    global serial_object
    serial_object.write(b'5')
    
def close_Oxidizer_fill():
    global serial_object
    serial_object.write(b'6')
    
def launch():
    global serial_object
    serial_object.write(b'7')
    
def Abort():
    global serial_object
    serial_object.write(b'8')


"""Plot data in real time in a thread from the queue where the data is stored. The data is placed on the queue by another thread running get_data."""
def thread_plot():
    global Q
    
    data=[]
    count=0  # Counter, used to count the number of data points



    # Display the plots in the canvas again
    figtwo = plt.figure()

    AX = figtwo.add_subplot(311)   

    AX.set_xlabel("Mission Time (Sec)")
    AX.set_ylabel("Temperature (C)")
    AX.set_title(" Pressurant Tank: ")
    AX.grid()
    AX2=AX.twinx()
    AX2.set_ylabel("Pressure (psi)")
    AX2.tick_params(axis='y', labelcolor='green')

    
    AXTWO = figtwo.add_subplot(312)

    AXTWO.set_xlabel("Mission Time (Sec)")
    AXTWO.set_ylabel("Temperature (C)")
    AXTWO.set_title(" Oxidizer Tank: ")
    AXTWO.grid()
    AXTWO2=AXTWO.twinx()
    AXTWO2.set_ylabel("Pressure (psi)")
    AXTWO2.tick_params(axis='y', labelcolor='black')


    AXTHREE = figtwo.add_subplot(313)
    AXTHREE.set_xlabel("Mission Time (Sec)")
    AXTHREE.set_ylabel("Pressure (psi)")
    AXTHREE.set_title(" Combustion Tank: ")
    AXTHREE.grid()
    

    graphTWO = FigureCanvasTkAgg(figtwo, master=root)
    graphTWO.get_tk_widget().place(height=600 , width=1000)

    while(1):
        try:
            data=Q.get()    # retrieve data from queue Q
        except Queue.Empty:
            pass

     
        ############# Convert data into numbers for ploting 
        MissionTime=float(data[0])
        PressurantTemp= float(data[1])
        PressurantPressure = float(data[3])
        OxidizerTemp= float(data[5])
        OxidizerPressure = float(data[7])
        CombustionPressure=float(data[11])

       

        if(count>5):    # Removes old data
            mission_time.pop(0)
            pressurant_temp.pop(0)
            pressurant_pressure.pop(0)
            oxidizer_temp.pop(0)
            oxidizer_pressure.pop(0)
            combustion_pressure.pop(0)

            
        mission_time.append(MissionTime)
        pressurant_temp.append(PressurantTemp)
        pressurant_pressure.append(PressurantPressure)
        oxidizer_temp.append(OxidizerTemp)
        oxidizer_pressure.append(OxidizerPressure)
        combustion_pressure.append(CombustionPressure)
        count=count+1
        
        # Clear axes
        AX.cla()
        AX2.cla()
        AXTWO.cla()
        AXTWO2.cla()
        AXTHREE.cla()
        
        AX.plot(mission_time,pressurant_temp, marker='x', color='blue')
        AX.set_title(" Pressurant Tank: ")
        AX.grid()
        AX.set_xlabel("Mission Time (Sec)")
        AX.set_ylabel("Temperature (C)")
        AX2.plot(mission_time,pressurant_pressure, marker='x', color='green')
        AX2.set_ylabel("Pressure (psi)")
         




       
        AXTWO.plot(mission_time,oxidizer_temp,marker='o', color='orange')
        AXTWO.set_title(" Oxidizer Tank: ")
        AXTWO.grid()
        AXTWO.set_xlabel("Mission Time (Sec)")
        AXTWO.set_ylabel("Temperature (C)")
        AXTWO2.plot(mission_time,oxidizer_pressure, marker='o', color='yellow')
        AXTWO2.set_ylabel("Pressure (psi)")





        
        AXTHREE.plot(mission_time,combustion_pressure,marker='x', color='red')
        AXTHREE.set_title(" Combustion Tank: ")
        AXTHREE.grid()
        AXTHREE.set_xlabel("Mission Time (Sec)")
        AXTHREE.set_ylabel("Pressure (psi)")
        
        

         
        

        graphTWO.draw()
        time.sleep(.1)
        figtwo.tight_layout()
    


# This function starts thread_plot function in a thread when the user clicks start plot
def Plot_Now():
    t2 = threading.Thread(target = thread_plot)
    t2.daemon = True
    t2.start()






    


################################################## Main 

if __name__ == "__main__":

    root = Tk()
    root.title("Aries Project")
    root.geometry('{}x{}'.format(1600, 800))
    root.resizable(False, False)
    root.update_idletasks()
    frame_1 = Frame(height = 400, width = 600, bd = 3, relief = 'groove').place(x = 1000, y = 400)


    #The lines below create the buttons and labels you see on the window.
    #Creating Widgets 
    LabelOne=Label(root,text= "Tanks:",font = "Times 14 bold")
    LabelTwo=Label(root,text= "Pressurant:",font = "Times 14 bold")
    LabelThree=Label(root,text= "Oxidizer:",font = "Times 14 bold")
    LabelFour=Label(root,text = "Combustion:",font = "Times 14 bold")
    LabelFive=Label(root,text= "Temperature  (C):")
    LabelSix=Label(root,text= "Temperature  (C):")	
    LabelSeven=Label(root,text= "Pressure        (psi):")
    LabelEight=Label(root,text= "Pressure        (psi):")
    LabelNine=Label(root, text= "Baud Rate:")
    LabelTen=Label(root, text= "Port:")	
    LabelEleven=Label(root, text= "Numbers Only")
    LabelTwelve=Label(root, text= "Valves: ",font = "Times 14 bold")
    LabelThirteen=Label(root, text= "High/Low (1/0):",font = "Times 14 bold")
    Label_14=Label(root, text ="Pressurant_Fill: ")
    Label_15=Label(root, text ="Pressurant_Purge:")
    Label_16=Label(root, text ="Pressurant_Oxidizer:")
    Label_17=Label(root, text ="Oxidizer_fill:")
    Label_18=Label(root, text ="Oxidizer_Purge:")
    Label_19=Label(root, text ="Oxi_Combustion:")


    #Placing Widgets
    LabelOne.place(x=40, y=602)
    LabelTwo.place(x=175, y=602)
    LabelThree.place(x=275, y=602)
    LabelFour.place(x=370, y=602)
    LabelFive.place(x=40, y=640)
    LabelSix.place(x=40, y=660)
    LabelSeven.place(x=40, y=680)
    LabelEight.place(x=40, y=700)
    LabelNine.place(x=1100, y=420)
    LabelTen.place(x=1100, y=460)
    LabelEleven.place(x=1100,y=500)
    LabelTwelve.place(x=600, y=602)
    LabelThirteen.place(x=800, y=602)
    Label_14.place(x=600, y=640)
    Label_16.place(x=600, y=660)
    Label_17.place(x=600, y=680)
    Label_19.place(x=600, y=700)


    #Data Labels
    Label_data1=Label(root, text ="X")
    Label_data2=Label(root, text ="X")
    Label_data3=Label(root, text ="X")
    Label_data4=Label(root, text ="X")
    Label_data5=Label(root, text ="X")
    Label_data6=Label(root, text ="X")
    Label_data7=Label(root, text ="X")
    Label_data8=Label(root, text ="X")
    Label_data9=Label(root, text ="X")
    Label_data10=Label(root, text ="X")
    Label_data11=Label(root, text ="X")
    Label_data12=Label(root, text ="X")

    Label_Pressurant_Fill=Label(root, text ="X")
    Label_Pressurant_Oxidizer=Label(root, text ="X")
    Label_Oxidizer_fill=Label(root, text ="X")
    Label_Oxi_Combustion=Label(root, text ="X")

    #Place Data Labels
    Label_data1.place(x=175,y=640) #  Temp of Pressurant
    Label_data2.place(x=175,y=660) #  Temp Redundant of Pressurant
    Label_data3.place(x=175,y=680) #  Pressure of Pressurant 
    Label_data4.place(x=175,y=700) #  Pressure Redundant of Pressurant
    Label_data5.place(x=275,y=640) #  Temp of Oxidizer
    Label_data6.place(x=275,y=660) #  Temp Redundant of Oxidizer
    Label_data7.place(x=275,y=680) #  Pressure of Oxidizer
    Label_data8.place(x=275,y=700) #  Pressure Redundant of Oxidizer
    Label_data9.place(x=375,y=640) #  Temp of Combustion Chamber
    Label_data10.place(x=375,y=660)#  Temp Redundant of Combustion Chamber
    Label_data11.place(x=375,y=680)#  Pressure of Combustion Chamber
    Label_data12.place(x=375,y=700)#  Pressure Redundant of Combustion Chamber
        


    Label_Pressurant_Fill.place(x=815, y=640)
    Label_Pressurant_Oxidizer.place(x=815, y=660)
    Label_Oxidizer_fill.place(x=815, y=680)
    Label_Oxi_Combustion.place(x=815, y=700)


    # Buttons
    button = Button(root,text = "Send", command = send, width = 6).place(x=1020, y=500) # One way to send command to Control Sys
    CONNECT = Button(root,text = "Connect", command = connect).place(x=1020, y=420) # connect to the Control Sys
    DISCONNECT = Button(root,text = "Disconnect", command = disconnect).place(x=1020, y=540) # Close the program


    # Button Commands for Control System 
    
    button1 = Button(root,text = "Open P-Fill", command = open_Pressurant_fill, width = 12).place(x=1020, y=600)  
    button2 = Button(root,text = "Close P-Fill", command = close_Pressurant_fill, width = 12).place(x=1020, y=640)
    button3 = Button(root,text = "Open POIV", command = open_POIV, width = 12).place(x=1020, y=680)                                                                    
    button4 = Button(root,text = "Close POIV", command = close_POIV, width = 12).place(x=1020, y=720)  
    button5 = Button(root,text = "Open Oxi-Fill", command = open_Oxidizer_fill, width = 12).place(x=1180, y=600)
    button6 = Button(root,text = "Close Oxi-Fill", command = close_Oxidizer_fill, width = 12).place(x=1180, y=640)
    button7 = Button(root,text = "Launch", command = launch, width = 12).place(x=1180, y=680)
    button8 = Button(root,text = "Abort", command = Abort, width = 12).place(x=1180, y=720)
    button9 = Button(root,text = "Start Plot", command = Plot_Now, width = 12).place(x=1300, y=420)
    
    

   

    # Entry
    data_entry=Entry(width=7)
    data_entry.place(x=1200,y=500)

    baud_rate=Entry(width=7)
    baud_rate.place(x=1200,y=420)

    port_entry=Entry(width=7)
    port_entry.place(x=1200,y=460)

    # Add temporary plot figures
    fig = plt.figure()

    ax = fig.add_subplot(311)   #311  312 313
    ax.set_xlabel("Mission Time (Sec)")
    ax.set_ylabel("Temperature (C)")
    ax.set_title(" Pressurant Tank: ")
    ax.grid()
    ax2=ax.twinx()
    ax2.set_ylabel("Pressure (psi)")


    axtwo = fig.add_subplot(312)
    axtwo.set_xlabel("Mission Time (Sec)")
    axtwo.set_ylabel("Temperature (C)")
    axtwo.set_title(" Oxidizer Tank: ")
    axtwo.grid()
    axtwo2=axtwo.twinx()
    axtwo2.set_ylabel("Pressure (psi)")

    axthree = fig.add_subplot(313)
    axthree.set_xlabel("Mission Time (Sec)")
    axthree.set_ylabel("Pressure (psi)")
    axthree.set_title(" Combustion Tank: ")
    axthree.grid()

    plt.tight_layout()
    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().place(height=600 , width=1000)
    
    
    

         

root.mainloop()



