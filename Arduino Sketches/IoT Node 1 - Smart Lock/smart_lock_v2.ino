#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include "Ultrasonic.h"
// #include <simpleRPC.h>

#define SS_PIN 10
#define RST_PIN 9
#define LED_G 2
#define LED_R 8
#define SERVO_PIN 3

MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo myServo;
Ultrasonic ultrasonic(4, 7);
int distance;
int no_of_ent = 0;
int angle = 90;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  myServo.attach(SERVO_PIN);
  myServo.write(angle);  // Default state is locked
  pinMode(LED_G, OUTPUT);
  pinMode(LED_R, OUTPUT);
  digitalWrite(LED_R, HIGH);  // Default state is locked
  Serial.println("----- Begin -----");
  Serial.println();
}

// RPC_Response processSwitchChange

// const size_t callbacks_size = 2;
// RPC_Callback callbacks[callbacks_size] = {
//    { "example_set_temperature", processTemperatureChange },
//    { "example_set_switch", processSwitchChange }
// };

bool subscribe = false;

void loop() {
  if (Serial.available()) {

    char receivedData = Serial.read();

    if (receivedData == '0') {
      digitalWrite(LED_G, HIGH);
      delay(2000);
      digitalWrite(LED_G,HIGH);
      delay(2000);
    } else if (receivedData == '1') {
      digitalWrite(LED_R, HIGH);
      delay(2000);
      digitalWrite(LED_R,HIGH);
      delay(2000);
    }
  }
  /* RPC test */


  /* Ultrasonic sensor */
  // distance = ultrasonic.read(CM);
  // Serial.println(distance);

  // if (distance <= 5) {
  //   Serial.println("Entity entered");
  // }

  // delay(1000);

  /* Check if an entity has entered the room */
  if (angle == 0) {
    /* Ultrasonic sensor */
    distance = ultrasonic.read(CM);
    //Serial.println(distance);

    if (distance <= 5) {
      no_of_ent += 1;
      Serial.print("Entity(s): ");
      Serial.println(no_of_ent);
      delay(2000);
    }
  }

  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
  {
    return;
  }

  // Show UID on serial monitor
  Serial.print("UID tag: ");
  
  String content = "";
  byte letter;

  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }

  Serial.println();
  Serial.print("Message: ");
  content.toUpperCase();

  /* Check if UID matches for authorisation */
  // Authorised access
  if (content.substring(1) == "E2 ED 71 19") {
    Serial.println("Authorised access");
    Serial.println();
    delay(500);
    digitalWrite(LED_G, HIGH);
    myServo.write(180);
    // delay(5000);

    if (angle == 90) {
      angle = 0;
      myServo.write(angle);
      Serial.println("Status: Unlocked");
      digitalWrite(LED_R, LOW);
      digitalWrite(LED_G, HIGH);

    } else if (angle != 90) {
      angle = 90;
      myServo.write(angle);
      Serial.println("Status: Locked");
      digitalWrite(LED_G, LOW);
      digitalWrite(LED_R, HIGH);
      no_of_ent = 0;
      Serial.print("Entity(s): ");
      Serial.println(no_of_ent);
    }

    // myServo.write(0);
    // digitalWrite(LED_G, LOW);
  } else {
    Serial.println("Access denied");
    digitalWrite(LED_R, HIGH);
    delay(500);
  }

  /* Ultrasonic sensor */
  // distance = ultrasonic.read(CM);
  // Serial.println(distance);

  // if (distance <= 5) {
  //   Serial.println("Entity entered");
  // }

  delay(2000);
}
