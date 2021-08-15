import PySimpleGUI as sg
import PySimpleGUI.PySimpleGUI as basic

basic._refresh_debugger = lambda *args, **kwargs: False  # disable PySimpleGUI debugger


#
def wraps(elem):
    class element(elem):
        def __init__(self, *args, מפתח=None, **kwargs):
            super(element, self).__init__(*args, key=מפתח, **kwargs)
            self.עדכן = self.update

    return element


טקסט = wraps(sg.T)
כפתור = wraps(sg.B)
תיבת_טקסט = wraps(sg.In)

חלון_קופץ = sg.popup
חלון_נסגר = sg.WIN_CLOSED
סיגנון = sg.theme
הדפס = sg.easy_print


class חלון(sg.Window):
    def __init__(self, title, *args, text_justification="right", **kwargs):
        super().__init__(title, *args, text_justification=text_justification, **kwargs)
        self.קרא = self.read
        self.סגור = self.close
        self.קבוע = self.finalize


def create_look_and_feel():
    nl = {
        "רגיל": "SystemDefault",
        "ירוק": "LightGreen",
        "זהב": "DarkAmber",
        "כחול": "BlueMono",
        "תכלת": "LightBlue",
    }
    n = {}
    for k, v in nl.items():
        n.update({k: sg.LOOK_AND_FEEL_TABLE[v]})
    return n


sg.LOOK_AND_FEEL_TABLE.update(create_look_and_feel())
