# Currency Exchange App

PyQt5 desktop currency converter that uses Yahoo Finance (via `yfinance`) to fetch real-time rates. The UI lets you pick any supported currency, type an amount, and see the converted value plus the current exchange rate.

## Project Layout

- `currency_data.py` – dictionary of supported currency codes and helper to get them sorted.
- `app.py` – `CurrencyExchangeApp` window class: builds the UI, wires the combo boxes, and performs conversions.
- `main.py` – entry point that creates `QApplication` and launches the window.

## Getting Started

1. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If there is no `requirements.txt`, manually install the basics:
   ```bash
   pip install PyQt5 yfinance
   ```
3. (Optional) Place flag images under `flags/<CURRENCY_CODE>.png` to show icons in the drop-downs.
4. Run the app:
   ```bash
   python3 main.py
   ```

## Notes

- Exchange rates come from Yahoo Finance. Ensure the machine has internet access when running conversions.
- The amount field accepts commas; they are stripped before conversion.
- Errors and validation feedback appear through PyQt message boxes.
