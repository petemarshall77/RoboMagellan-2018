#include <SoftwareSerial.h>

SoftwareSerial xbee(6, 7);

unsigned long xbee_start_time;

void setup() {

  xbee.begin(9600);
  //pinMode(5, OUTPUT);
  //pinMode(13, OUTPUT);
  pinMode(10, OUTPUT);
  Serial.begin(9600);

  xbee_start_time = micros();

}

void loop() {

  if(xbee.available()){

    char dataStatus = xbee.read();
    
    if(dataStatus == 'y'){
      xbee_start_time = micros();
      
    }
  }

  if(micros() - xbee_start_time > 200000){
    //digitalWrite(5, LOW);
    //digitalWrite(13, LOW);
    digitalWrite(10, LOW);
    Serial.println("LOW");
  }else{
    //digitalWrite(5, HIGH);
    //digitalWrite(13, HIGH);
    digitalWrite(10, HIGH);
    Serial.println("HIGH");
  }
  Serial.flush();

}
