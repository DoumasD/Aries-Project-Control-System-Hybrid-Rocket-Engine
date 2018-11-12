// Demetrios Doumas   8/4/18 Final  Aries Project
// Hybrid Rocket Engine control System Code


//Function Headers

void Open_Pressurant_Tank();
void Close_Pressurant_Tank();
void Open_POIV();//Open Pressurant_Oxidizer Valve
void Close_POIV();//Close Pressurant_Oxidizer Valve
void Open_Oxidizer_Tank();
void Close_Oxidizer_Tank();
void Launch();
void Abort();


//Declarations and initalization of data collection variables

int inputByte=0; // Used for reading commands

float mission_time;  //keep track of time in millis seconds

//Pressurant tank
float temp1=0;
float temp2=0;
float pressure1=0;
float pressure2=0;

//Oxidizer tank
float temp3=0;
float temp4=0;
float pressure3=0;
float pressure4=0;

//Combustion tank
float temp5=0;
float temp6=0;
float pressure5=0;
float pressure6=0;


//Valve indicators initialize to zero meaning initally low signal
int Pressurant_Fill_Indicator=0; 
int Oxidizer_Fill_Indicator=0;
int Pressurant_Oxidizer_Indicator=0;
int Oxidizer_Combustion_Indicator=0;

////////////////////////////////////////////////////Set Digital port of the valves
// Selonoid Pins
int PressurantFillPin=22;   //Also known as P-Fill
int POIV_Pin=25; // valve seperation between Pressurant & Oxidizer
int PRTPRV_Pin=24;
int OxidizerFillPin=23;    //Also known as Ox-Fill
int ORTPRV_Pin=26;
int MIV_Pin=27; //oxidizerCombustionPin



// Pins are Ports on the Arduino Mega 2560 
////////////////////////////////////////////////////// Set ignition port for launch
int ignitionPin=40;   // digital pin "heater"    

///////////////////////////////////////////////////// Temperture Sensors Pins

int PressurantTemp = A2;
int OxidizerTemp =A3;

///////////////////////////////////////////////////// Pressure Sensors  Pins

int PressurantPressure=A5;
int OxidizerPressure=A6;
int CombustionPressure=A7;




///////////////////////////////////////// Setting Limit Protections

float pressurant_temp_limit = 9999;  // Fill in by Michael
float pressurant_pressure_limit = 50.0;
float oxidizer_temp_limit=9999;      // Fill in by Michael
float oxidizer_pressure_limit= 50.0; 



// Level for closeing the fill valves 
// Below are testing values 
float pressure_pressuarnt_level=20;   // Fill in By Michael
float pressure_oxidizer_level=30;     // Fill in By Michael

float Upper_pressuarnt_level= pressure_pressuarnt_level + (pressure_pressuarnt_level*.1);
float Lower_pressuarnt_level= pressure_pressuarnt_level - (pressure_pressuarnt_level*.1);


float Upper_oxidizer_level= pressure_oxidizer_level + (pressure_oxidizer_level*.1);
float Lower_oxidizer_level= pressure_oxidizer_level - (pressure_oxidizer_level*.1);


// Counters for over pressure in Oxidizer & Pressurant Tanks
int i=0;
int j=0;


void setup() {

// Enable serial communication with a buad rate of 9600
Serial.begin(9600);
Serial1.begin(9600);


//Set digital i/o pins to outputs
pinMode(PressurantFillPin,OUTPUT);
pinMode(POIV_Pin,OUTPUT);
pinMode(PRTPRV_Pin,OUTPUT);
pinMode(OxidizerFillPin,OUTPUT);
pinMode(ORTPRV_Pin,OUTPUT);
pinMode(MIV_Pin,OUTPUT);
pinMode(ignitionPin,OUTPUT);



}

void loop() {


mission_time=millis(); // Start time
  
///////////////////////////////////////////////////// Calculate Temperature, Pressure, of Tanks
/////////////////////////// Pressurant Tank
temp1=(analogRead(PressurantTemp))*(5.0/1024.0)*100;   // 10mv per degree celcusis 
pressure1= (((analogRead(PressurantPressure))*(5.0/1024.0))- .469)/.0276;

////////////////////////// Oxidizer Tank

temp3=(analogRead(OxidizerTemp))*(5.0/1024.0)*100;   // 10mv per degree celcusis 
//pressure3= (((analogRead(OxidizerPressure))*(5.0/1024.0))- .483)/.006;
pressure3= (((analogRead(OxidizerPressure))*(5.0/1024.0))- .680)/.006;




///////////////////////// Combustion Tank

pressure5= (((analogRead(CombustionPressure))*(5.0/1024.0))- .483)/.006;




/////////////////////////////////////////////////////////////////////////////////Actuation 





// Increasing counter # of times either pressure or temperature remain constant
if ((temp1 > pressurant_temp_limit)  ||  (pressure1 > pressurant_pressure_limit))
{
i++;
}
else
{
i=0;  
}

// Make sure no overpressure or temperature in the pressurant tank
// If pressure or temp is constant for over 5 readings then abort
if (  ((temp1 > pressurant_temp_limit)  ||  (pressure1 > pressurant_pressure_limit)) && (i==5))  
{
Abort();  
}





// Close P-fill valve if pressure in the pressurant tank is meet
if (     (pressure1 >= Lower_pressuarnt_level)   &&       (pressure1 <= Upper_pressuarnt_level)  )
{
Close_Pressurant_Tank();  
}


// Close Oxi-fill valve if pressure in the oxidizer tank is meet
if (     (pressure3 >= Lower_oxidizer_level)   &&       (pressure3 <= Upper_oxidizer_level)  )
{
Close_Oxidizer_Tank(); 
}







// Increasing counter # of times either pressure or temperature remain constantly above pressure or temperature limit of the oxidizer tank.
if ((temp3 > oxidizer_temp_limit)  ||  (pressure3 > oxidizer_pressure_limit))
{
j++;
}
else
{
j=0;  
}



// Make sure no overpressure or temperature in the oxidizer tank
// If pressure or temp is constant for over 5 readings then abort
if (  ((temp3 > oxidizer_temp_limit)  ||  (pressure3 > oxidizer_pressure_limit)) && (j==5))  
{
Abort();  
}






/////////////////////////////////////////////////////////////////////////////////Read commands

    if(Serial1.available()>0){    // Wait for a command from serial port 1 of the Arduino   wireless connection
        
        inputByte= Serial1.read();  // Store command

     }


   // Switch case Commnands
   switch(inputByte){
     case 49:    // 1
       Open_Pressurant_Tank();
       break;
     case 50:   // 2
       Close_Pressurant_Tank();
       break;
     case 51:   //3
       Open_POIV();
       break;
     case 52:   //4
       Close_POIV();
       break;
     case 53:  //5
       Open_Oxidizer_Tank();
       break;
     case 54:  //6
       Close_Oxidizer_Tank();
       break;
     case 55:  //7
       Launch();
       break;
     case 56:  //8
       Abort();
       break;
     default:
       break;
   }  
   

//Serial print data calculation


  
Serial1.print(mission_time/1000);   // index 0 data
Serial1.print(",");
Serial1.print(temp1);
Serial1.print(",");
Serial1.print(temp2);
Serial1.print(",");
Serial1.print(pressure1);
Serial1.print(",");
Serial1.print(pressure2);
Serial1.print(",");
Serial1.print(temp3);
Serial1.print(",");
Serial1.print(temp4);
Serial1.print(",");
Serial1.print(pressure3);
Serial1.print(",");
Serial1.print(pressure4);
Serial1.print(",");
Serial1.print(temp5);
Serial1.print(",");
Serial1.print(temp6);
Serial1.print(",");
Serial1.print(pressure5);
Serial1.print(",");
Serial1.print(pressure6);
Serial1.print(",");
Serial1.print(Pressurant_Fill_Indicator);
Serial1.print(",");
Serial1.print(Pressurant_Oxidizer_Indicator);
Serial1.print(",");
Serial1.print(Oxidizer_Fill_Indicator);
Serial1.print(",");
Serial1.print(Oxidizer_Combustion_Indicator);
Serial1.println("");





delay(1000); // used to sync with the GUI
}


void Open_Pressurant_Tank()
{
digitalWrite(PRTPRV_Pin,HIGH);  // close relief valve normally open
digitalWrite(PressurantFillPin,HIGH);
Pressurant_Fill_Indicator=1;
inputByte=0;   //  Reset Command variable to zero
}

void Close_Pressurant_Tank()
{
digitalWrite(PressurantFillPin,LOW);
Pressurant_Fill_Indicator=0;  
inputByte=0;   //  Reset Command variable to zero
}




void Open_POIV()//Open Pressurant_Oxidizer
{
digitalWrite(POIV_Pin,HIGH);
Pressurant_Oxidizer_Indicator=1;
inputByte=0;    //  Reset Command variable to zero
}

void Close_POIV()//Close Pressurant_Oxidizer
{
digitalWrite(POIV_Pin,LOW);
Pressurant_Oxidizer_Indicator=0;
inputByte=0;    //  Reset Command variable to zero
}




void Open_Oxidizer_Tank()
{
digitalWrite(ORTPRV_Pin,HIGH);  // close relief valve normally open
digitalWrite(OxidizerFillPin,HIGH);
Oxidizer_Fill_Indicator=1;  
inputByte=0;    //  Reset Command variable to zero
}

void Close_Oxidizer_Tank()
{
digitalWrite(OxidizerFillPin,LOW);  
Oxidizer_Fill_Indicator=0;
inputByte=0;  //  Reset Command variable to zero
}





void Launch()
{

// Heat up the parafain  (Solid Fuel Grain)
digitalWrite(ignitionPin,HIGH);
delay(5000); //wait to heat up wax
//Opening the Main isolation Valve
//Once liquid or vapor from oxidizer tank reaches the solid fuel grain ignition starts
digitalWrite(MIV_Pin,HIGH);
Oxidizer_Combustion_Indicator=1;
inputByte=0;  //Important because this is used to reset the command variable in order to continue sending data.
}


void Abort()
{
  
//Stop Filling tanks
digitalWrite(PressurantFillPin,LOW);
digitalWrite(OxidizerFillPin,LOW);   
//Open POIV  becarefull valve is normally open  * Needed to release pressurant gas to atmoshphere 
digitalWrite(POIV_Pin,LOW);
digitalWrite(PRTPRV_Pin,LOW);
digitalWrite(ORTPRV_Pin,LOW);
digitalWrite(MIV_Pin,LOW);
digitalWrite(ignitionPin,LOW);

//Valve indicators initialize to zero meaning initally no signal
Pressurant_Fill_Indicator=0; 
Oxidizer_Fill_Indicator=0;
Pressurant_Oxidizer_Indicator=0;
Oxidizer_Combustion_Indicator=0;
// Retart the counters back to zero
j=0;
i=0;

inputByte=0;   //  Reset Command variable to zero

}
