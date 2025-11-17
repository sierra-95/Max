#ifndef ENCODER_READER_H
#define ENCODER_READER_H

#include <Arduino.h>

class EncoderReader {
public:
    EncoderReader(uint8_t phaseA, uint8_t phaseB, float cpr, bool invert = false);

    void begin();
    float computeVelocityRadSec(unsigned long intervalMs);
    char getDirection() const;

    void handleISR(); // called from ISR

private:
    uint8_t phaseA_pin, phaseB_pin;
    float countsPerRev;
    volatile uint32_t pulseCount;
    volatile char direction; // 'p' or 'n'
    bool invertDirection;
};

#endif
