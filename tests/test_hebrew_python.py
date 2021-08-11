import builtins
import sys
import unittest

import hebrew_python.hook as hepy
from io import StringIO
from contextlib import contextmanager


@contextmanager
def Output():
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    with StringIO() as stdout, StringIO() as stderr:
        sys.stdout = stdout
        sys.stderr = stderr
        try:
            yield stdout, stderr
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class TestHebrewPython(unittest.TestCase):
    def setUp(self):
        hepy.setup()
        self.assertIn("הראה", hepy.hebrew_builtins)

    def test_keywords_transform(self):
        hook = hepy.create_hook()
        s = "אמת וגם שקר"
        en = hook.transform_source(s)
        self.assertEqual(en, "True and False")

    def test_builtins(self):
        self.assertIn("הראה", hepy.hebrew_builtins)
        with Output() as (std,_):
            hepy.exec_code("הראה('OK')", '<test>', {}, builtins, {})
            self.assertEqual(std.getvalue(),"OK\n")

    def test_errors(self):
        try:
            1 / 0
        except ZeroDivisionError:
            with Output() as (stdout, stderr):
                hepy.error_hook.excepthook(*sys.exc_info())
                value = stdout.getvalue()
                # stdout
                self.assertIn("ידידותי", value)
                # stderr
                value = stderr.getvalue()
                self.assertIn("Traceback", value)
                self.assertIn("Traceback", value)
                self.assertIn("ZeroDivisionError", value)

    def test_basic_file(self):
        # sys.argv = [sys.argv[0], "basic_file.hepy", sys.argv[1:]]
        hepy.create_hook(False, console=False)
        from . import basic_file
        n = basic_file.main()
        heb_min = basic_file.מינימום
        heb_max = basic_file.מקסימום
        self.assertIn(n, range(heb_min, heb_max + 1))

    def test_import_file(self):
        hepy.create_hook(False, console=False)
        from . import import_file
        self.assertTrue(import_file.בודק())


if __name__ == '__main__':
    unittest.main()
