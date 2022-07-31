#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiServer.h>
 
const char* ssid = "Hacker station";
const char* password =  "1445c6072773";
const int port = 666;

const char startCharacter = '<';
const char endCharacter = '>';

char operation;
char side; 

const int leftMotorPin = 5;   // D1
const int rightMotorPin = 4;  //D2
const int wifiLedPin = 0;     // D3
const int clientLedPin = 2;   // D4

const int motorPower = 255; // 0 - 255
const int ledPower = 100;   // 0 - 255
int value;

String message;

WiFiServer wifiServer(port);

void motorHandler() {
  side = message[0];
  operation = message[1];

  if (operation == 'D') {
    value = motorPower;
  } else {
    value = 0;
  }
  if (side == 'L') {
    analogWrite(leftMotorPin, value);
  } else {
    analogWrite(rightMotorPin, value);
  }
}


void setup() {
  pinMode(leftMotorPin, OUTPUT);
  pinMode(rightMotorPin, OUTPUT);
  pinMode(wifiLedPin, OUTPUT);
  pinMode(clientLedPin, OUTPUT);
 
  Serial.begin(115200);
 
  delay(1000);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
    analogWrite(wifiLedPin, 0);
  }

  Serial.println("Connected to the WiFi network");
  Serial.println("IP: " + WiFi.localIP().toString());
  analogWrite(wifiLedPin, ledPower);
  
  wifiServer.begin();
  
}
 
void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    analogWrite(wifiLedPin, 0);
  } else {
    analogWrite(wifiLedPin, ledPower);
  }
 
  WiFiClient client = wifiServer.available();
 
  if (client) {
    Serial.println("Client connected");
    analogWrite(clientLedPin, ledPower);

    while (client.connected()) {

      while (client.available()>0) {
        char c = client.read();
        
        if (c == startCharacter) {
          message = "";
        } else if (c == endCharacter) {
          motorHandler();
        } else {
          message = message + c;
        }
        // Serial.println(message);
      }
      
      delay(10);
    }
 
    client.stop();
    Serial.println("Client disconnected");
    analogWrite(clientLedPin, 0);
 
  }
 
delay(100);
}

