import builtins
import json
import logging
import os
import sys
import importlib.util
import importlib
from friendly_traceback.console_helpers import set_formatter
from ideas import import_hook
from ideas.examples import french

try:
    from ddebug import dd
except ImportError as e:
    exc = e


    class DD:
        def call(self, *args, **kwargs):
            raise exc

        __add__ = __enter__ = __exit__ = __call__ = __and__ = __getattr__ = __getitem__ = __setitem__ = __setattr__ = call


    dd = DD()

from . import error_hook

useful_globals = {"dd": dd, 'set_formatter': set_formatter}


def set_lang(l: str):
    """
    set hook error friendly language
    Args:
        l (str):  the language (like en,fr)- it need to be in friendly language list in url:https://friendly-traceback.github.io/docs/usage_adv.html#language-used
    """
    error_hook.lang = l


def transform_source(source: str, module=None, callback_params=None, **_kwargs):
    """
    'This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.'

    transform source from hebrew keywords to english keywords using ideas.examples.french.french_to_english.

    Args:
        source (str): source string of the file
        module (ModuleType): module of source (use for __name__)
        callback_params (dict|None): can be dict with {show_original:bool,show_transformed:bool}
        **_kwargs: more parameters I don't need for the transform

    Returns: source after transform to english keywords

    """
    if callback_params is not None:
        if callback_params["show_original"]:
            french.print_info("Original", source)
    source = french.french_to_english(source)

    if callback_params is not None:
        if callback_params["show_transformed"]:
            french.print_info("Transformed", source)

    return source


french.transform_source = transform_source
is_setup = False
hebrew_builtins = {}


def setup(with_excepthook=True):
    """
    set excepthook,load hebrew_keywords.json and hebrew_builtins.json to fr_to_py dict (keywords) and hebrew_builtins (builtins) dict
    """
    sys.excepthook = error_hook.excepthook
    cdir = os.path.dirname(__file__)
    with open(os.path.join(cdir, "hebrew_keywords.json")) as io:
        french.fr_to_py = json.load(io)
    with open(os.path.join(cdir, "hebrew_builtins.json")) as io:
        str_hebrew_builtins: dict = json.load(io)
    for k, v in str_hebrew_builtins.items():
        k: str
        v: str
        if hasattr(builtins, v):
            hebrew_builtins.update({k: getattr(builtins, v)})
        else:
            logging.warning(f"cannot find key in builtins: '{v}'")


def exec_code(code, filename, globals_: dict, module, callback_params):  # noqa
    """
    execute code with hebrew_builtins+normal_builtins

    Args:
        code (codeType): code object for exec
        filename: filename to execute
        globals_: globals values of the code
        module: module of the code
        callback_params: callback_params with show_original and show_transformed. I don't need them for this function
    """
    globals_.update(useful_globals)
    all_builtins = module.__dict__
    all_builtins.update(hebrew_builtins)

    exec(code, globals_, all_builtins)


def create_hook(run_module: bool = False, show_original: bool = False, show_transformed: bool = False,
                verbose_finder: bool = False,
                console: bool = (len(sys.argv) == 1)) -> import_hook.IdeasMetaFinder:
    """
    create import hook. start console with this hook if `console` is True and run the module `run_module` if `run_module` is True and console is False

    Args:
        run_module (bool): if sys.argv[1] is exist - run the module sys.argv[1] with the hook
        show_original (bool): show original source
        show_transformed (bool): show transformed source
        verbose_finder (bool): verbose the .hepy finder - print every search and find
        console (bool): the default value is (True if commandline argument < 0). if this True and `run_module` is True - start repl with the hook

    Returns :
        ideas.import_hook.IdeasMetaFinder: the hook

    """
    if not hebrew_builtins:
        setup()

    hook = import_hook.create_hook(
        transform_source=french.transform_source,
        callback_params={"show_original": show_original, "show_transformed": show_transformed},
        hook_name=__name__,
        extensions=[".hepy"] if not console else None,
        verbose_finder=verbose_finder,
        # source_init=lambda: '__hook__="HEPY"\n',
        exec_=exec_code
    )
    if run_module:
        # breakpoint()
        if not console:
            if os.path.splitext(sys.argv[1])[1] == ".py":
                print("note: you are run .py as main...")
                print("החלפו את הסיומת ל.hepy")
                exit(1)
            #
            module = None
            if os.path.exists(sys.argv[1]):
                module = os.path.splitext(sys.argv[1])[0]
            elif os.path.exists(sys.argv[1] + ".hepy"):
                module = sys.argv[1]
            if not module:
                print("file not found:", sys.argv[1])
                print(sys.argv[1], "הקובץ לא נמצא:")
                exit()
        else:
            from ideas import console

            def runcode(self, code):
                try:
                    exec_code(code, "<stdin>", {}, builtins, {})
                except SystemExit:
                    os._exit(1)  # noqa
                except Exception:
                    self.showtraceback()

            console.IdeasConsole.runcode = runcode
            console.start()
            return hook

        sys.path.append(os.path.dirname(module))

        # hook.find_spec = snoop.snoop(hook.find_spec)
        importlib.import_module(module)
    return hook
