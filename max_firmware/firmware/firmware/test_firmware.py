import serial
import threading
import time

PORT = "/dev/ttyACM0"
BAUD = 115200

lock = threading.Lock()
running = True

def serial_reader(ser):
    """Background thread to continuously read serial feedback."""
    global running
    while running:
        with lock:
            if ser.in_waiting > 0:
                line = ser.readline().decode(errors="ignore").strip()
                if line:
                    print("Feedback:", line)
        time.sleep(0.01)


def send_cmd(ser, r_sign, r_val, l_sign, l_val):
    """Thread-safe command writer."""
    cmd = f"r{r_sign}{r_val:.2f},l{l_sign}{l_val:.2f},"
    with lock:
        ser.write(cmd.encode())


def main():
    global running

    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    time.sleep(2)  # Allow Arduino reset

    # Start feedback thread
    thread = threading.Thread(target=serial_reader, args=(ser,), daemon=True)
    thread.start()

    # ----------- Forward 5s -----------
    send_cmd(ser, "p", 10.00, "p", 10.00)
    time.sleep(5)

    # ----------- Stop 2s -----------
    send_cmd(ser, "p", 0.00, "p", 0.00)
    time.sleep(2)

    # ----------- Reverse 5s -----------
    send_cmd(ser, "n", 10.00, "n", 10.00)
    time.sleep(5)

    # ----------- Final Stop -----------
    send_cmd(ser, "p", 0.00, "p", 0.00)

    # Cleanup
    running = False
    thread.join(timeout=1)
    ser.close()


if __name__ == "__main__":
    main()
