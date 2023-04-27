import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
ESC_GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_GPIO_PIN, GPIO.OUT)

# PWM 주파수 설정
ESC_FREQ = 50
pwm = GPIO.PWM(ESC_GPIO_PIN, ESC_FREQ)

# ESC 최소/최대값 설정
ESC_MIN_VALUE = 1000
ESC_MAX_VALUE = 2000

# 모터 속도 설정
motor_speed = 1500  # 모터 속도가 1500일 때 중립값

# ESC 초기화 함수
def init_esc():
    pwm.start(0)
    time.sleep(1)
    set_speed(ESC_MIN_VALUE)
    time.sleep(1)

# 모터 속도 설정 함수
def set_speed(speed):
    duty = speed / 100.0
    pwm.ChangeDutyCycle(duty)

# 모터 시작 함수
def start_motor():
    set_speed(motor_speed)

# 모터 정지 함수
def stop_motor():
    set_speed(ESC_MIN_VALUE)
    time.sleep(1)
    pwm.stop()

# ESC 종료 함수
def cleanup():
    GPIO.cleanup()

# ESC 초기화
init_esc()

# 모터 시작
start_motor()

# 5초간 모터 구동 후 정지
time.sleep(5)
stop_motor()

# 종료 처리
cleanup()
