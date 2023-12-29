#include <Wire.h>
#include <Servo.h>
#include <MPU6050_tockn.h>

MPU6050 mpu6050(Wire);
Servo servoHorizontal;
Servo servoVertical;

int pinServoHorizontal = 8;
int pinServoVertical = 9;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);  // Calibración del giroscopio

  servoHorizontal.attach(pinServoHorizontal);
  servoVertical.attach(pinServoVertical);
}

void loop() {
  mpu6050.update();

  int servoHPos = map(mpu6050.getAngleX(), 90, -90, -5, 180);
  int servoVPos = map(mpu6050.getAngleY(), -90, 90, 0, 180);

  servoHorizontal.write(servoHPos);
  servoVertical.write(servoVPos);

  //delay(100);
}
