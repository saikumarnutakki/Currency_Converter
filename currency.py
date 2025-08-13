import requests

class CurrencyConverter:
    BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1"

    def __init__(self):
        self.currencies = self.get_currencies()

    def get_currencies(self):
        """Fetch all available currency codes."""
        try:
            url = f"{self.BASE_URL}/currencies.json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return list(data.keys())
        except Exception as e:
            print("Error fetching currency list:", e)
            return []

    def convert(self, from_currency, to_currency, amount):
        """Convert amount from one currency to another."""
        try:
            url = f"{self.BASE_URL}/currencies/{from_currency.lower()}.json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            rates = data[from_currency.lower()]  # actual rate dictionary

            rate = rates.get(to_currency.lower())
            if rate is None:
                print(f"No rate found for {to_currency.upper()}.")
                return None, None

            converted = round(amount * rate, 2)
            return converted, rate
        except Exception as e:
            print("Error during conversion:", e)
            return None, None

def main():
    print("===== Currency Converter =====")
    converter = CurrencyConverter()

    if not converter.currencies:
        print("Unable to load currency list. Check your internet connection or the API endpoint.")
        return

    print(f"Available currencies (sample): {', '.join(sorted(converter.currencies)[:20])} ...")
    print("(e.g., USD, INR, EUR, GBP, JPY)")

    src = input("From Currency: ").strip().lower()
    tgt = input("To Currency: ").strip().lower()

    if src not in converter.currencies or tgt not in converter.currencies:
        print("Invalid currency code. Please use standard ISO codes.")
        return

    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount entered!")
        return

    result, rate = converter.convert(src, tgt, amount)
    if result is not None:
        print(f"\n{amount} {src.upper()} = {result} {tgt.upper()} (Rate: {rate})")

if __name__ == "__main__":
    main()
