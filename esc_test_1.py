import RPi.GPIO as GPIO
import time

# GPIO �� ����
ESC_GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_GPIO_PIN, GPIO.OUT)

# PWM ���ļ� ����
ESC_FREQ = 50
pwm = GPIO.PWM(ESC_GPIO_PIN, ESC_FREQ)

# ESC �ּ�/�ִ밪 ����
ESC_MIN_VALUE = 1000
ESC_MAX_VALUE = 2000

# ���� �ӵ� ����
motor_speed = 1500  # ���� �ӵ��� 1500�� �� �߸���

# ESC �ʱ�ȭ �Լ�
def init_esc():
    pwm.start(0)
    time.sleep(1)
    set_speed(ESC_MIN_VALUE)
    time.sleep(1)

# ���� �ӵ� ���� �Լ�
def set_speed(speed):
    duty = speed / 100.0
    pwm.ChangeDutyCycle(duty)

# ���� ���� �Լ�
def start_motor():
    set_speed(motor_speed)

# ���� ���� �Լ�
def stop_motor():
    set_speed(ESC_MIN_VALUE)
    time.sleep(1)
    pwm.stop()

# ESC ���� �Լ�
def cleanup():
    GPIO.cleanup()

# ESC �ʱ�ȭ
init_esc()

# ���� ����
start_motor()

# 5�ʰ� ���� ���� �� ����
time.sleep(5)
stop_motor()

# ���� ó��
cleanup()
