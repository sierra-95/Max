// ----- Pin Definitions -----
#define ENA_R 7   // Rear Left Enable (PWM)
#define ENB_R 8   // Rear Right Enable (PWM)
#define IN1_R 26  // RL IN1
#define IN2_R 27  // RL IN2
#define IN3_R 28  // RR IN3
#define IN4_R 29  // RR IN4

void setup() {
  // Rear motor pins
  pinMode(ENA_R, OUTPUT);
  pinMode(ENB_R, OUTPUT);
  pinMode(IN1_R, OUTPUT);
  pinMode(IN2_R, OUTPUT);
  pinMode(IN3_R, OUTPUT);
  pinMode(IN4_R, OUTPUT);

  // Ensure motors are stopped initially
  stopMotorsRear();
}

void loop() {
  // ----- Forward -----
  digitalWrite(IN1_R, HIGH);
  digitalWrite(IN2_R, LOW);
  digitalWrite(IN3_R, HIGH);
  digitalWrite(IN4_R, LOW);

  analogWrite(ENA_R, 200); // PWM speed (0-255)
  analogWrite(ENB_R, 200);

  delay(5000);  // run 5 seconds

  stopMotorsRear();
  delay(1000);

  // ----- Reverse -----
  digitalWrite(IN1_R, LOW);
  digitalWrite(IN2_R, HIGH);
  digitalWrite(IN3_R, LOW);
  digitalWrite(IN4_R, HIGH);

  analogWrite(ENA_R, 200);
  analogWrite(ENB_R, 200);

  delay(5000);

  stopMotorsRear();
  delay(2000);
}

void stopMotorsRear() {
  analogWrite(ENA_R, 0);
  analogWrite(ENB_R, 0);
  digitalWrite(IN1_R, LOW);
  digitalWrite(IN2_R, LOW);
  digitalWrite(IN3_R, LOW);
  digitalWrite(IN4_R, LOW);
}
