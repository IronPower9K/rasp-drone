import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

ESC_PIN = 18
GPIO.setup(ESC_PIN, GPIO.OUT)

pwm = GPIO.PWM(ESC_PIN, 50)
pwm.start(0)

print("Disconnect the battery and press Enter")
input()

print("Calibrating...")
pwm.ChangeDutyCycle(2)
time.sleep(2)
pwm.ChangeDutyCycle(12)
time.sleep(2)

pwm.stop()
GPIO.cleanup()

print("Calibration complete!")
