import PySimpleGUI as sg
import PySimpleGUI.PySimpleGUI as basic

basic._refresh_debugger = lambda *args, **kwargs: False  # disable PySimpleGUI debugger

hebrew_kwargs = {
    "מפתח": "key"
}


#
def wraps(elem):
    class element(elem):

        def __init__(self, *args, **kwargs):
            for k, v in hebrew_kwargs.items():
                if kwargs.get(k, None):  # there is one of hebrew_kwargs
                    kwargs[v] = kwargs[k]
                    del kwargs[k]
            super(element, self).__init__(*args, **kwargs)
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


def main():
    טקסט("t", מפתח="key"),
    סיגנון("זהב")
    t = [
        [טקסט("t", מפתח="key")],

    ]
    window = חלון("", t)
    window.read()


if __name__ == '__main__':
    main()
