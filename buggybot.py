# ------------------------------------------------------------------------------
# Code for Team Diddybot PiWars 2019 robot aka Buggybot
#
# ------------------------------------------------------------------------------


from approxeng.input.selectbinder import ControllerResource
from time import sleep


# ------------------------------------------------------------------------------


class RobotStopException(Exception):
    pass


# ------------------------------------------------------------------------------


def manual():
    print('Manual driving')


# ------------------------------------------------------------------------------


def straight_line():
    print('Straight line speed test')


# ------------------------------------------------------------------------------
# This is the main menu selection code

switcher = {
    1: manual,
    2: straight_line
}


def run_mode(argument):
    func = switcher.get(argument, lambda: "Invalid month")
    # Execute the function
    return func()


class MenuExitException(Exception):
    pass


try:
    while True:
        # Inner try / except is used to wait for a controller to become available, at which point we
        # bind to it and enter a loop where we read axis values and drive menu.
        try:
            mode = 1

            # Bind to any available joystick, this will use whatever's connected as long as the library
            # supports it.
            with ControllerResource(dead_zone=0.05, hot_zone=0.05) as joystick:
                print('Controller found, press HOME button to exit, X to select mode')
                print(joystick.controls)

                # Loop until the joystick disconnects, or we deliberately stop by raising a
                # RobotStopException
                while joystick.connected:
                    joystick.check_presses()

                    # Print out any buttons that were pressed, if we had any
                    if joystick.has_presses:
                        print(joystick.presses)

                        if 'home' in joystick.presses:
                            # If home was pressed, raise a RobotStopException to bail out of the loop
                            # Home is generally the PS button for playstation controllers, XBox for XBox etc
                            raise MenuExitException()

                        elif 'dleft' in joystick.presses:
                            mode -= 1
                            if mode < 1:
                                mode = len(switcher)

                        elif 'dright' in joystick.presses:
                            mode += 1
                            if mode > len(switcher):
                                mode = 1

                        elif 'cross' in joystick.presses:
                            print('Selected mode {}'.format(mode))
                            run_mode(mode)

                    sleep(0.1)

        except IOError:
            # We get an IOError when using the ControllerResource if we don't have a controller yet,
            # so in this case we just wait a second and try again after printing a message.
            print('No controller found yet')
            sleep(1)

except RobotStopException:
    # This exception will be raised when the home button is pressed, at which point we should
    # stop the motors.
    print('Shutting down')
