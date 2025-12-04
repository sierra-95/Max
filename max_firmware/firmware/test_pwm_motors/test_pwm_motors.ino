// ----- Pin Definitions -----
#define ENA 5   //ENA
#define ENB 6   // ENB
#define IN1 22  // IN1
#define IN2 23  // IN2
#define IN3 24  // IN3
#define IN4 25  // IN4


void setup() {
  // Front motor pins
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Ensure all motors are stopped initially
  stopMotors();
}

void loop() {
  // ----- Forward -----
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 200);
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
