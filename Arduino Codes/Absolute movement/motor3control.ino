#include "Arduino.h"
#include "AX12A.h"

#define DirectionPin  (10u)
#define BaudRate      (1000000ul)
#define ID            (3u)

int target_pos = 512; // Initial position
const int MIN_POS = 0;   // Minimum position for AX-12A
const int MAX_POS = 1023; // Maximum position for AX-12A

String inputString = ""; // String to hold incoming serial data
bool stringComplete = false; // Flag for completed input

void setup()
{
  Serial.begin(BaudRate); // Start Serial at AX-12A baud rate
  ax12a.begin(BaudRate, DirectionPin, &Serial); // Initialize AX-12A on same Serial
  inputString.reserve(10); // Reserve space for input string
  ax12a.move(ID, target_pos); // Move to initial position
  delay(100); // Wait for motor to stabilize
  Serial.begin(9600); // Switch to Serial Monitor baud rate
  Serial.println("Enter a position (0 to 1023 or negative for reverse):");
}

void loop()
{
  // Read input from Serial Monitor
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') { // Check for newline to complete the input
      stringComplete = true;
      break;
    } else {
      inputString += inChar; // Add character to input string
    }
  }

  // Process input if complete
  if (stringComplete) {
    // Switch Serial to AX-12A baud rate
    Serial.end();
    Serial.begin(BaudRate);
    
    // Convert string to integer
    int new_pos = inputString.toInt();
    
    // Validate the position
    if (new_pos >= MIN_POS && new_pos <= MAX_POS) {
      target_pos = new_pos;
      ax12a.move(ID, target_pos); // Move motor to the target position
      delay(50); // Allow motor to move
    }
    
    // Switch back to Serial Monitor baud rate
    Serial.end();
    Serial.begin(9600);
    
    // Provide feedback
    if (new_pos >= MIN_POS && new_pos <= MAX_POS) {
      Serial.print("Moving to position: ");
      Serial.println(target_pos);
    } else {
      Serial.println("Invalid position! Enter a value between 0 and 1023.");
    }
    
    // Clear the string and flag
    inputString = "";
    stringComplete = false;
    
    Serial.println("Enter a new position:");
  }
}