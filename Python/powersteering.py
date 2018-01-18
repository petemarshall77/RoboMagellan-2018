from serial import Serial

# Interface to steering servo and power controller
#    Input values:
#        Steering: from -500 (full left) to +500 (full right)
#        Power:    from -500 (full reverse) to +500 (full forward)
#
#        All values are further constained to limit steering and
#        (especially) power.
STEER_MAX = 500
POWER_MAX = 150

class PowerSteering:

    def __init__(self, port_name, baud_rate, logger):
        self.logger = logger
        self.logger.write("PowerSteering: started.")
        self.serial = Serial(port_name, baud_rate)
        self.set_power_and_steering(0,0)

    def stop(self):
        self.logger.write("PowerSteering: stop")
        self.set_power_and_steering(0, 0)

    def set_power_and_steering(self, power_value, steer_value):
        self.logger.write("PowerSteering: power %d, steer %d" %
                          (power_value, steer_value))
        # Condition values past
        if steer_value > STEER_MAX:
            steer_value = STEER_MAX
        elif steer_value < -STEER_MAX:
            steer_value = -STEER_MAX
        if power_value > POWER_MAX:
            power_value = POWER_MAX
        elif power_value < -POWER_MAX:
            power_value = -POWER_MAX

        # Convert to servo values
        steer_value = 1500+steer_value
        power_value = 1500+power_value

        self.serial.write(str(int(steer_value)) + "," + str(int(power_value)))
        self.serial.write('\n')
        self.serial.flush()
