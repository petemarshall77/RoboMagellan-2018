#include <Wire.h>

#define Addr 0x1E               // 7-bit address of HMC5883 compass

const int bump_switch = 4;
const int start_switch = 5;

void setup() {
  Serial.begin(9600);
  delay(100);                   // Power up delay
  Wire.begin();
  pinMode(bump_switch, INPUT_PULLUP);
  pinMode(start_switch, INPUT_PULLUP);
  
  // Set operating mode to continuous
  Wire.beginTransmission(Addr); 
  Wire.write(byte(0x02));
  Wire.write(byte(0x00));
  Wire.endTransmission();
}

void loop() {
  int x, y, z;

  // Initiate communications with compass
  Wire.beginTransmission(Addr);
  Wire.write(byte(0x03));       // Send request to X MSB register
  Wire.endTransmission();

  Wire.requestFrom(Addr, 6);    // Request 6 bytes; 2 bytes per axis
  if(Wire.available() <=6) {    // If 6 bytes available
    x = Wire.read() << 8 | Wire.read();
    z = Wire.read() << 8 | Wire.read();
    y = Wire.read() << 8 | Wire.read();
  }
  
  // Output X and Y values
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");

  // Switch states
  int bump_state = !digitalRead(bump_switch);
  int start_state = !digitalRead(start_switch);

  Serial.print(bump_state);
  Serial.print(",");
  Serial.println(start_state);
  delay(100);
}
