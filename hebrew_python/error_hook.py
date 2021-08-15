from types import FrameType
import friendly.core
import rich.panel
import rich.traceback
import rich.markdown
import sys
import inspect

friendly.debug_helper.DEBUG = True
old_log = friendly.debug_helper.log_error


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


friendly.debug_helper.log_error = new_log
lang = "he"
jupyter = False
use_rich = False


def excepthook(exc_type, exc_value, tb,show_traceback = True):
    friendly.set_lang(lang)
    if jupyter:
        import IPython.display
        import IPython.core.ultratb
    else:
        IPython = None
    # load friendly
    fr = friendly.core.FriendlyTraceback(exc_type, exc_value, tb)
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
    if IPython and use_rich :
        IPython.display.display(IPython.display.Markdown(string))

    else:
        trace = rich.panel.Panel(rich.markdown.Markdown(string),
                                 title="[traceback.title] הסבר ידידותי [dim](בדרך כלל אחרי הארור הלא ידידותי של פייתון):\n",
                                 expand=False,
                                 padding=(0, 1))

        rich.get_console().print(trace)


#####
old_get_partial_source = friendly.core.get_partial_source
en_sources = {}


def get_partial_source(filename, linenumber, lines, index, text_range=None):
    if index is not None:
        return old_get_partial_source(filename, linenumber, lines, index, text_range)
    else:  # index is none
        if filename == '<frozen importlib._bootstrap>':
            frame: inspect.FrameInfo = inspect.currentframe().f_back.f_locals.get("record", None)
            if frame:
                frame: FrameType = frame.frame
                if frame.f_locals.get("name", None) in en_sources:
                    source = en_sources[frame.f_locals["name"]]
                    return {
                        "source": source,
                        "line": ''
                    }
    return {
        "source": '\n',
        "line": ''
    }
    # print(frame.f_globals)
    # print(frame.f_locals["name"])
    # return old_get_partial_source(filename, linenumber, lines, index, text_range)


friendly.core.get_partial_source = get_partial_source
