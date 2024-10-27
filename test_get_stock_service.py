# tests/test_services/test_get_stock_service.py
import unittest
from get_stock_service import get_stock_data

class TestGetStockService(unittest.TestCase):
    def test_get_stock_data(self):
        data = get_stock_data("^GSPC")  # get_stock_data 関数を呼び出し
        print("取得データはPython の辞書形式:", data)  # データをターミナルに表示
        self.assertIn("Close", data)  # データに "Close" キーが含まれていることを確認
        self.assertGreater(data["Close"].size, 0)  # "Close" データのサイズが 0 より大きいことを確認


if __name__ == "__main__":
    unittest.main()


# python -m unittest discover -s .  -p 'test*.py'
# python -m unittest test_get_stock_service