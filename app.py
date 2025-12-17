import os
from typing import Tuple

import yfinance as yf
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QComboBox,
    QCompleter,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from currency_data import CURRENCIES, sorted_currency_codes


class CurrencyExchangeApp(QMainWindow):
    """Main window that handles user interactions and conversions."""

    def __init__(self):
        super().__init__()
        self.currencies = CURRENCIES
        self.currency_codes = sorted_currency_codes()

        self._setup_window()
        self._setup_widgets()
        self._populate_currency_combos()

    def _setup_window(self):
        self.setWindowTitle("Currency Exchange")
        self.setGeometry(100, 100, 400, 300)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

    def _setup_widgets(self):
        font = QFont()
        font.setPointSize(12)

        self.amount_label = QLabel("Amount:")
        self.amount_label.setFont(font)
        self.amount_input = QLineEdit()
        self.amount_input.setFont(font)

        self.from_currency_label = QLabel("From Currency:")
        self.from_currency_label.setFont(font)
        self.from_currency_combo = self._build_currency_combo(font)

        self.to_currency_label = QLabel("To Currency:")
        self.to_currency_label.setFont(font)
        self.to_currency_combo = self._build_currency_combo(font)

        self.convert_button = QPushButton("Convert")
        self.convert_button.setFont(font)
        self.convert_button.clicked.connect(self.convert_currency)

        self.result_label = QLabel("")
        self.result_label.setFont(font)

        self.rate_label = QLabel("")
        self.rate_label.setFont(font)

        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_input)
        self.layout.addWidget(self.from_currency_label)
        self.layout.addWidget(self.from_currency_combo)
        self.layout.addWidget(self.to_currency_label)
        self.layout.addWidget(self.to_currency_combo)
        self.layout.addWidget(self.convert_button)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.rate_label)

    @staticmethod
    def _build_currency_combo(font: QFont) -> QComboBox:
        combo = QComboBox()
        combo.setFont(font)
        combo.setEditable(True)
        return combo

    def _populate_currency_combos(self):
        self._configure_combo(self.from_currency_combo)
        self._configure_combo(self.to_currency_combo)

    def _configure_combo(self, combo_box: QComboBox):
        completer = QCompleter(self.currency_codes, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        combo_box.setCompleter(completer)

        for code in self.currency_codes:
            currency_name = self.currencies[code]
            display_text = f"{code} - {currency_name}"
            flag_path = os.path.join('flags', f'{code}.png')
            flag_icon = QIcon(flag_path) if os.path.exists(flag_path) else QIcon()
            combo_box.addItem(flag_icon, display_text)

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text().replace(',', ''))
            from_currency = self._selected_currency(self.from_currency_combo)
            to_currency = self._selected_currency(self.to_currency_combo)

            if from_currency == to_currency:
                QMessageBox.warning(self, "Error", "Please select different currencies for conversion.")
                return

            exchange_rate = self._fetch_exchange_rate(from_currency, to_currency)
            converted_amount = amount * exchange_rate
            formatted_amount = f"{converted_amount:,.2f}"
            self.result_label.setText(f"{amount:,.2f} {from_currency} = {formatted_amount} {to_currency}")
            self.rate_label.setText(f"Exchange Rate: 1 {from_currency} = {exchange_rate:.4f} {to_currency}")
        except ValueError as ve:
            QMessageBox.critical(self, "Error", f"Value Error: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert currency: {e}")

    @staticmethod
    def _selected_currency(combo_box: QComboBox) -> str:
        return combo_box.currentText().split(' - ')[0]

    def _fetch_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        rate_from_usd, rate_to_usd = self._pair_rates(from_currency, to_currency)
        return rate_from_usd * rate_to_usd

    def _pair_rates(self, from_currency: str, to_currency: str) -> Tuple[float, float]:
        if from_currency != 'USD':
            ticker_from_usd = f"{from_currency}USD=X"
            data_from_usd = yf.download(ticker_from_usd, period='1d')
            if data_from_usd.empty:
                raise ValueError(f"No data fetched for {ticker_from_usd}")
            exchange_rate_from_usd = data_from_usd['Close'].iloc[-1].item()
        else:
            exchange_rate_from_usd = 1.0

        if to_currency != 'USD':
            ticker_to_usd = f"USD{to_currency}=X"
            data_to_usd = yf.download(ticker_to_usd, period='1d')
            if data_to_usd.empty:
                raise ValueError(f"No data fetched for {ticker_to_usd}")
            exchange_rate_to_usd = data_to_usd['Close'].iloc[-1].item()
        else:
            exchange_rate_to_usd = 1.0

        return exchange_rate_from_usd, exchange_rate_to_usd
