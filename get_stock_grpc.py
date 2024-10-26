# grpc_servers/get_stock_grpc.py
import grpc
from concurrent import futures  # スレッドプールを使用するためのモジュール
import get_stock_pb2 as get_stock_pb2 #  "." を追加 # Protocol Buffersコンパイラによって生成されるメッセージの定義を含むPythonモジュール
import get_stock_pb2_grpc as get_stock_pb2_grpc # Protocol Buffersコンパイラによって生成されるgRPCサービスに関連するコードを含むPythonモジュール
from get_stock_service import get_stock_data

class GetStockService(get_stock_pb2_grpc.GetStockServiceServicer):
    def GetStockData(self, request, context):
        # request:クライアントが指定した銘柄コードが含まれる
        # context:RPC呼び出しのコンテキスト情報を含む
        ticker = request.ticker
        stock_data = get_stock_data(ticker)
        return get_stock_pb2.GetStockResponse(stock_data=stock_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # gRPCサーバーインスタンス
    # max_workers=10: 最大10個のワーカースレッドを作成して、リクエストを並行処理
    get_stock_pb2_grpc.add_GetStockServiceServicer_to_server(GetStockService(), server) # GetStockServiceクラスとサーバーのインスタンス
    server.add_insecure_port('[::]:50051') # サーバーがポート50051ですべてのIPアドレス（IPv6を含む）でリスンしリクエストを受け付けるように設定
    server.start() # サーバー起動
    server.wait_for_termination() # サーバーが終了するまで待機

if __name__ == '__main__':
    serve()
