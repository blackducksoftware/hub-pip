import sys
import traceback

DEBUG = True


def info(message):
    print(str(message))


def error(message=None, e_message=None, print_exception=DEBUG, exit=False):
    if message:
        print("ERROR >>>>>> " + str(message))
    if e_message and print_exception:
        print(e_message)
    if exit:
        print("hub-pip failed")
        sys.exit()


def debug(message=None, exit=False):
    if DEBUG:
        if message:
            print("DEBUG >>>>>> " + str(message))
        if exit:
            print("hub-pip failed")
            sys.exit()
