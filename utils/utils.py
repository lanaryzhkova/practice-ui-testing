def prices_array_handle(prices_text):
        return [float(price.replace("$", "")) for price in prices_text]

def price_str_handle(price_str):
        return float(price_str.text.strip().replace("$", "").replace(",", ""))

