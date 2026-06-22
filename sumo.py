from zumo_2040_robot import robot
import time

# Motor Constants
MAX_SPEED = const(6000)

# Sensor Constants
SENSOR_THRESHOLD = const(1)
LINE_THRESHOLD = const(700)

# global variables
opponent_found = False

motors = robot.Motors()
proximity_sensors = robot.ProximitySensors()
line_sensors = robot.LineSensors()

def turn_left(speed):
    motors.set_speeds(speed, -speed)

def turn_right(speed):
    motors.set_speeds(-speed, speed)

def turn(speed, dir):
    motors.set_speeds(-speed, speed) if dir else motors.set_speeds(speed, -speed)

def forward(speed):
    motors.set_speeds(speed, speed)

def reverse(speed):
    motors.set_speeds(-speed, -speed)

def stop():
    motors.set_speeds(0, 0)

def find_opponent_tick(turn_speed, turn_dir):
    # Try putting this on other thread and be interrupted by line tracking
    TURN_SPEED_MIN = 1500
    # FRONT_DECELERATION, SIDE_DECELERATION = 100, 200
    ACCELERATION_DELTA =  150
    # Read the proximity sensors.
    proximity_sensors.read()
    reading_left = proximity_sensors.left_counts_with_left_leds()
    reading_front_left = proximity_sensors.front_counts_with_left_leds()
    reading_front_right = proximity_sensors.front_counts_with_right_leds()
    reading_right = proximity_sensors.right_counts_with_right_leds()

    if not any(reading > SENSOR_THRESHOLD for reading in \
        (reading_left, reading_front_left, reading_front_right, reading_right)):
        # Object not seen
        turn_speed += ACCELERATION_DELTA
        turn(turn_speed, turn_dir)
        return turn_speed, turn_dir, False
        

    left = max(reading_front_left, reading_left)
    right = max(reading_front_right, reading_right)
    turn_speed -= ACCELERATION_DELTA

    if left > right:
        # turn left
        turn_dir = -1
        turn_left(turn_speed)
        return turn_speed, turn_dir, False
    elif right > left:
        # turn right
        turn_dir = 0
        turn_left(turn_speed)
        return turn_speed, turn_dir, False
    else:
        # opponent found
        forward(MAX_SPEED)
        return  MAX_SPEED, turn_dir, True
    

def avoid_line():
    line = line_sensors.read_calibrated()[:]
    line_sensors.start_read()

    if line[1] < LINE_THRESHOLD and line[2] < LINE_THRESHOLD and line[3] < LINE_THRESHOLD:
        turn_left(MAX_SPEED)
        time.sleep_ms(40)
        pass
    elif line[0] < LINE_THRESHOLD:
        # turn 120 deg right
        turn_right(MAX_SPEED)
        time.sleep_ms(25)
    elif line[4] < LINE_THRESHOLD:
        # turn 120 deg left
        turn_left(MAX_SPEED)
        time.sleep_ms(25)

def main_loop():
    turn_speed = MAX_SPEED
    turn_dir = 1
    while True:
        turn_speed, turn_dir, obj_found = find_opponent_tick(turn_speed, turn_dir)
        avoid_line()

if __name__ == "__main__":
    main_loop()


