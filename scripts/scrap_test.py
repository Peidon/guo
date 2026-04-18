import unittest
from generate_overnight_report import fetch_html, parse_investing_quote, fetch_tradingeconomics_iron_ore,yfinance_quote_info
import requests

class TestScrap(unittest.TestCase):
    def test_fetch_asx_vix200(self):
        url = "https://www.investing.com/indices/s-p-asx-200-vix"

        session = requests.Session()
        html = fetch_html(
            session,
            url,
            timeout=20,
            prefer_browser = True
        )
        quote = parse_investing_quote(html, url)
        self.assertTrue(quote is not None)

    def test_fetch_iron_ore(self):
        session = requests.session()
        quote = fetch_tradingeconomics_iron_ore(session, 20)
        self.assertTrue(quote is not None)

    def test_fetch_stoxx600(self):
        quote = yfinance_quote_info('^STOXX')
        print(quote)


if __name__ == '__main__':
    unittest.main()