'''
MoNoA main app launcher
'''
import sys
from PyQt5.QtWidgets import QApplication
from ui.monoa_ui import MonoaMainWindow
import warnings
# Remove PyQt-related deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main() -> None:
    '''
    MoNoA main() function
    - init instances of QApplication and MonoaMainWindow
    - pass user screen size to MonoaMainWindow
    - show main window
    '''
    app = QApplication(sys.argv)
    win = MonoaMainWindow(user_screen_size=app.primaryScreen().size())
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
