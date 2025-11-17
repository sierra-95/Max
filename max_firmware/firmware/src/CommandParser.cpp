#include "../include/CommandParser.h"

void CommandParser::readSerial() {
    while (Serial.available()) {
        char chr = Serial.read();

        // Wheel selection
        if(chr == 'r') { isRightCmd = true;  isLeftCmd = false; valueIdx = 0; }
        else if(chr == 'l') { isRightCmd = false; isLeftCmd = true; valueIdx = 0; }

        // Direction
        else if(chr == 'p') {
            if(isRightCmd) rightFwd = true;
            if(isLeftCmd)  leftFwd = true;
        }
        else if(chr == 'n') {
            if(isRightCmd) rightFwd = false;
            if(isLeftCmd)  leftFwd = false;
        }

        // Separator
        else if(chr == ',') {
            double val = atof(value);
            if(isRightCmd) rightCmdVel = val;
            if(isLeftCmd)  leftCmdVel  = val;

            // Reset value buffer
            valueIdx = 0;
            strcpy(value, "00.00");
        }

        // Value characters
        else {
            if(valueIdx < 5) value[valueIdx++] = chr;
        }
    }
}

double CommandParser::getRightCmd() const { return rightCmdVel; }
double CommandParser::getLeftCmd()  const { return leftCmdVel; }
bool CommandParser::rightForward()  const { return rightFwd; }
bool CommandParser::leftForward()   const { return leftFwd; }
