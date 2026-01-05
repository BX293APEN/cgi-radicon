#!/usr/bin/env python3
#coding:utf-8
import pycgi, pycgitb

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
        else: 
            self.pigpio             = _GPIO

        self.leftGPIO1              = 24
        self.leftGPIO2              = 18
        self.rightGPIO1             = 4
        self.rightGPIO2             = 23
        self.leftLED                = 20
        self.rightLED               = 21
        self.html                   = html
        self.gpio                   = self.pigpio.pi() 
        
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
    form    = pycgi.FieldStorage()
    log     = pycgitb.enable()
    with RadioControlCar() as rcc: 
        key     = form.getvalue("direction", default = "")
        log.handler(f"{key}が押されました")
        rcc.control(key)
