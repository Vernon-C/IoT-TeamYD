#include <Servo.h>

Servo myservo;

int PIR = 12;
int alarm = 13;
int pwm = A0;
int servo = 11;
int led_open = 7;
int led_close = 2;

void setup() {
  // put your setup code here, to run once:
  pinMode(PIR, INPUT);
  pinMode(alarm, OUTPUT);
  pinMode(pwm, INPUT);
  pinMode(led_open, OUTPUT);
  pinMode(led_close, OUTPUT);
  myservo.attach(servo);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    int num = Serial.parseInt();

    if (digitalRead(PIR) >0){
      switch(num){
        case 0:
        // If no someone there and motion detected
        // alarm will be triggered
          digitalWrite(alarm, HIGH);
          digitalWrite(led_open, HIGH);
          break;
      
      default:
        // If someone is there, the alarm will not be triggered
          myservo.write(180);
          digitalWrite(alarm,LOW);
          break;
        
      }
    }
  }else{
    int PIR_value = digitalRead(PIR);
    int pot_value = analogRead(pwm);
    int door = map(pot_value, 0, 1023, 0, 180);
    
    myservo.write(door);
  
    
    if (door > 0){
      digitalWrite(led_open, HIGH);
      delay(50);
      digitalWrite(led_open, LOW);
      delay(50);
      digitalWrite(led_close, LOW);
      Serial.print("1");
    }else{
      digitalWrite(led_close, HIGH);
      Serial.print("0");
    }
  
    if (PIR_value == 1 && door > 0){
      digitalWrite(alarm, HIGH);
      Serial.print(", 1\n");
    }else{
      digitalWrite(alarm, LOW);
      Serial.print(", 0\n");
    }
  
    
  }
  delay(1000);
}
