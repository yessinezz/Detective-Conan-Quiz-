import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Set application-wide font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Icon.jpg')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
