#include <SoftwareSerial.h>
#include <Wire.h>
#include <Servo.h>
#include <MPU6050_tockn.h>

SoftwareSerial BTSerial(10, 11); // RX | TX
MPU6050 mpu6050(Wire);
Servo servoHorizontal;
Servo servoVertical;

int pinServoHorizontal = 8;
int pinServoVertical = 9;
bool gyroEnabled = false;
unsigned long activationTime = 0; // Tiempo de activación del giroscopio
const long stabilizationPeriod = 5000; // Período de estabilización en milisegundos (5 segundos)

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  BTSerial.begin(9600);
  Wire.begin();

  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);

  servoHorizontal.attach(pinServoHorizontal);
  servoVertical.attach(pinServoVertical);
}

void loop() {
  if (BTSerial.available()) {
    char c = BTSerial.read();
    Serial.println(c);
    BTSerial.write(c);

    if (c == 'a') {
      gyroEnabled = true;
      activationTime = millis();
    }
  }

  // Activar el giroscopio sólo durante el período de estabilización
  if (gyroEnabled && (millis() - activationTime < stabilizationPeriod)) {
    mpu6050.update();

    int servoHPos = map(mpu6050.getAngleX(), 90, -90, -5, 180);
    int servoVPos = map(mpu6050.getAngleY(), -90, 90, 0, 180);

    servoHorizontal.write(servoHPos);
    servoVertical.write(servoVPos);
  } else {
    gyroEnabled = false;
  }

  // Puedes agregar un pequeño delay si es necesario
  // delay(100);
}
