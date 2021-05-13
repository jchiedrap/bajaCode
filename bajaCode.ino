// BAJA TEST CODE REV. 10: 28/12/2020
// CONTAINS GPS, SD, LCD, and GasLevel code
// Updates code to be in the system of "Gather, Display, Store". Further documentation found above each section. -Juan
#define gpsPort Serial1
#define GPS_PORT_NAME "Serial1"
#define DEBUG_PORT Serial

// LIBRARY INCLUSION
#include <SD.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <NMEAGPS.h>
#include <string.h>

// INITIALIZING VARIABLES

//  Debug Variables
int ledSD = 42; int ledGPS = 44; int ledFinishedSetup = 46;
bool bledSD, bledGPS, bledFinishedSetup;

//  Fuel Pins
int upfuel = 12; //pin for top fuel tank
int bottomfuel = 13; //pin for bottom fuel tank
bool lastUp = false;
bool lastBottom = false;

//    RPM Variables
int rpmMode = 1; // 1 = IR, 0 = Ind.
int rpmPin = A0; // temp
int rpmPinIR = 2;
int rpmCounter = 0;
int rpmDebug = -1;
unsigned long periodRpm = 0;

//    GPS Variables
const int gpsBaud = 9600;
NMEAGPS gps;
gps_fix fix;
double lat, lon, spd, hed;
int dd, mo, yyyy, hh, mi , ss;

//    SD Variables
File dataFile;

//    LCD Variables
LiquidCrystal_I2C lcd1 = LiquidCrystal_I2C(0x27, 16, 2);
LiquidCrystal_I2C lcd2 = LiquidCrystal_I2C(0x26, 16, 2);
uint8_t testChar[8] = {0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff}; // Custom char

//    Output Data Variables
String colNames = "Index,RPM,Gas,Latitude,Longitude,Speed,Heading,DDMMYYYYHHMMSS";
unsigned int i = 0;

//    dataOut Struct
int gas;
double rpm;
gps_fix currFix;


// SETUP
void setup() {

  // DEBUG LEDS SETUP
  pinMode(ledGPS, OUTPUT);
  pinMode(ledSD, OUTPUT);
  pinMode(ledFinishedSetup, OUTPUT);

  digitalWrite(ledGPS, HIGH);
  digitalWrite(ledSD, HIGH);

  delay(300);

  digitalWrite(ledGPS, LOW);
  digitalWrite(ledSD, LOW);
  bledGPS = bledSD = false;

  // SD CARD SETUP
  DEBUG_PORT.begin(9600);
  if (!SD.begin(53)) {
    DEBUG_PORT.println("SD DOES NOT WORK!");
  } else {
    DEBUG_PORT.println("SD works!");
  }

  dataFile = SD.open("dataFile.txt", FILE_WRITE);
  if (dataFile) {
    DEBUG_PORT.println("Writing!");
    dataFile.println(colNames);
    dataFile.close();
    DEBUG_PORT.println("Done!");
    bledSD = true;
    digitalWrite(ledSD, HIGH);
  } 
  else {
    DEBUG_PORT.println("Error opening file!");
  }

  // GPS SETUP
  gpsPort.begin(gpsBaud);
  bledGPS = true;
  digitalWrite(ledGPS, HIGH);

  // LCD SETUP
  lcd1.init();
  lcd1.backlight();
  lcd1.setCursor(2,0);  lcd1.print("ROUGH RIDER");
  lcd1.setCursor(5,1);  lcd1.print("HUD 1");
  lcd2.init();
  lcd2.createChar(1, testChar);
  lcd2.backlight();
  lcd2.setCursor(2,0);  lcd2.print("ROUGH RIDER");
  lcd2.setCursor(5,1);  lcd2.print("HUD 2");
  DEBUG_PORT.print("Should have printed!");
  lcd1.clear();
  lcd2.clear();

  // GAS SETUP
  pinMode(upfuel, INPUT_PULLUP);
  pinMode(bottomfuel, INPUT_PULLUP);

  // RPM SETUP 
  if (rpmMode == 1) {
    pinMode(rpmPinIR, INPUT_PULLUP);
  } else {
    pinMode(rpmPin, INPUT);
  }

  // FINALIZED DEBUG LEDS

  if (bledGPS && bledSD) {
    bledFinishedSetup = true;
    bledGPS = bledSD = false;
    digitalWrite(ledGPS, LOW);
    digitalWrite(ledSD, LOW);
    digitalWrite(ledFinishedSetup, HIGH);
    delay(300);
    digitalWrite(ledFinishedSetup, LOW);
  }

}

//  FUNCTIONS

//  DATA FUNCTIONS:

void gatherData() {
  // gather fuel
  bool top, bot = false;
  top = digitalRead(upfuel);
  bot = digitalRead(bottomfuel);

  if (top == 1 and bot == 1) gas = 2;
  else if (top == 0 and bot == 1) gas = -1;
  else if ((top == 1 and bot == 0)) gas = 1;
  else gas = 0;

  // gather GPS
  while (gps.available(gpsPort)) {
    digitalWrite(ledGPS, HIGH);
    currFix = gps.read();
  }
  lat = (double) currFix.latitudeL()*1e-7d;
  lon = (double) currFix.longitudeL()*1e-7d;
  spd = round(currFix.speed_kph()*100.00d)/100.00d;
  hed = currFix.heading();
  dd = currFix.dateTime.date; mo = currFix.dateTime.month; yyyy = currFix.dateTime.year;
  hh = currFix.dateTime.hours; mi = currFix.dateTime.minutes; ss = currFix.dateTime.seconds;
  digitalWrite(ledGPS, LOW);

  // gather RPM
  if (rpmMode == 1) {
    if (i > 0) {
      rpm = rpmCounter * 1e6 / periodRpm;
    } else rpm = 0;
  } else {
    // TODO: write code for Inductor test
  }
}

void displayData() {
  // display fuel
  lcd1.clear(); lcd2.clear();
  switch (gas) {
    case -1: 
      lcd2.setCursor(0, 0); lcd2.print("ERROR");
      break;
    case 0: 
      lcd2.setCursor(0, 0); 
      lcd2.setCursor(0, 1); lcd2.print("GAS UP BUTTERCUP");
      break;
    case 1: 
      for (int i = 0; i < 2; i++) {
        lcd2.setCursor(i, 0); lcd2.write(1);
      }
      break;
    case 2: 
      for (int i = 0; i < 4; i++) {
        lcd2.setCursor(i, 0); lcd2.write(1);
      }
      break;
    default: break;
  }

  // display gps data
    // display speed
  if (currFix.valid.speed) {
    lcd1.setCursor(0,0); lcd1.print("SPEED: ");
    lcd1.setCursor(7,0); lcd1.print(spd);
  } else {
    lcd1.setCursor(0,0); lcd1.print("SPEED: ");
    lcd1.setCursor(7,0); lcd1.print("N/A");
  }
    // display time
  if (currFix.valid.date) {
    lcd1.setCursor(0,1);  lcd1.print("TIME: ");
    lcd1.setCursor(6,1);  lcd1.print(hh); 
    lcd1.setCursor(8,1);  lcd1.print(":");
    lcd1.setCursor(9,1);  lcd1.print(mi); 
    lcd1.setCursor(11,1); lcd1.print(":");
    lcd1.setCursor(12,1); lcd1.print(ss); 
  } else {
    lcd1.setCursor(0,1);  lcd1.print("TIME: ");
    lcd1.setCursor(6,1);  lcd1.print("N/A"); 
  }

  // display RPM
  lcd2.setCursor(6, 0); lcd2.print("RPM: ");
  lcd2.setCursor(11, 0); lcd2.print((int) rpm);
}

void storeData() {

  // Activate dataFile

  digitalWrite(ledSD, HIGH);
  dataFile = SD.open("dataFile.txt", FILE_WRITE);

  if (dataFile) { // Ensure the file is available before writing to it
    // Write index
    dataFile.print(i); dataFile.print(",");

    // Write RPM and Gas

    dataFile.print(rpm); dataFile.print(",");
    dataFile.print(gas); dataFile.print(",");

    // Write location, speed, and heading

    dataFile.print(String(lat, 6)); dataFile.print(",");
    dataFile.print(String(lon, 6)); dataFile.print(",");
    Serial.println(String(lat, 6));
    Serial.println(String(lon, 6));
    dataFile.print(spd); dataFile.print(",");
    dataFile.print(hed); dataFile.print(",");

    // Write datetime

    dataFile.print(dd); dataFile.print(mo); dataFile.print(yyyy); 
    dataFile.print(hh); dataFile.print(mi); dataFile.print(ss);

    // Close dataFile to save

    dataFile.print("\n");
    dataFile.close();
    i++;
  }
  digitalWrite(ledSD, LOW);
}


//  rpmCount: [INTERRUPT] adds to rpmCounter every time the interrupt port is RISING
void rpmCount() {
  rpmCounter++;
}

//  LOOP: MAIN FUNCTIONS

void loop() {
  gatherData();
  rpmCounter = 0;
  attachInterrupt(digitalPinToInterrupt(rpmPinIR), rpmCount, RISING);
  periodRpm = micros();
  storeData();
  if (i % 5 == 0) displayData(); // lower refresh rate to increase display stability
  detachInterrupt(digitalPinToInterrupt(rpmPinIR));
  periodRpm = micros() - periodRpm;
  delay(10);

  //// DEPRECATED

  //GPSWrite();
  /* SD TEST CODE
  dataFile = SD.open("newFile.txt", FILE_WRITE);
  dataFile.println(millis());
  dataFile.close(); 
  */
  //gasDisplay();

  ////
}

/* Deprecated Functions


//    GPSWrite: Writes GPS data to sd card and outputs relevant data to LCD monitors
void GPSWrite() {
  int i = 0;
  while (gps.available(gpsPort)) {
    fix = gps.read();
    dataFile = SD.open("dataFile.txt", FILE_WRITE);
    dataFile.print(i); // print fix index

    if (fix.valid.location) {
      dataFile.print(',');
      dataFile.print(fix.latitude(), 6 );
      dataFile.print(',' );
      dataFile.print(fix.longitude(), 6 );
    }

    if (fix.valid.speed) {
      dataFile.print(',');
      dataFile.print(fix.speed_kph());
      lcd1.setCursor(0,0); lcd1.print("SPEED: ");
      lcd1.setCursor(7,0); lcd1.print(round(fix.speed_kph()*100)/100);
    }

    if (fix.valid.heading) {
      dataFile.print(',');
      dataFile.print(fix.heading());
    }

    if (fix.valid.date) {
      dataFile.print(',');
      dataFile.print(fix.dateTime.day); dataFile.print(fix.dateTime.month); dataFile.print(fix.dateTime.year); 
      dataFile.print(fix.dateTime.hours); dataFile.print(fix.dateTime.minutes); dataFile.println(fix.dateTime.seconds); 
      lcd1.setCursor(0,1);  lcd1.print("TIME: ");
      lcd1.setCursor(6,1);  lcd1.print(fix.dateTime.hours); 
      lcd1.setCursor(8,1);  lcd1.print(":");
      lcd1.setCursor(9,1);  lcd1.print(fix.dateTime.minutes); 
      lcd1.setCursor(11,1); lcd1.print(":");
      lcd1.setCursor(12,1); lcd1.print(fix.dateTime.seconds); 
    }
    dataFile.close();
    i++;
  }
}

//    gasDisplay: Measures gas levels and outputs them to LCD2
void gasDisplay() {
 //if (digitalRead(upfuel) != lastUp || digitalRead(bottomfuel) != lastBottom) {
    if (digitalRead(upfuel) == LOW && digitalRead(bottomfuel) == LOW) {
     lcd2.setCursor(0,0); 
     lcd2.write(1);
     lcd2.setCursor(1,0); 
     lcd2.write(1);
     lcd2.setCursor(2,0); 
     lcd2.write(1);
     lcd2.setCursor(3,0); 
     lcd2.write(1);
     lcd2.setCursor(4,0); 
     lcd2.write(1);
     lcd2.setCursor(5,0); 
     lcd2.write(1);
     delay(500);
     lcd2.clear();
      //lcd2.setCursor(0,0);
      //lcd2.print(">66%");
      //delay(500);
      //lcd2.clear();
      
    }

    if (digitalRead(upfuel) == LOW && digitalRead(bottomfuel) == HIGH) {// when gas tank is around half full(between 1/3 abd 2/3 - bottom mag on top off)   
     lcd2.setCursor(0,0); 
     lcd2.write(1);
     lcd2.setCursor(1,0); 
     lcd2.write(1);
     lcd2.setCursor(2,0); 
     lcd2.write(1);
     lcd2.setCursor(3,0); 
     lcd2.write(1);
     delay(500);
     lcd2.clear();
      //lcd2.setCursor(0,0);
      //lcd2.print(">35%");
      //delay(500);
      //lcd2.clear();
    }

    if (digitalRead(upfuel) == HIGH && digitalRead(bottomfuel) == HIGH)   {//When gas tank is near empty(between 0/3 and 2/3 - both mag sensors off)
     lcd2.setCursor(0,0); 
     lcd2.write(1);
     lcd2.setCursor(1,0); 
     lcd2.write(1);
     lcd2.setCursor(0,1); 
     lcd2.print("GAS UP BUTTERCUP"); 
     delay(500);
     lcd2.clear();
      //lcd2.print("REFUEL! 1/3 LEFT");     
      //delay(500);
      //lcd2.clear();
    }
    DEBUG_PORT.print(digitalRead(upfuel));
    DEBUG_PORT.println(digitalRead(bottomfuel));
  //lastUp = digitalRead(upfuel);
  //lastBottom = digitalRead(bottomfuel);
  //}
}

*/
