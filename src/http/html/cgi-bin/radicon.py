#!/usr/bin/env python3
#coding:utf-8
import os, sys
from urllib import parse

class cgi:
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
    
    def getvalue(
        self,
        formName            = "formName",
        default             = ""
    ):
        return self.getlist(formName, default)[0]

class _GPIO:
    OUTPUT                  = 0 

    class pi:
        def __init__(self):
            pass

        def write(self, pin, value): 
            pass 

        def set_mode(self, pin, mode): 
            pass

        def stop(self): 
            pass

class RadioControlCar():
    def control(self, key):
        if(key == "前"): # 上
            self.gpio.write(self.leftGPIO1, 1)
            self.gpio.write(self.leftGPIO2, 0)
            self.gpio.write(self.rightGPIO1, 1)
            self.gpio.write(self.rightGPIO2, 0)

            self.gpio.write(self.leftLED, 1)
            self.gpio.write(self.rightLED, 1)

        elif(key == "後"):# 下
            self.gpio.write(self.leftGPIO1, 0)
            self.gpio.write(self.leftGPIO2, 1)
            self.gpio.write(self.rightGPIO1, 0)
            self.gpio.write(self.rightGPIO2, 1)
            self.gpio.write(self.leftLED, 0)
            self.gpio.write(self.rightLED, 0)

        elif(key == "右"): # 右
            self.gpio.write(self.leftGPIO1, 0)
            self.gpio.write(self.leftGPIO2, 1)
            self.gpio.write(self.rightGPIO1, 1)
            self.gpio.write(self.rightGPIO2, 0)
            self.gpio.write(self.leftLED, 0)
            self.gpio.write(self.rightLED, 1)

        
        elif(key == "左"): # 左
            self.gpio.write(self.leftGPIO1, 1)
            self.gpio.write(self.leftGPIO2, 0)
            self.gpio.write(self.rightGPIO1, 0)
            self.gpio.write(self.rightGPIO2, 1)
            self.gpio.write(self.leftLED, 1)
            self.gpio.write(self.rightLED, 0)


        else: # stop
            self.gpio.write(self.leftGPIO1, 0)
            self.gpio.write(self.leftGPIO2, 0)
            self.gpio.write(self.rightGPIO1, 0)
            self.gpio.write(self.rightGPIO2, 0)
            self.gpio.write(self.leftLED, 0)
            self.gpio.write(self.rightLED, 0)


    def __init__(
        self,
        html = """
<!DOCTYPE html>
<html lang="ja">
    <head>
        <title>
            Radicon
        </title>
        <meta charset="UTF-8">
    </head>
    <body>
        <form>
            <br>
                <input type="submit" value="前" name="direction" style="margin-left:50px"/>
            <br>
                <input type="submit" value="左" name="direction"/>
                <input type="submit" value="□" name="direction"/>
                <input type="submit" value="右" name="direction"/>
            <br>
                <input type="submit" value="後" name="direction" style="margin-left:50px"/>
        </form>
    </body>
    <style>
        input{
            width:50px;
            height:50px;
            font-size: 30px;
        }
    </style>
</html>
"""
    ):
        try: 
            import pigpio
            self.PIGPIO_AVAILABLE   = True 
        except ImportError:
            self.PIGPIO_AVAILABLE   = False
            
        if self.PIGPIO_AVAILABLE: # self.gpioにアクセスするためのインスタンスを作成します
            self.pigpio             = pigpio
            self.gpio               = pigpio.pi() 
        else: 
            self.pigpio             = _GPIO
            self.gpio               = _GPIO().pi()


        self.leftGPIO1              = 24
        self.leftGPIO2              = 18
        self.rightGPIO1             = 4
        self.rightGPIO2             = 23
        self.leftLED                = 20
        self.rightLED               = 21
        self.html                   = html
        
        self.gpio.set_mode(self.leftGPIO1, self.pigpio.OUTPUT)
        self.gpio.set_mode(self.leftGPIO2, self.pigpio.OUTPUT)
        self.gpio.set_mode(self.rightGPIO1, self.pigpio.OUTPUT)
        self.gpio.set_mode(self.rightGPIO2, self.pigpio.OUTPUT)
    
    def __enter__(self, *args):
        print("Content-Type: text/html\n")
        print(self.html)
        return self
    
    def __exit__(self, *args):
        self.gpio.stop()


if __name__ == "__main__": 
    form = cgi()
    with RadioControlCar() as rcc: 
        rcc.control(
            form.getvalue(
                "direction", 
                default = ""
            )
        )
