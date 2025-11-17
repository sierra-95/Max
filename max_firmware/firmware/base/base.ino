#include <Servo.h>
// ------------------- Encoder pins -------------------
// Front Right
#define ENCA_FR 2   // Green
#define ENCB_FR 3   // Yellow

// Rear Left
#define ENCA_RL 18  // Green
#define ENCB_RL 19  // Yellow

// Rear Right
#define ENCA_RR 20  // Yellow
#define ENCB_RR 21  // Green


// ------------------- Motor pins -------------------
// Front Motors (Driver 1)
#define ENA_F 5
#define ENB_F 6
#define IN1_F 22
#define IN2_F 23
#define IN3_F 24
#define IN4_F 25

// Rear Motors (Driver 2)
#define ENA_R 7
#define ENB_R 8
#define IN1_R 26
#define IN2_R 27
#define IN3_R 28
#define IN4_R 29

//--------------------Tipper Setup--------------------
Servo tipper;
const int servoPin = 9;
const int stepSize = 2;
const int stepDelay = 10; 
int targetAngle = 0;
int currentAngle = 0;
unsigned long lastStepTime = 0;

// ------------------- Encoder counters -------------------
volatile long countFR = 0;
volatile long countRL = 0;
volatile long countRR = 0;

// ------------------- Timing -------------------
unsigned long lastReport = 0;
const unsigned long reportInterval = 50;

void setup() {
  // Motor pins
  pinMode(ENA_F, OUTPUT); pinMode(ENB_F, OUTPUT);
  pinMode(IN1_F, OUTPUT); pinMode(IN2_F, OUTPUT);
  pinMode(IN3_F, OUTPUT); pinMode(IN4_F, OUTPUT);
  pinMode(ENA_R, OUTPUT); pinMode(ENB_R, OUTPUT);
  pinMode(IN1_R, OUTPUT); pinMode(IN2_R, OUTPUT);
  pinMode(IN3_R, OUTPUT); pinMode(IN4_R, OUTPUT);

  // Encoder interrupts
  attachInterrupt(digitalPinToInterrupt(ENCA_FR), readEncoderFR_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_FR), readEncoderFR_B, CHANGE);

  attachInterrupt(digitalPinToInterrupt(ENCA_RL), readEncoderRL_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_RL), readEncoderRL_B, CHANGE);

  attachInterrupt(digitalPinToInterrupt(ENCA_RR), readEncoderRR_A, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_RR), readEncoderRR_B, CHANGE);

  // Servo pins
  tipper.attach(servoPin);
  tipper.write(0); 

  Serial.begin(115200);
}

// ------------------- Main loop -------------------
void loop() {
  char buffer[32];
  if (Serial.available()) {
    int len = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
    if (len > 0) {
      buffer[len] = '\0'; // null terminate

      if (strncmp(buffer, "VEL,", 4) == 0) {
        char *p = strtok(buffer + 4, ",");
        if (p) {
          float linear = atof(p);
          p = strtok(NULL, ",");
          if (p) {
            float angular = atof(p);
            setMotorPWM(linear, angular);
          }
        }
      }
      else if (strncmp(buffer, "TIP,", 4) == 0) {
        int action = atoi(buffer + 4);
        if (action == 1) targetAngle = 60;
        else if (action == 0) targetAngle = 0;
      }
    }
  }

  updateServo();
  // Report encoder counts at fixed rate
  if (millis() - lastReport >= reportInterval) {
    lastReport = millis();
    Serial.print(countRL);
    Serial.print(",");
    Serial.print(countRR);
    Serial.println();
  }
}

// ------------------- Convert cmd_vel to PWM -------------------
void setMotorPWM(float linear, float angular) {
  //wheelbase is the distance between the left and right wheel contact points
  const float WHEEL_BASE = 0.2325;
  const int MAX_PWM = 255;

  const float MAX_LINEAR  = 0.425;   // measured m/s
  const float MAX_ANGULAR = 2.99;    // measured rad/s

  // Clip incoming commands to max
  if (linear > MAX_LINEAR) linear = MAX_LINEAR;
  if (linear < -MAX_LINEAR) linear = -MAX_LINEAR;
  if (angular > MAX_ANGULAR) angular = MAX_ANGULAR;
  if (angular < -MAX_ANGULAR) angular = -MAX_ANGULAR;

  // Differential drive kinematics
  float v_left  = linear - (angular * WHEEL_BASE / 2.0);
  float v_right = linear + (angular * WHEEL_BASE / 2.0);

  // Scale to PWM
  int pwmFL = constrain(int((v_left / MAX_LINEAR) * MAX_PWM), -MAX_PWM, MAX_PWM);
  int pwmFR = constrain(int((v_right / MAX_LINEAR) * MAX_PWM), -MAX_PWM, MAX_PWM);
  int pwmRL = pwmFL;
  int pwmRR = pwmFR;

  // Deadzone
  if (abs(pwmFL) < 30) pwmFL = 0;
  if (abs(pwmFR) < 30) pwmFR = 0;
  if (abs(pwmRL) < 30) pwmRL = 0;
  if (abs(pwmRR) < 30) pwmRR = 0;

  // Front Left
  if (pwmFL >= 0) { digitalWrite(IN1_F,HIGH); digitalWrite(IN2_F,LOW); }
  else { digitalWrite(IN1_F,LOW); digitalWrite(IN2_F,HIGH); pwmFL = -pwmFL; }
  analogWrite(ENA_F, pwmFL);

  // Front Right
  if (pwmFR >= 0) { digitalWrite(IN3_F,HIGH); digitalWrite(IN4_F,LOW); }
  else { digitalWrite(IN3_F,LOW); digitalWrite(IN4_F,HIGH); pwmFR = -pwmFR; }
  analogWrite(ENB_F, pwmFR);

  // Rear Left
  if (pwmRL >= 0) { digitalWrite(IN3_R,HIGH); digitalWrite(IN4_R,LOW); }
  else { digitalWrite(IN3_R,LOW); digitalWrite(IN4_R,HIGH); pwmRL = -pwmRL; }
  analogWrite(ENA_R, pwmRL);

  // Rear Right
  if (pwmRR >= 0) { digitalWrite(IN1_R,HIGH); digitalWrite(IN2_R,LOW); }
  else { digitalWrite(IN1_R,LOW); digitalWrite(IN2_R,HIGH); pwmRR = -pwmRR; }
  analogWrite(ENB_R, pwmRR);

}

void updateServo() {
  unsigned long now = millis();
  if (now - lastStepTime >= stepDelay) {
    lastStepTime = now;

    if (currentAngle < targetAngle) {
      currentAngle += stepSize;
      if (currentAngle > targetAngle) currentAngle = targetAngle;
      tipper.write(currentAngle);
    }
    else if (currentAngle > targetAngle) {
      currentAngle -= stepSize;
      if (currentAngle < targetAngle) currentAngle = targetAngle;
      tipper.write(currentAngle);
    }
  }
}

// ------------------- Encoder ISRs -------------------
void readEncoderFR_A() { int a=digitalRead(ENCA_FR), b=digitalRead(ENCB_FR); if(a==b) countFR++; else countFR--; }
void readEncoderFR_B() { int a=digitalRead(ENCA_FR), b=digitalRead(ENCB_FR); if(a!=b) countFR++; else countFR--; }

void readEncoderRL_A() { int a=digitalRead(ENCA_RL), b=digitalRead(ENCB_RL); if(a==b) countRL++; else countRL--; }
void readEncoderRL_B() { int a=digitalRead(ENCA_RL), b=digitalRead(ENCB_RL); if(a!=b) countRL++; else countRL--; }

void readEncoderRR_A() { int a=digitalRead(ENCA_RR), b=digitalRead(ENCB_RR); if(a==b) countRR++; else countRR--; }
void readEncoderRR_B() { int a=digitalRead(ENCA_RR), b=digitalRead(ENCB_RR); if(a!=b) countRR++; else countRR--; }