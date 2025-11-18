import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

def send_cmd(right_sign, right_val, left_sign, left_val):
    cmd = f"r{right_sign}{right_val:.2f},l{left_sign}{left_val:.2f},"
    ser.write(cmd.encode())
    print("Sent:", cmd)

# ---- Move forward for 5 seconds ----
send_cmd("p", 10.00, "p", 10.00)
time.sleep(5)

# ---- Safety stop ----
send_cmd("p", 0.00, "p", 0.00)
time.sleep(2)

# ---- Move backward for 5 seconds ----
send_cmd("n", 10.00, "n", 10.00)
time.sleep(5)

# ---- Safety stop ----
send_cmd("p", 0.00, "p", 0.00)

ser.close()
