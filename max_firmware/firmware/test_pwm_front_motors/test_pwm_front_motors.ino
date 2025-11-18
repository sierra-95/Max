// ----- Pin Definitions -----
#define ENA 5   // Front Left Enable (PWM)
#define ENB 6   // Front Right Enable (PWM)
#define IN1 22  // FL IN1
#define IN2 23  // FL IN2
#define IN3 24  // FR IN3
#define IN4 25  // FR IN4

// Rear motors (wired but not used)
#define ENA_R 7
#define ENB_R 8
#define IN1_R 26
#define IN2_R 27
#define IN3_R 28
#define IN4_R 29

void setup() {
  // Front motor pins
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Rear motor pins (unused for now)
  pinMode(ENA_R, OUTPUT);
  pinMode(ENB_R, OUTPUT);
  pinMode(IN1_R, OUTPUT);
  pinMode(IN2_R, OUTPUT);
  pinMode(IN3_R, OUTPUT);
  pinMode(IN4_R, OUTPUT);

  // Ensure all motors are stopped initially
  stopMotors();
}

void loop() {
  // ----- Forward -----
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 200); // PWM speed (0-255)
  analogWrite(ENB, 200);

  delay(5000);  // run 5 seconds

  stopMotors();
  delay(1000);

  // ----- Reverse -----
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  analogWrite(ENA, 200);
  analogWrite(ENB, 200);

  delay(5000);

  stopMotors();
  delay(2000);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
