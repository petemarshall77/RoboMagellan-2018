#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_LSM303_Mag_Unified mag = Adafruit_LSM303_Mag_Unified(12345);

// Bump/start switch pins
const int bump_switch = 4;
const int start_switch = 5;

// Compass calibration 
float MaxX = 53.82;
float MinX = -22.18;
float MaxY = 19.27;
float MinY = -52.45;

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
  
  float Pi = 3.14159;
  
  // Calculate the angle of the vector y,x
  float normal_X = (event.magnetic.x - MinX) * (2.0) / (MaxX - MinX) - 1.0;
  float normal_Y = (event.magnetic.y - MinY) * (2.0) / (MaxY - MinY) - 1.0;
  float heading = (atan2(normal_Y,normal_X) * 180) / Pi;
  
  // Normalize to 0-360
  if (heading < 0)
  {
    heading = 360 + heading;
  }

  // Switch states
  int bump_state = !digitalRead(bump_switch);
  int start_state = !digitalRead(start_switch);
  
  Serial.print(heading); Serial.print(",");Serial.print(bump_state);Serial.print(",");Serial.println(start_state);
  delay(500);
}
