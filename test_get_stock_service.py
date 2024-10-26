# tests/test_services/test_get_stock_service.py
import unittest
from get_stock_service import get_stock_data

class TestGetStockService(unittest.TestCase):
    def test_get_stock_data(self):
        data = get_stock_data("^GSPC")
        self.assertIn("Close", data)
        self.assertGreater(len(data["Close"]), 0)

if __name__ == "__main__":
    unittest.main()
