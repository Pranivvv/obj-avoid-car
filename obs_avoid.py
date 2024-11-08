#Include the library files
from machine import Pin,PWM
import utime
import time

servo = PWM(Pin(0))  #Include the servo motor pin
servo.freq(50)  #Set the frequency
trigger = Pin(16 , Pin.OUT)  #Include the Trig pin
echo = Pin(17, Pin.IN)  #Include the Echo pin

#Motor driver pins
ENA = PWM(Pin(15))
IN1 = Pin(14,Pin.OUT)
IN2 = Pin(13,Pin.OUT)
IN3 = Pin(12,Pin.OUT)
IN4 = Pin(11,Pin.OUT)
ENB = PWM(Pin(10))
ENA.freq(1000)
ENB.freq(1000)
speed = 30000  #Speed of this robot
def forward():
    ENA.duty_u16(speed)
    IN1.value(0)
    IN2.value(1)
    ENB.duty_u16(speed)
    IN3.value(1)
    IN4.value(0)
    
def backward():
    ENA.duty_u16(speed)
    IN1.value(1)
    IN2.value(0)
    ENB.duty_u16(speed)
    IN3.value(0)
    IN4.value(1)
    
def left():
    ENA.duty_u16(speed)
    IN1.value(1)
    IN2.value(0)
    ENB.duty_u16(speed)
    IN3.value(1)
    IN4.value(0)
    
def right():
    ENA.duty_u16(speed)
    IN1.value(0)
    IN2.value(1)
    ENB.duty_u16(speed)
    IN3.value(0)
    IN4.value(1)
def stop():
    ENA.duty_u16(0)
    IN1.value(0)
    IN2.value(0)
    ENB.duty_u16(0)
    IN3.value(0)
    IN4.value(0)
    
#Get the distance
def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()

    # Initialize variables with current time to avoid reference before assignment
    signaloff = utime.ticks_us()
    signalon = utime.ticks_us()

    # Timeout for echo to go high
    start_time = utime.ticks_us()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
        if utime.ticks_diff(utime.ticks_us(), start_time) > 5000:  # 5ms timeout
            return None  # Timeout occurred, no echo received

    # Timeout for echo to go low
    start_time = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
        if utime.ticks_diff(utime.ticks_us(), start_time) > 5000:  # 5ms timeout
            return None  # Timeout occurred, echo stayed high too long

    timepassed = utime.ticks_diff(signalon, signaloff)
    distance = (timepassed * 0.0343) / 2
    print("The distance from the object is", distance, "cm")
    return distance

def servoLeft():
    servo.duty_u16(7000)  #1500-8500
    
def servoRight():
    servo.duty_u16(3000)  #1500-8500
    
def servoStart():
    servo.duty_u16(5400)  #1500-8500

# while True:
#     dis = ultra()
#     if(dis<10):
#         
#     else:
        
while True:
    dis = ultra()
    if dis is None:
        print("Failed to read distance - check the sensor")
    elif dis < 10:
        stop()
        time.sleep(1) 
        servoLeft()
        time.sleep(1)
        leftDis = ultra()
        time.sleep(0.5)
        print(leftDis)
        servoStart()
        time.sleep(1)
        servoRight()
        time.sleep(1)
        rightDis = ultra()
        time.sleep(0.5)
        print(rightDis)
        servoStart()
        time.sleep(1)
        if(leftDis > rightDis): 
            print("Turn Left")
            left()            
            time.sleep(0.5)
            stop()
            time.sleep(1)
        elif(leftDis < rightDis):
            print("Turn Right")
            right()
            time.sleep(0.5)
            stop()
            time.sleep(1)
        pass
    else:
        leftDis = 0
        rightDis = 0
        forward()
        pass


