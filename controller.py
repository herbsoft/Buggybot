# Code for Team Diddybot PiWars 2019 robot aka Buggybot
#
# ------------------------------------------------------------------------------

from approxeng.input.selectbinder import ControllerResource
from time import sleep

# ------------------------------------------------------------------------------


try:
    import piconzero as pz

    def set_speeds(power_left, power_right):

        motor_left = 0  # Motor A
        motor_right = 1  # Motor B

        pz.setMotor(motor_left, power_left)
        pz.setMotor(motor_right, power_right)

        # print('Left: {}, Right {}'.format(power_left, power_right))

        # The sleep here is needed otherwise the controller goes a bit out of control
        sleep(0.1)

    def stop_motors():
        pz.stop()

except ImportError:

    print('Piconzero not found, using dummy functions.')

    def set_speeds(power_left, power_right):
        print('DEBUG Left: {}, Right: {}'.format(power_left, power_right))
        sleep(0.3)


    def stop_motors():
        print('DEBUG Motors stopping')


# ------------------------------------------------------------------------------


class RobotStopException(Exception):
    pass


# ------------------------------------------------------------------------------


def mixer(yaw, throttle, max_power=100):
    """
    Mix a pair of joystick axes, returning a pair of wheel speeds. This is where the mapping from
    joystick positions to wheel powers is defined, so any changes to how the robot drives should
    be made here, everything else is really just plumbing.

    :param yaw:
        Yaw axis value, ranges from -1.0 to 1.0
    :param throttle:
        Throttle axis value, ranges from -1.0 to 1.0
    :param max_power:
        Maximum speed that should be returned from the mixer, defaults to 100
    :return:
        A pair of power_left, power_right integer values to send to the motor driver
    """
    left = throttle + yaw
    right = throttle - yaw
    scale = float(max_power) / max(1, abs(left), abs(right))
    return int(left * scale), int(right * scale)


# ------------------------------------------------------------------------------


try:
    while True:
        # Inner try / except is used to wait for a controller to become available, at which point we
        # bind to it and enter a loop where we read axis values and send commands to the motors.
        try:
            # Bind to any available joystick, this will use whatever's connected as long as the library
            # supports it.
            with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
                print('Controller found, press HOME button to exit, use left stick to drive.')
                print(joystick.controls)
                # Loop until the joystick disconnects, or we deliberately stop by raising a
                # RobotStopException
                while joystick.connected:
                    # Get joystick values from the left analogue stick
                    x_axis, y_axis = joystick['lx', 'ly']
                    # Get power from mixer function
                    power_left, power_right = mixer(yaw=x_axis, throttle=y_axis)
                    # Set motor speeds
                    set_speeds(power_left, power_right)
                    # Get a ButtonPresses object containing everything that was pressed since the last
                    # time around this loop.
                    joystick.check_presses()
                    # Print out any buttons that were pressed, if we had any
                    if joystick.has_presses:
                        print(joystick.presses)
                    # If home was pressed, raise a RobotStopException to bail out of the loop
                    # Home is generally the PS button for playstation controllers, XBox for XBox etc
                    if 'home' in joystick.presses:
                        raise RobotStopException()
        except IOError:
            # We get an IOError when using the ControllerResource if we don't have a controller yet,
            # so in this case we just wait a second and try again after printing a message.
            print('No controller found yet')
            sleep(1)

except RobotStopException:
    # This exception will be raised when the home button is pressed, at which point we should
    # stop the motors.
    stop_motors()
