import sys

from PyQt5.QtWidgets import QApplication

from app import CurrencyExchangeApp


def main():
    app = QApplication(sys.argv)
    window = CurrencyExchangeApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
