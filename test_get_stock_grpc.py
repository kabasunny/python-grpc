# tests/test_grpc_servers/test_get_stock_grpc.py
import unittest  # 標準的なテストフレームワークをインポート
import grpc
from concurrent import futures
from get_stock_grpc import GetStockService, serve  # サービスとサーバー起動関数をインポート
import sys
sys.path.insert(0, '<プロジェクトのルートディレクトリのパス>')

import get_stock_pb2 as get_stock_pb2 #  "." を追加
import get_stock_pb2_grpc as  get_stock_pb2_grpc
from get_stock_service import get_stock_data

class TestGetStockGRPC(unittest.TestCase):  # テストクラスの定義
    @classmethod
    def setUpClass(cls):  # クラス全体で一度だけ実行されるセットアップメソッド
        cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        get_stock_pb2_grpc.add_GetStockServiceServicer_to_server(GetStockService(), cls.server)
        cls.server.add_insecure_port('[::]:50051')
        cls.server.start()
    @classmethod
    def tearDownClass(cls):  # クラス全体で一度だけ実行されるクリーンアップメソッド
        cls.server.stop(None)

    def test_get_stock_data(self):  # 実際のテストメソッド
        with grpc.insecure_channel('localhost:50051') as channel:  # gRPCチャンネルを作成
            stub = get_stock_pb2_grpc.GetStockServiceStub(channel)  # スタブを作成
            response = stub.GetStockData(get_stock_pb2.GetStockRequest(ticker="^GSPC"))  # リクエストを送信
            print("gPRCレスポンスは Protocol Buffers の形式:", response)  # レスポンスをターミナルに表示
            self.assertIn("Close", response.stock_data)  # レスポンスに"Close"キーが含まれていることを確認

if __name__ == "__main__":  # スクリプトが直接実行された場合にテストを実行
    unittest.main()


# python -m unittest discover -s .  -p 'test*.py'
# python -m unittest test_get_stock_grpc