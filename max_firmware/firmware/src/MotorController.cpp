#include "../include/MotorController.h"

MotorController::MotorController(uint8_t en, uint8_t in1, uint8_t in2)
: enPin(en), in1Pin(in1), in2Pin(in2) {}

void MotorController::begin() {
    pinMode(enPin, OUTPUT);
    pinMode(in1Pin, OUTPUT);
    pinMode(in2Pin, OUTPUT);
    setDirection(true);
}

void MotorController::setDirection(bool forward) {
    isForward = forward;
    digitalWrite(in1Pin, forward ? HIGH : LOW);
    digitalWrite(in2Pin, forward ? LOW : HIGH);
}

void MotorController::setSpeed(double pwmValue) {
    analogWrite(enPin, constrain(pwmValue, 0, 255));
}

bool MotorController::getDirection() {
    return isForward;
}
