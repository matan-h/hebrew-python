import copy
import sys
from typing import Optional

from . import hook

from functools import partial


class HebrewIPython:
    def __init__(self, shell):
        """
        IPython extension for write IPython (or jupyter) scripts in hebrew

        Args:
            shell (InteractiveShell): current IPython shell
        """
        from IPython import InteractiveShell
        # set_formatter('jupyter')
        hook.error_hook.jupyter = True

        self.ip: InteractiveShell = shell
        # old values
        self.old_showtraceback = self.ip.showtraceback
        self.old_auto_builtins = copy.copy(self.ip.builtin_trap.auto_builtins)

        hook.setup(with_excepthook=False)
        hook.error_hook.use_rich = self.isnotebook()
        hook.create_hook(False, console=False)

    def isnotebook(self):  # credit https://stackoverflow.com/a/39662359/12269724
        try:
            shell = self.ip.__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True  # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False  # Probably standard Python interpreter

    @staticmethod
    def hebrew2py(lines: str) -> list:
        """
        convert HebrewPython keywords to normal Python keywords.

        show the original and transformed if the first line start with "# HEPY:SHOW".

        Args:
            lines: list of lines with HebrewPython keywords

        Returns:
            list:list of lines with normal python keywords

        """
        callback_params = None
        hepy_sow = False
        if lines:
            if lines[0].upper().startswith("# HEPY:SHOW"):
                hepy_sow = True
        lines = list(map(partial(hook.transform_source), lines))
        if hepy_sow:
            hook.french.print_info("Transformed", ''.join(lines))
        # return hook.transform_source('\n'.join(lines), callback_params=callback_params).split("\n")
        return lines

    def showtraceback(self, exc_tuple: Optional[tuple] = None, show_traceback=True, *args, **kwargs):  # noqa

        """
        show the traceback on normal error

        Args:
            exc_tuple (tuple or None): (exc_type,exc_value,tb) like sys.excepthook or None for auto detect
        """
        try:
            etype, value, tb = self.ip._get_exc_info(exc_tuple)  # noqa
        except ValueError:
            print('No traceback available to show.', file=sys.stderr)
            return
        hook.error_hook.excepthook(etype, value, tb, show_traceback=show_traceback)

    def load(self):
        """
        load the HebrewIPython extension by update IPython shell functions and objects
        """
        # functions to replace:
        self.ip.showtraceback = self.showtraceback
        # self.ip.showsyntaxerror = lambda *a, **k: self.showtraceback(self.ip._get_exc_info(),show_traceback = False)

        # objects to modify:
        # self._old(self.ip.input_transformers_cleanup)
        self.ip.input_transformers_cleanup.append(self.hebrew2py)
        # self._old(self.ip.user_global_ns)
        self.ip.user_global_ns.update(hook.useful_globals)
        #
        self.ip.builtin_trap.auto_builtins.update(hook.hebrew_builtins)

    def unload(self):
        self.ip.showtraceback = self.old_showtraceback
        if self.hebrew2py in self.ip.input_transformers_cleanup:
            self.ip.input_transformers_cleanup.remove(self.hebrew2py)
        for k in hook.useful_globals.keys():
            self.ip.user_global_ns.pop(k, None)
        self.ip.builtin_trap.auto_builtins = self.old_auto_builtins


hepy_s = []


def load_ipython_extension(shell):
    """
    the function ipython call on `%load_ext hebrew_python`.

    init HebrewIPython class and load the HebrewIPython extension with HebrewIPython.load

    Args:
        shell (InteractiveShell): ipython shell
    """
    hepy = HebrewIPython(shell)
    hepy.load()
    hepy_s.append(hepy)


def unload_ipython_extension(shell):
    """
    the function ipython call on `%unload_ext hebrew_python`.

    unload the HebrewIPython extension by HebrewIPython.unload

    Args:
         shell (InteractiveShell): ipython shell

    """
    for hepy in hepy_s:
        hepy.unload()
