#ifndef MOTOR_CONTROLLER_H
#define MOTOR_CONTROLLER_H

#include <Arduino.h>

class MotorController {
public:
    MotorController(uint8_t enPin, uint8_t in1Pin, uint8_t in2Pin);

    void begin();
    void setDirection(bool forward);
    void setSpeed(double pwmValue);  // expects 0–255
    bool getDirection();

private:
    uint8_t enPin, in1Pin, in2Pin;
    bool isForward = true;
};

#endif
