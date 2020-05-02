import RPi.GPIO as GPIO
import time
import pyspeedtest

#setup
st = pyspeedtest.SpeedTest()
motor_speed=0.001#lower is slower. 0.001 seems to be as fast as my stepper will go.

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)

def halt_motor():
  for pin in range(4):
    GPIO.output(control_pins[pin], 0)
  print("Motor stopped")
  
def move_motor(steps):
  if steps<0:
    steps=abs(steps)
    for i in range(int(round(steps))):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq_back[halfstep][pin])
        time.sleep(motor_speed)
  else:
    for i in range(int(round(steps))):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(motor_speed)



control_pins = [7,11,13,15]
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

halfstep_seq_back = [
  [1,0,0,1],
  [0,0,0,1],
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0]
]

#Homing
while GPIO.input(12):
  move_motor(-1)
  
move_motor(256)
move_motor(-253)
halt_motor()
current_position=0
print("HOMING COMPLETED")

#Main program
while True:
  speed = st.download()/1000000
  print(str(speed)+"Mb/s")
  speed_to_steps=speed*2.56#256 max steps, 1000mb/s max network speed
 
  if speed_to_steps>256:
    speed_to_steps=256
    
  if speed_to_steps<2:
    speed_to_steps=2
   
  move_motor(speed_to_steps-current_position)
  halt_motor()
  current_position=speed_to_steps

  time.sleep(10)#10 seconds between speedchecks
