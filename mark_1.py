import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

ESC_PIN = 18
GPIO.setup(ESC_PIN, GPIO.OUT)

pwm = GPIO.PWM(ESC_PIN, 50)
pwm.start(0)

def set_speed(speed):
    duty_cycle = speed / 100 * 10 + 2
    pwm.ChangeDutyCycle(duty_cycle)

print("Starting up...")

# 캘리브레이션 과정 생략

print("Ready to fly!")

set_speed(0)  # 드론의 속도를 0으로 설정하여 정지비행 상태로 만듦

while True:
    pass  # 드론이 정지비행 상태를 유지하도록 무한 루프를 실행함
