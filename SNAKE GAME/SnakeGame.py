from PyQt5.QtWidgets import QApplication

import Window


if __name__ == "__main__":
    main_event = QApplication([])
    window = Window.MainWindow()
    main_event.exec()
