#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_LSM303_Mag_Unified mag = Adafruit_LSM303_Mag_Unified(12345);

// Bump/start switch pins
const int bump_switch = 4;
const int start_switch = 5;

// Compass calibration 
float MaxX = -9999;
float MinX = 9999;
float MaxY = -9999;
float MinY = 9999;

void setup(void) 
{
  Serial.begin(9600);
  Serial.println("Magnetometer Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }

  // Set bump/switch pins
  pinMode(bump_switch, INPUT_PULLUP);
  pinMode(start_switch, INPUT_PULLUP);
}

void loop(void) 
{
  /* Get a new sensor event */ 
  sensors_event_t event; 
  mag.getEvent(&event);

  if (event.magnetic.x > MaxX){
    MaxX = event.magnetic.x;
    
  }
  if (event.magnetic.y > MaxY){
    MaxY = event.magnetic.y;
  }
  if (event.magnetic.x < MinX){
    MinX = event.magnetic.x;
  }
  if (event.magnetic.y < MinY){
    MinY = event.magnetic.y;
  }
  
  
  Serial.print(MaxX); Serial.print(",");Serial.print(MaxY);Serial.print(",");Serial.print(MinX);Serial.print(",");Serial.println(MinY);
  delay(500);
}
