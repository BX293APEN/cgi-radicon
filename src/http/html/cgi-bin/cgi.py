import os, sys
from urllib import parse

class FieldStorage:
    def __init__(self):
        self.method         = os.environ.get("REQUEST_METHOD", "GET")
        if self.method      == "GET": 
            self.query      = os.environ.get("QUERY_STRING", "")            # GET : URL の ? 以降が QUERY_STRING に入る
            self.params     = parse.parse_qs(self.query)                    # URL クエリ形式の文字列を辞書形式に変換

        elif self.method    == "POST": 
            length          = int(os.environ.get("CONTENT_LENGTH", 0))      # POST データの長さ(バイト数)を環境変数 CONTENT_LENGTH から取得
            self.query      = sys.stdin.read(length)                        # 標準入力(stdin)から length バイト分URLクエリ形式の文字列を読み込み
            self.params     = parse.parse_qs(self.query)                    # URL クエリ形式の文字列を辞書形式に変換
        else:
            self.query      = ""
            self.params     = dict()
    
    def getlist(
        self,
        formName            = "formName",
        default             = ""
    ):
        return self.params.get(formName, [default])
    
    def getfirst(
        self,
        formName            = "formName",
        default             = ""
    ):
        return self.getlist(formName, default)[0]
    
    def getvalue(
        self,
        formName            = "formName",
        default             = ""
    ):
        value               = self.getlist(formName, default)
        if len(value) > 1:
            return value
        else:
            return value[0]