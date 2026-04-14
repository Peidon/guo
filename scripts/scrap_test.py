import unittest
from generate_overnight_report import fetch_html, parse_investing_quote
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


if __name__ == '__main__':
    unittest.main()