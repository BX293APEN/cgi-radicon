#!/usr/bin/env python3
#coding:utf-8
import pigpio, os, sys
from urllib import parse

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


    def __init__(self):
        self.leftGPIO1 = 24
        self.leftGPIO2 = 18
        self.rightGPIO1 = 4
        self.rightGPIO2 = 23
        self.leftLED = 20
        self.rightLED = 21
        self.gpio = pigpio.pi() #self.gpioにアクセスするためのインスタンスを作成します

        self.gpio.set_mode(self.leftGPIO1, pigpio.OUTPUT)
        self.gpio.set_mode(self.leftGPIO2, pigpio.OUTPUT)
        self.gpio.set_mode(self.rightGPIO1, pigpio.OUTPUT)
        self.gpio.set_mode(self.rightGPIO2, pigpio.OUTPUT)
    
    def __enter__(self, *args):
        print("Content-Type: text/html\n")
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
        print(html)
        return self
    def __exit__(self, *args):
        self.gpio.stop()
            
    def get_form_value(self): 
        method = os.environ.get("REQUEST_METHOD", "GET") 
        if method == "GET": 
            qs = os.environ.get("QUERY_STRING", "") 
            params = parse.parse_qs(qs) 
            return params.get("direction", [""])[0] 
        elif method == "POST": 
            length = int(os.environ.get("CONTENT_LENGTH", 0)) 
            body = sys.stdin.read(length) 
            params = parse.parse_qs(body) 
            return params.get("direction", [""])[0] 
        else:
            return "" 
    
if __name__ == "__main__": 
    with RadioControlCar() as rcc: 
        rcc.control(rcc.get_form_value())
