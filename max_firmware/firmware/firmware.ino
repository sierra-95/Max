#include <PID_v1.h>
#include "include/MotorController.h"
#include "include/EncoderReader.h"
#include "include/CommandParser.h"

MotorController rightMotorCtrl(9, 12, 13);
MotorController leftMotorCtrl(11, 7, 8);
EncoderReader encoderRight(3, 5, 385.0);
EncoderReader encoderLeft(2, 4, 385.0, true);
CommandParser parser;

// PID variables…
double rightMeas = 0, leftMeas = 0;
double rightSet = 0, leftSet = 0;
double rightPWM = 0, leftPWM = 0;

// PID objects
PID rightPID(&rightMeas, &rightPWM, &rightSet, 11.5, 7.5, 0.1, DIRECT);
PID leftPID(&leftMeas, &leftPWM, &leftSet, 12.8, 8.3, 0.1, DIRECT);

unsigned long lastSample = 0;
const unsigned long period = 100;

void setup() {
  Serial.begin(115200);

  rightMotorCtrl.begin();
  leftMotorCtrl.begin();
  encoderRight.begin();
  encoderLeft.begin();

  attachInterrupt(digitalPinToInterrupt(3), [](){ encoderRight.handleISR(); }, RISING);
  attachInterrupt(digitalPinToInterrupt(2), [](){ encoderLeft.handleISR(); }, RISING);

  rightPID.SetOutputLimits(0,255);
  leftPID.SetOutputLimits(0,255);
  rightPID.SetMode(AUTOMATIC);
  leftPID.SetMode(AUTOMATIC);
}

void loop() {
  parser.readSerial();

  rightSet = parser.getRightCmd();
  leftSet  = parser.getLeftCmd();

  unsigned long now = millis();
  if(now - lastSample >= period) {
    rightMeas = encoderRight.computeVelocityRadSec(period);
    leftMeas  = encoderLeft.computeVelocityRadSec(period);

    rightPID.Compute();
    leftPID.Compute();

    rightMotorCtrl.setDirection(parser.rightForward());
    leftMotorCtrl.setDirection(parser.leftForward());

    rightMotorCtrl.setSpeed(rightPWM);
    leftMotorCtrl.setSpeed(leftPWM);

    String feedback = "r";
    feedback += encoderRight.getDirection();    // 'p' or 'n'
    feedback += String(rightMeas, 2);          // measured velocity
    feedback += ",l";
    feedback += encoderLeft.getDirection();     // 'p' or 'n'
    feedback += String(leftMeas, 2);
    feedback += ",";
    Serial.println(feedback);

    lastSample = now;
  }
}
