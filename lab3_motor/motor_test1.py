from utils.brick import Motor
import time
motor = Motor("A")

motor.reset_encoder()
motor.set_limits(power=50, dps=90)



while True:
    try:
        
        
        motor.set_position_relative(45)
        motor.set_position_relative(-45)
        
    except KeyboardInterrupt:
        
        break
