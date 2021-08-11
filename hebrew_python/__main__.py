import sys

from .hook import create_hook

show_transformed = show_original = verbose_finder = False
if "-t" in sys.argv:
    show_transformed = True
if "-o" in sys.argv:
    show_original = True
if "-v" in sys.argv:
    verbose_finder = True


def main():
    create_hook(True, show_original=show_original, show_transformed=show_transformed, verbose_finder=verbose_finder)


if __name__ == '__main__':
    main()
