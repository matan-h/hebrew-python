from sys import exc_info
from . import error_hook


def הראה_שגיאה():
    if all(exc_info()):  # if there is exc info
        error_hook.excepthook(*exc_info())


def main():
    a = ''
    try:
        1 / 0
    except ZeroDivisionError:
        הראה_שגיאה()
        print("DONE")


if __name__ == '__main__':
    main()
