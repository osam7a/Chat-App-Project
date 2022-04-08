from pyqt5 import MainWindow
from pyqt5.uic import loadUi

from Client.cache import Cache

class Window(MainWindow):
    def __init__(self, window):
        super().__init__()

        loadUi(f"Client/.ui/{window}.ui")


def launch():
    global loggedin
    cache = Cache()
    loggedin = cache.loggedin
    if loggedin:
        Window("login")
    else:
        Window("main")