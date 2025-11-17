#ifndef COMMAND_PARSER_H
#define COMMAND_PARSER_H

#include <Arduino.h>

class CommandParser {
public:
    void readSerial();
    double getRightCmd() const;
    double getLeftCmd() const;
    bool rightForward() const;
    bool leftForward() const;

private:
    double rightCmdVel = 0.0;
    double leftCmdVel  = 0.0;
    bool rightFwd = true;
    bool leftFwd = true;

    char value[6] = "00.00";
    uint8_t valueIdx = 0;
    bool isRightCmd = false;
    bool isLeftCmd  = false;
};

#endif
