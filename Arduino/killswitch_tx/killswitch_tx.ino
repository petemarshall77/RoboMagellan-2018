#include <SoftwareSerial.h>

SoftwareSerial xbee(5,6);

const int buttonPin = 2;
int buttonState = 0;

void setup() {
  xbee.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  buttonState = digitalRead(buttonPin);

  if(buttonState == LOW){
    xbee.write("y\n");
    delay(200);
    
  }else{
    xbee.write("n\n");
    delay(200);
  }

}

