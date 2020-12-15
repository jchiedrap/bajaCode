// BAJA TEST CODE REV. 9: 12/MAY/2020
// CONTAINS GPS, SD, LCD, and GasLevel code
// Sent by Ozan - May 12th
#define gpsPort Serial1
#define GPS_PORT_NAME "Serial1"
#define DEBUG_PORT Serial

// LIBRARY INCLUSION
#include <SD.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <NMEAGPS.h>

// INITIALIZING VARIABLES

//  Fuel Pins
int upfuel = 22;//pin for top fuel tank
int bottomfuel = 23;//pin for bottom fuel tank
bool lastUp = false;
bool lastBottom = false;

//    RPM Variables
int rpmMode = 1; // 1 = IR, 0 = Ind.
int rpmPin = A0; // temp
int rpmPinIR = 2;
int rpmCounter = 0;
unsigned long periodRpm = 0;

//    GPS Variables
const int gpsBaud = 9600;
NMEAGPS gps;
gps_fix fix;

//    SD Variables
File dataFile;

//    LCD Variables
LiquidCrystal_I2C lcd1 = LiquidCrystal_I2C(0x27, 16, 2);
LiquidCrystal_I2C lcd2 = LiquidCrystal_I2C(0x26, 16, 2); // CHANGE PORT FOR SECOND LCD
uint8_t testChar[8] = {0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff}; // Custom char

//    Output Data Variables
String colNames = "Ind,RPM,Gas,Lat,Lon,Spd,Head,DMYHMS";
unsigned int i = 0;

//    dataOut Struct

struct DataBlip
{
  int gas;
  double rpm;
  gps_fix currFix;
};


// SETUP
void setup() {

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
  } 
  else {
    DEBUG_PORT.println("Error opening file!");
  }
  // GPS SETUP
  gpsPort.begin(gpsBaud);
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
  pinMode(upfuel, INPUT);
  pinMode(bottomfuel, INPUT);
  // RPM SETUP 
  if (rpmMode == 1) {
    pinMode(rpmPinIR, INPUT_PULLUP);
  } else {
    pinMode(rpmPin, INPUT);
  }

}

//  FUNCTIONS

//  DATA FUNCTIONS:

void gatherData(DataBlip d) {
  // gather fuel
  if (digitalRead(upfuel) == LOW) { // if the top one is floating
    d.gas = (digitalRead(bottomfuel) == LOW) ? 2 : -1;
  } else {
    d.gas = (digitalRead(bottomfuel) == LOW) ? 1 : 0;
  }

  // gather GPS
  while (gps.available(gpsPort)) d.currFix = gps.read();

  // gather RPM
  if (rpmMode == 1) {
    d.rpm = (i > 0) ? ((rpmCounter * 1e6) / (periodRpm)) : 0;
  } else {
    // TODO: write code for Inductor test
  }
}

void displayData(DataBlip d) {
  // display fuel
  switch (d.gas) {
    case -1: 
      lcd2.setCursor(0, 0); lcd2.print("ERROR");
      break;
    case 0: 
      lcd2.setCursor(0, 0); lcd2.blink();
      lcd2.setCursor(0, 1); lcd2.print("GAS UP BUTTERCUP");
      break;
    default:
      for (int i = 0; i < d.gas*2; i++) {
        lcd2.setCursor(i, 0); lcd2.write(1);
      }
      break;
  }

  // display gps data
    // display speed
  if (d.currFix.valid.speed) {
    lcd1.setCursor(0,0); lcd1.print("SPEED: ");
    lcd1.setCursor(7,0); lcd1.print(round(d.currFix.speed_kph()*100)/100);
  } else {
    lcd1.setCursor(0,0); lcd1.print("SPEED: ");
    lcd1.setCursor(7,0); lcd1.print("N/A");
  }
    // display time
  if (d.currFix.valid.date) {
    lcd1.setCursor(0,1);  lcd1.print("TIME: ");
    lcd1.setCursor(6,1);  lcd1.print(d.currFix.dateTime.hours); 
    lcd1.setCursor(8,1);  lcd1.print(":");
    lcd1.setCursor(9,1);  lcd1.print(d.currFix.dateTime.minutes); 
    lcd1.setCursor(11,1); lcd1.print(":");
    lcd1.setCursor(12,1); lcd1.print(d.currFix.dateTime.seconds); 
  } else {
    lcd1.setCursor(0,1);  lcd1.print("TIME: ");
    lcd1.setCursor(6,1);  lcd1.print("N/A"); 
  }

  // display RPM
  lcd2.setCursor(6, 1); lcd2.print("RPM: ");
  lcd2.setCursor(11, 1); lcd2.print((int) d.rpm);
}

void storeData(DataBlip d) {
  dataFile = SD.open("dataFile.txt", FILE_WRITE);
  String blip = "";

  blip += i; blip += ",";

  blip += d.rpm; blip += ",";
  blip += d.gas; blip += ",";

  if (d.currFix.valid.location) {
    blip += round(d.currFix.latitude()*1000000)/1000000; blip += ",";
    blip += round(d.currFix.longitude()*1000000)/1000000; blip += ",";
    blip += round(d.currFix.speed_kph()*100)/100; blip += ",";
    blip += d.currFix.heading(); blip += ",";
  } else {
    for (int j = 0; j < 4; j++) {
      blip += "ERROR"; blip += ",";
    }
  }

  if (d.currFix.valid.date) {
    blip += d.currFix.dateTime.day; blip += d.currFix.dateTime.month; blip += d.currFix.dateTime.year; 
    blip += d.currFix.dateTime.hours; blip += d.currFix.dateTime.minutes; blip += d.currFix.dateTime.seconds;
  } else {
    blip += "ERROR";
  }

  dataFile.print(blip);
  dataFile.close();

  i++;
}

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
      /*lcd2.setCursor(0,0);
      lcd2.print(">66%");
      delay(500);
      lcd2.clear();*/
      
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
      /*lcd2.setCursor(0,0);
      lcd2.print(">35%");
      delay(500);
      lcd2.clear();*/
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
      /*lcd2.print("REFUEL! 1/3 LEFT");     
      delay(500);
      lcd2.clear();*/
    }
    DEBUG_PORT.print(digitalRead(upfuel));
    DEBUG_PORT.println(digitalRead(bottomfuel));
  //lastUp = digitalRead(upfuel);
  //lastBottom = digitalRead(bottomfuel);
  //}
}

//  rpmCount: [INTERRUPT] adds to rpmCounter every time the interrupt port is RISING
void rpmCount() {
  rpmCounter++;
}

//  rpmCalc: Calculate RPM
void rpmCalc() {

}

//  LOOP: MAIN FUNCTIONS

void loop() {
  DataBlip data;
  gatherData(data);
  attachInterrupt(digitalPinToInterrupt(rpmPinIR), rpmCount, RISING);
  periodRpm = micros();
  displayData(data);
  storeData(data);
  detachInterrupt(digitalPinToInterrupt(rpmPinIR));
  periodRpm = micros() - periodRpm;
  //GPSWrite();
  /* SD TEST CODE
  dataFile = SD.open("newFile.txt", FILE_WRITE);
  dataFile.println(millis());
  dataFile.close(); 
  */
  //gasDisplay();
  delay(10);
}