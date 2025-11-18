// ------------------- Encoder pins -------------------
#define ENCA_RL 18
#define ENCB_RL 19

#define ENCA_RR 20
#define ENCB_RR 21

// ------------------- Counters -------------------
volatile long countRL = 0;
volatile long countRR = 0;

void setup() {
  pinMode(ENCA_RL, INPUT);
  pinMode(ENCB_RL, INPUT);

  pinMode(ENCA_RR, INPUT);
  pinMode(ENCB_RR, INPUT);

  // Attach interrupts for RL
  attachInterrupt(digitalPinToInterrupt(ENCA_RL), readEncoderRL_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_RL), readEncoderRL_B, CHANGE);

  // Attach interrupts for RR
  attachInterrupt(digitalPinToInterrupt(ENCA_RR), readEncoderRR_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_RR), readEncoderRR_B, CHANGE);

  Serial.begin(115200);
}

void loop() {
  static long lastCountRL = 0;
  static long lastCountRR = 0;
  static unsigned long lastTime = 0;

  if (millis() - lastTime >= 200) {  // update every 200 ms
    unsigned long now = millis();

    long deltaRL = countRL - lastCountRL;
    long deltaRR = countRR - lastCountRR;

    String dirRL = (deltaRL > 0) ? "Forward" : (deltaRL < 0) ? "Reverse" : "Stopped";
    String dirRR = (deltaRR > 0) ? "Forward" : (deltaRR < 0) ? "Reverse" : "Stopped";

    Serial.print("RL: "); 
    Serial.print(countRL); 
    Serial.print(" (Δ"); 
    Serial.print(deltaRL); 
    Serial.print(", "); 
    Serial.print(dirRL); 
    Serial.print(") | ");

    Serial.print("RR: "); 
    Serial.print(countRR); 
    Serial.print(" (Δ"); 
    Serial.print(deltaRR); 
    Serial.print(", "); 
    Serial.print(dirRR); 
    Serial.println(")");

    lastCountRL = countRL;
    lastCountRR = countRR;
    lastTime = now;
  }
}

// ------------------- RL Encoder ISRs -------------------
void readEncoderRL_A() {
  int a = digitalRead(ENCA_RL);
  int b = digitalRead(ENCB_RL);
  if (a == b) countRL++;
  else countRL--;
}

void readEncoderRL_B() {
  int a = digitalRead(ENCA_RL);
  int b = digitalRead(ENCB_RL);
  if (a != b) countRL++;
  else countRL--;
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
