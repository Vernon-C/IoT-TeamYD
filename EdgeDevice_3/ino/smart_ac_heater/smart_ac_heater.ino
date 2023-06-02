#include <Servo.h>

int potPin = A0;
int servoPin = 10;
int relayPin = 8;
int pirPin = 12;
int redledPin = 2;
int blueledPin = 4;

Servo myservo;

void setup() {
  Serial.begin(9600);
  
  myservo.attach(servoPin);
  
  pinMode(pirPin, INPUT);
  
  pinMode(relayPin, OUTPUT);
  pinMode(redledPin, OUTPUT);
  pinMode(blueledPin, OUTPUT);
}

void loop() {
  int potValue = analogRead(potPin);
  int motionDetected = digitalRead(pirPin);
  int servodegree = map(potValue, 0, 1023, 0, 180); 
  int temp = map(potValue, 0, 1023, 20, 30);

  Serial.print(temp);
  Serial.print(",");
  
  if (Serial.available())
  {
    int num = Serial.parseInt();

    if (motionDetected > 0){
      switch (num)
      {
        
        case 0:
            digitalWrite(redledPin, HIGH);
            digitalWrite(blueledPin, LOW);
            digitalWrite(relayPin, HIGH);
            myservo.write(0);
            break;
  
         default:
            digitalWrite(blueledPin, HIGH);
            digitalWrite(redledPin, LOW);
            digitalWrite(relayPin, LOW);
            myservo.write(servodegree);
            break; 

      }
    }else{
      digitalWrite(redledPin, LOW);
      digitalWrite(blueledPin, LOW);
      digitalWrite(relayPin, LOW);
      myservo.write(0);
    }
  }
    Serial.print(servodegree);
    Serial.println("");
    delay(1000);
}