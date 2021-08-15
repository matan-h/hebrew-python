import friendly_traceback.core
import rich.panel
import rich.traceback
import rich.markdown
import sys
import inspect

friendly_traceback.debug_helper.DEBUG = True
old_log = friendly_traceback.debug_helper.log_error


def getinnerframes(tb, context=1):
    """copy of inspect.getinnerframes but with try/except on getframeinfo:
    Get a list of records for a traceback's frame and all lower frames.

    Each record contains a frame object, filename, line number, function
    name, a list of lines of context, and index within the context."""
    framelist = []
    while tb:
        try:
            frameinfo = (tb.tb_frame,) + inspect.getframeinfo(tb, context)
            framelist.append(inspect.FrameInfo(*frameinfo))
        except IndexError:  # python inspect may raise this error because it cant access to source
            pass
        tb = tb.tb_next
    return framelist


inspect.getinnerframes = getinnerframes


def new_log(exc=None):
    se = SystemExit()
    try:
        old_log(exc)
    except SystemExit as e:
        se = e
    if exc is not None:
        if not jupyter:
            import rich.traceback
            rich.get_console().print(
                rich.traceback.Traceback.from_exception(type(exc), exc, exc.__traceback__, show_locals=True))
        else:
            import traceback
            traceback.print_exc(file=sys.stderr)
    raise se


friendly_traceback.debug_helper.log_error = new_log
# lang = "he"
lang = "en"
jupyter = False
use_rich = False


def excepthook(exc_type, exc_value, tb, show_traceback=True):
    friendly_traceback.set_lang(lang)
    if jupyter:
        import IPython.display
        import IPython.core.ultratb
    else:
        IPython = None
    # load friendly
    fr = friendly_traceback.core.FriendlyTraceback(exc_type, exc_value, tb)
    fr.compile_info()
    # print traceback
    if IPython:
        ip = IPython.get_ipython()
        ###########
        if show_traceback:
            stb = ip.InteractiveTB.structured_traceback(exc_type,
                                                        exc_value, tb)

            ip._showtraceback(exc_type, exc_value, stb)
        ###############
    else:
        if show_traceback:
            print(fr.info["shortened_traceback"], file=sys.stderr)
    # get info from friendly
    generic = fr.info.get("generic", '')
    cause = fr.info.get("cause", '')
    suggest = fr.info.get("suggest", '')
    if suggest:
        suggest = "\n" + suggest

    # build Panel (or display Markdown for ipython)
    string = f'{generic}\n{suggest}\n{cause}'
    if IPython and use_rich:
        IPython.display.display(IPython.display.Markdown(string))

    else:
        trace = rich.panel.Panel(rich.markdown.Markdown(string),
                                 title="[traceback.title] הסבר ידידותי [dim](בדרך כלל אחרי הארור הלא ידידותי של פייתון):\n",
                                 expand=False,
                                 padding=(0, 1))

        rich.get_console().print(trace)


#####

# hook friendly_traceback partial_source:
from friendly_traceback.frame_info import FrameInfo, current_lang, cache, debug_helper, FakeLineObject, os

old_get_partial_source = FrameInfo._partial_source
en_sources = {}


def _partial_source(self, with_node_range: bool):
    """Copy of friendly_traceback.frame_info.FrameInfo._partial_source,but with <frozen importlib._bootstrap> as stdin.
    Gets the part of the source where an exception occurred,
    formatted in a pre-determined way, as well as the content
    of the specific line where the exception occurred.
    """
    _ = current_lang.translate

    file_not_found = _("Problem: source of `{filename}` is not available\n").format(
        filename=self.filename
    )
    source = line = ""

    if not self.lines and self.filename:
        # protecting against https://github.com/alexmojaki/stack_data/issues/13
        try:
            lineno = self.lineno
            s_lines = cache.get_source_lines(self.filename)
            self.lines = []  # noqa
            with_node_range = False
            linenumber = lineno - 2
            for line in s_lines[linenumber: lineno + 1]:
                self.lines.append(FakeLineObject(line, linenumber, lineno))
                linenumber += 1
        except Exception as e:  # noqa
            debug_helper.log_error(e)

    if self.lines:
        source, line = self._highlighted_source(with_node_range)
    elif self.filename and os.path.abspath(self.filename):
        if self.filename in ["<stdin>", "<string>", '<frozen importlib._bootstrap>']:
            pass
            # Using a normal Python REPL - source unavailable.
            # An appropriate error message will have been given via
            # cannot_analyze_stdin
        else:
            source = file_not_found
            debug_helper.log("Problem in get_partial_source().")
            debug_helper.log(file_not_found)
    elif not self.filename:  # pragma: no cover
        source = file_not_found
        debug_helper.log("Problem in get_partial_source().")
        debug_helper.log(file_not_found)
    else:  # pragma: no cover
        debug_helper.log("Problem in get_partial_source().")
        debug_helper.log("Should not have reached this option")
        debug_helper.log_error()

    if not source.endswith("\n"):
        source += "\n"

    return {"source": source, "line": line}


FrameInfo._partial_source = _partial_source
