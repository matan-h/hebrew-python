import atexit
import contextlib
import unittest

from IPython.testing import globalipapp
from IPython.utils.io import capture_output

extension_name = "hebrew_python"


def start_ipython():
    session_ip = globalipapp.start_ipython()
    print(session_ip)
    session_ip.run_line_magic(magic_name='load_ext', line=extension_name)
    return session_ip


ip = start_ipython()


def close_ipython():
    ip.run_line_magic(magic_name='unload_ext', line=extension_name)
    ip.run_line_magic(magic_name='reset', line='-f')


class TestHebrewPython(unittest.TestCase):
    def test_keywords(self):
        # cell = "# HEPY:SHOW\n"
        cell = 'out=(אמת אם אמת אחרת שקר)'
        ip.run_cell(cell)
        self.assertEqual(ip.user_global_ns["out"], True)

    def test_builtins(self):
        cell = 'out = אמת אם אורך(רשימה())==0 אחרת שקר'
        ip.run_cell(cell)
        self.assertEqual(ip.user_global_ns["out"], True)

    def test_basic_file(self):
        cell = """
יבא basic_file

מספר = basic_file.main()
מינימום = basic_file.מינימום
מקסימום = basic_file.מקסימום
        """
        ip.run_cell(cell)
        self.assertIn(ip.user_global_ns["מספר"], range(ip.user_global_ns["מינימום"], ip.user_global_ns["מקסימום"] + 1))

    def test_import_file(self):
        cell = """
        יבא import_file
        tester = import_file.בודק
        """
        ip.run_cell(cell)
        ip.user_global_ns["tester"]()



if __name__ == '__main__':
    unittest.main()
    close_ipython()
