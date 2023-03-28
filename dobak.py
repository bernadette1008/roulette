import board
import neopixel_spi
import time
import busio
import random

from clcd.I2C_Charactor_Liquid_Crystal_Display import LCD
from clcd.I2C_Device import *
from adafruit_ht16k33 import segments
from colorsys import hls_to_rgb
from collections import deque

i2c = busio.I2C(board.SCL, board.SDA)
segment = segments.set(i2c, address = 0x77)
CLCD = LCD(i2c)
led = neopixel_spi.NeoPixel_SPI(board.SPI(), 16, pixel_order=neopixel_spi.GRB)


def dobak_on():
    for i in range(0, 16):
        if (i%2)==0:
            led[i] = ((5,0,0))
        elif (i%2) == 1:
            led[i] = ((0,0,5))
        if i == 0:
            led[i] = ((0,5,0))

def spin(i):
    if (i%2)==0:
        led[i] = ((255,0,0))
    elif (i%2) == 1:
        led[i] = ((0,0,255))
    if i == 0:
        led[i] = ((0,255,0))

##LED 출력
def bits_operation(pixels, now ,t):
    items = deque(pixels)
    while t <= 5:
        dobak_on()
        spin(now)
        now += 1
        if now == 16:
            now = 0
        time.sleep(t)
        rand = random.randint(1, 10)
        if t < 0.1:
            t += 0.001 * rand
        elif t <= 1:
            t += 0.1 * rand
        else:
            t += 1 * (rand/10)
    dobak_on()
    spin(now)
    return now


##세그먼트 출력
def printmoney(my_money):
    segment.fill(0)
    segment.print(my_money)    

##LCD 출력
def ch(t, money):
    if t == '1':
        CLCD.clear()
        CLCD.setCursor(0,0)
        CLCD.display_string('Type : Check')
        CLCD.setCursor(1,0)
        CLCD.display_string("BETING : "+ str(money))
    elif t == '2':
        CLCD.clear()
        CLCD.setCursor(0,0)
        CLCD.display_string('Type : Red Black')
        CLCD.setCursor(1,0)
        CLCD.display_string("BETING : "+ str(money))
    elif t == '3':
        CLCD.clear()
        CLCD.setCursor(0,0)
        CLCD.display_string('Type : Even Odd')
        CLCD.setCursor(1,0)
        CLCD.display_string("BETING : "+ str(money))
    elif t == '4':
        CLCD.clear()
        CLCD.setCursor(0,0)
        CLCD.display_string('Type : Zero')
        CLCD.setCursor(1,0)
        CLCD.display_string("BETING : "+ str(money))


##배팅
def bet(my_money):
    n = 0
    b = input("1. 숫자, 2. RED BLUE, 3. 짝홀, 4: 0(GREEN) : ")
    
    if b == '1':
        sel = int(input("1~15 : "))
        while True:
            money = int(input("bet money : "))
            if money <= my_money and money > 0:
                my_money -= money
                printmoney(my_money)
                break
        ch(b, money)
        n = bits_operation(led, n, 0.001)
        if sel == n:
            my_money += money*4
            print("win!")
        else:
            money = 0
            print("lose...")
    elif b == '2':
        while True:
            sel = input("1. RED, 2. BLUE : ")
            if sel == '1' or sel == '2':
                break
        while True:
            money = int(input("bet money : "))
            if money <= my_money and money > 0:
                my_money -= money
                printmoney(my_money)
                break
        ch(b, money)
        n = bits_operation(led, n, 0.001)
        items = deque(led)
        if sel == '1':
            if n != 0 and list((255,0,0)) == items[n]:
                my_money += money*2
                print("win!")
            else:
                money = 0
                print(items[n])
                print("lose...")
        elif(sel == '2'):
            if n != 0 and list((0,0,255)) == items[n]:
                my_money += money*2
                print("win!")
            else:
                money = 0
                print("lose...")
    elif b == '3':
        while True:
            sel = input("1. 짝수, 2. 홀수 : ")
            if sel == '1' or sel == '2':
                break
        while True:
            money = int(input("bet money : "))
            if money <= my_money and money > 0:
                my_money -= money
                printmoney(my_money)
                break
        ch(b, money)
        n = bits_operation(led, n, 0.001)
        if sel == '1':
            if n != 0 and (n % 2) == 0:
                my_money += money*2
                print("win!")
            else:
                money = 0
                print("lose...")
        elif(sel == '2'):
            if n != 0 and (n % 2) == 1:
                my_money += money*2
                print("win!")
            else:
                money = 0
                print("lose...")
    elif b == '4':
        while True:
            money = int(input("bet money : "))
            if money <= my_money and money > 0:
                my_money -= money
                printmoney(my_money)
                break
        ch(b, money)
        n = bits_operation(led, n, 0.001)
        if n == 0:
            my_money += money*10
            print("win!")
        else:
            money = 0
            print("lose...")
    return my_money

##실행구간
n = 0
my_money = 1000
CLCD.clear()
dobak_on()
while my_money != 0:
    printmoney(my_money)
    my_money = bet(my_money)
    time.sleep(1)