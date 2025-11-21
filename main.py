"""
Crypto Multi-Exchange Arbitrage Opportunity Detector
-----------------------------------------------------

This script compares live prices of multiple exchanges and
detects arbitrage opportunities in real-time.

Exchanges:
- Binance
- KuCoin
- Kraken
- Coinbase

Purely for educational + demo purpose.
"""

import requests
import time


# -----------------------------------------
# Helper: Safe GET Request
# -----------------------------------------
def safe_get(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json()
    except Exception:
        return None


# -----------------------------------------
# Fetch Prices from Exchanges
# -----------------------------------------

def binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = safe_get(url)
    return float(data["price"]) if data else None


def kucoin_price(symbol="BTC-USDT"):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
    data = safe_get(url)
    return float(data["data"]["price"]) if data else None


def kraken_price(pair="XBTUSDT"):
    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
    data = safe_get(url)
    if data and data.get("result"):
        key = list(data["result"])[0]
        return float(data["result"][key]["a"][0])
    return None


def coinbase_price(symbol="BTC-USD"):
    url = f"https://api.coinbase.com/v2/prices/{symbol}/spot"
    data = safe_get(url)
    return float(data["data"]["amount"]) if data else None


# -----------------------------------------
# Arbitrage Finder
# -----------------------------------------

def get_all_prices():
    return {
        "Binance": binance_price(),
        "KuCoin": kucoin_price(),
        "Kraken": kraken_price(),
        "Coinbase": coinbase_price(),
    }


def find_arbitrage(prices, threshold=1.0):
    """
    threshold = percent difference required (e.g., 1% profit)
    """
    exchanges = list(prices.keys())
    opps = []

    for i in range(len(exchanges)):
        for j in range(len(exchanges)):
            if i == j:
                continue

            ex1 = exchanges[i]
            ex2 = exchanges[j]

            p1 = prices[ex1]
            p2 = prices[ex2]

            if not p1 or not p2:
                continue

            diff = ((p2 - p1) / p1) * 100

            if diff >= threshold:
                opps.append({
                    "Buy From": ex1,
                    "Price Buy": p1,
                    "Sell On": ex2,
                    "Price Sell": p2,
                    "Profit %": round(diff, 3)
                })

    return opps


# -----------------------------------------
# Main Loop
# -----------------------------------------

def main():
    print("\n🚀 Real-Time Crypto Arbitrage Scanner Started")
    print("Scanning exchanges every 5 seconds...\n")

    while True:
        prices = get_all_prices()

        print("Live Prices:")
        for ex, pr in prices.items():
            print(f"  {ex:10s} : {pr}")

        print("\nChecking Arbitrage Opportunities...")

        opps = find_arbitrage(prices, threshold=1.0)

        if opps:
            print("\n🔥 PROFITABLE ARBITRAGE FOUND!")
            for o in opps:
                print(f"\nBuy on {o['Buy From']} @ {o['Price Buy']}")
                print(f"Sell on {o['Sell On']} @ {o['Price Sell']}")
                print(f"➡ Profit: {o['Profit %']}%\n")
        else:
            print("❌ No profitable arbitrage right now.")

        print("-" * 40)
        time.sleep(5)


if __name__ == "__main__":
    main()
