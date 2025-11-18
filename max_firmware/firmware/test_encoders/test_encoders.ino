// ------------------- Encoder pins -------------------
#define ENCA_FL 18
#define ENCB_FL 19

#define ENCA_FR 20
#define ENCB_FR 21

#define ENCA_RR 2
#define ENCB_RR 3

// ------------------- Counters -------------------
volatile long countFL = 0;
volatile long countFR = 0;
volatile long countRR = 0;

void setup() {
  pinMode(ENCA_FL, INPUT);
  pinMode(ENCB_FL, INPUT);

  pinMode(ENCA_FR, INPUT);
  pinMode(ENCB_FR, INPUT);

  pinMode(ENCA_RR, INPUT);
  pinMode(ENCB_RR, INPUT);

  // Attach interrupts for FL
  attachInterrupt(digitalPinToInterrupt(ENCA_FL), readEncoderFL_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_FL), readEncoderFL_B, CHANGE);

  // Attach interrupts for FR
  attachInterrupt(digitalPinToInterrupt(ENCA_FR), readEncoderFR_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_FR), readEncoderFR_B, CHANGE);

  // Attach interrupts for RR
  attachInterrupt(digitalPinToInterrupt(ENCA_RR), readEncoderRR_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_RR), readEncoderRR_B, CHANGE);

  Serial.begin(115200);
}

void loop() {
  static long lastCountFL = 0;
  static long lastCountFR = 0;
  static long lastCountRR = 0;
  static unsigned long lastTime = 0;

  if (millis() - lastTime >= 200) {  // update every 200 ms
    unsigned long now = millis();

    long deltaFL = countFL - lastCountFL;
    long deltaFR = countFR - lastCountFR;
    long deltaRR = countRR - lastCountRR;

    String dirFL = (deltaFL > 0) ? "Forward" : (deltaFL < 0) ? "Reverse" : "Stopped";
    String dirFR = (deltaFR > 0) ? "Forward" : (deltaFR < 0) ? "Reverse" : "Stopped";
    String dirRR = (deltaRR > 0) ? "Forward" : (deltaRR < 0) ? "Reverse" : "Stopped";

    Serial.print("FL: "); Serial.print(countFL); Serial.print(" (Δ"); Serial.print(deltaFL); Serial.print(", "); Serial.print(dirFL); Serial.print(") | ");
    Serial.print("FR: "); Serial.print(countFR); Serial.print(" (Δ"); Serial.print(deltaFR); Serial.print(", "); Serial.print(dirFR); Serial.print(") | ");
    Serial.print("RR: "); Serial.print(countRR); Serial.print(" (Δ"); Serial.print(deltaRR); Serial.print(", "); Serial.print(dirRR); Serial.println(")");

    lastCountFL = countFL;
    lastCountFR = countFR;
    lastCountRR = countRR;
    lastTime = now;
  }
}

// ------------------- FL Encoder ISRs -------------------
void readEncoderFL_A() {
  int a = digitalRead(ENCA_FL);
  int b = digitalRead(ENCB_FL);
  if (a == b) countFL++;
  else countFL--;
}

void readEncoderFL_B() {
  int a = digitalRead(ENCA_FL);
  int b = digitalRead(ENCB_FL);
  if (a != b) countFL++;
  else countFL--;
}

// ------------------- FR Encoder ISRs -------------------
void readEncoderFR_A() {
  int a = digitalRead(ENCA_FR);
  int b = digitalRead(ENCB_FR);
  if (a == b) countFR++;
  else countFR--;
}

void readEncoderFR_B() {
  int a = digitalRead(ENCA_FR);
  int b = digitalRead(ENCB_FR);
  if (a != b) countFR++;
  else countFR--;
}

// ------------------- RR Encoder ISRs -------------------
void readEncoderRR_A() {
  int a = digitalRead(ENCA_RR);
  int b = digitalRead(ENCB_RR);
  if (a == b) countRR++;
  else countRR--;
}

void readEncoderRR_B() {
  int a = digitalRead(ENCA_RR);
  int b = digitalRead(ENCB_RR);
  if (a != b) countRR++;
  else countRR--;
}
