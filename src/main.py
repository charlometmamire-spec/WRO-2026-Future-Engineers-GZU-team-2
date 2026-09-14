import machine
import time

# --- PIN CONFIGURATION ---
SERVO_PIN = 18       # Front steering servo
PWM_PIN = 19         # Rear motor PWM speed pin
DIR_PIN_1 = 22       # Motor direction 1
DIR_PIN_2 = 23       # Motor direction 2
TRIG_PIN = 5         # Ultrasonic trigger
ECHO_PIN = 17        # Ultrasonic echo

# --- SYSTEM CONSTANTS ---
STEER_CENTER = 90    # Straight direction angle (degrees)
STEER_MAX_LEFT = 50   # Maximum left angle
STEER_MAX_RIGHT = 130 # Maximum right angle
BASE_SPEED = 65000   # Motor speed duty cycle (0 to 65535)

# --- INITIALIZE HARDWARE ---
# Servo setup using PWM at 50Hz
servo_pwm = machine.PWM(machine.Pin(SERVO_PIN), freq=50)

# Motor setup
motor_pwm = machine.PWM(machine.Pin(PWM_PIN), freq=1000)
dir1 = machine.Pin(DIR_PIN_1, machine.Pin.OUT)
dir2 = machine.Pin(DIR_PIN_2, machine.Pin.OUT)

# Ultrasonic sensor setup
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

# AI Vision Serial Link (UART1)
uart = machine.UART(1, baudrate=9600, rx=16, tx=4)


def set_servo_angle(angle):
    """Maps 0-180 degrees to standard 50Hz servo duty cycle."""
    angle = max(STEER_MAX_LEFT, min(STEER_MAX_RIGHT, angle))
    # Standard 1ms-2ms pulse width mapping for MicroPython PWM (16-bit)
    duty = int(((angle / 180.0) * 6553 + 1638))
    servo_pwm.duty_u16(duty)


def set_drive_speed(speed, forward=True):
    """Controls the rear axle drive motor direction and speed."""
    if forward:
        dir1.value(1)
        dir2.value(0)
    else:
        dir1.value(0)
        dir2.value(1)
    motor_pwm.duty_u16(max(0, min(65535, speed)))


def adjust_steering(offset):
    """
    Maps camera offset (-100 to +100) to steering servo range.
    Offset -100 = Far Left, +100 = Far Right.
    """
    angle = int(STEER_CENTER + (offset / 100.0) * (STEER_MAX_RIGHT - STEER_CENTER))
    set_servo_angle(angle)


def read_distance_cm():
    """Reads distance from the ultrasonic sensor in cm."""
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duration = machine.time_pulse_us(echo, 1, 25000)
    if duration < 0:
        return 999  # Timeout
    return (duration * 0.0343) / 2


def execute_parallel_park():
    """Automated maneuver for parallel parking."""
    # Stop vehicle
    set_drive_speed(0)
    time.sleep(0.5)

    # Step 1: Full right turn and reverse into space
    set_servo_angle(STEER_MAX_RIGHT)
    set_drive_speed(45000, forward=False)
    time.sleep(1.2)

    # Step 2: Full left counter-steer while continuing reverse
    set_servo_angle(STEER_MAX_LEFT)
    time.sleep(1.2)

    # Step 3: Straighten wheels and hold position
    set_servo_angle(STEER_CENTER)
    set_drive_speed(0)

    while True:
        time.sleep(1)


# --- MAIN CONTROL LOOP ---
set_servo_angle(STEER_CENTER)
time.sleep(2)
set_drive_speed(BASE_SPEED, forward=True)

while True:
    # 1. Process incoming AI Vision commands over Serial
    if uart.any():
        line = uart.readline().decode('utf-8').strip()

        if line.startswith("OFFSET:"):
            try:
                offset_val = int(line.split(":")[1])
                adjust_steering(offset_val)
            except ValueError:
                pass

        elif line == "PARK_NOW":
            execute_parallel_park()

    # 2. Safety Distance Check
    dist = read_distance_cm()
    if 0 < dist < 15:
        set_drive_speed(0)
        time.sleep(0.5)

    time.sleep_ms(20)
