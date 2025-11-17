#include "../include/EncoderReader.h"

EncoderReader::EncoderReader(uint8_t a, uint8_t b, float cpr, bool invert)
    : phaseA_pin(a), phaseB_pin(b), countsPerRev(cpr), pulseCount(0), direction('p'), invertDirection(invert) {}

void EncoderReader::begin() {
    pinMode(phaseB_pin, INPUT);
}

// ISR for this encoder (attach using a lambda or static wrapper)
void EncoderReader::handleISR() {
    char dir = digitalRead(phaseB_pin) ? 'p' : 'n';
    direction = invertDirection ? (dir == 'p' ? 'n' : 'p') : dir;
    pulseCount++;
}

float EncoderReader::computeVelocityRadSec(unsigned long intervalMs) {
    // Calculate rev/sec
    float revsPerSec = (pulseCount * (1000.0 / intervalMs)) / countsPerRev;
    float radPerSec = revsPerSec * 2.0 * 3.14159265;
    pulseCount = 0; // reset counter for next interval
    return radPerSec * (direction == 'p' ? 1.0 : -1.0); // apply direction
}

char EncoderReader::getDirection() const {
    return direction;
}
