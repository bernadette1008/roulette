# roulette
파이썬를 통해 만든 롤렛머신


## 1. 시작
![start](https://user-images.githubusercontent.com/103907857/233059610-5d9e8b89-d5de-44ca-8bb6-d2d906f97b32.png)
### 처음 시작 시의 모습
LED를 통해 롤렛머신을 표시하며, 공의 위치는 가장 밝은 LED로 표시한다.
(기본 RGB(0 ~ 5, 0 ~ 5, 0 ~ 5), 공의 위치 RGB(0 ~ 255, 0 ~ 255, 0 ~ 255))
초기 자금으로 1000원을 주며 현재 소유한 자금은 세그먼트를 통해 출력하며,
LCD를 초기화시켜 아무것도 없는 상태로 만든다.


## 2. 배팅
![betting](https://user-images.githubusercontent.com/103907857/233059943-4afd4dce-5335-48da-badf-c5432a71fc85.jpg)
### 배팅(코드를 통해 입력)
자신이 배팅할 곳과 배팅할 금액을 키보드를 이용하여 입력하여 장치를 조작.
이 배팅한 금액과 종류는 LCD를 통해 출력


## 3. 회전
![spin](https://user-images.githubusercontent.com/103907857/233060272-8a71b27c-da01-41b5-b5e4-5d4891603c34.jpg)
입력이 끝나면 총 16개의 LED가 마치 돌아가듯 깜박이며 마지막엔 어느 한 장소만 밝게 빛난다. 그 위치는 각 위치마다 번호, 색상이 다르며, 번호의 경우엔 초록색부터 시작하며, 숫자는 0에서 15까지로 인식된다.

## 배팅 종류
![type1](https://user-images.githubusercontent.com/103907857/233061075-2fcb811f-4446-45c2-a6ae-b6ef3b013d66.jpg)
![type2](https://user-images.githubusercontent.com/103907857/233061082-c4fac991-b4d5-4d58-8e35-657242775de6.jpg)
![type3](https://user-images.githubusercontent.com/103907857/233061086-8d3fc3b2-257c-4198-8e5e-b5fab607f277.jpg)
![type4](https://user-images.githubusercontent.com/103907857/233061090-5df4fa01-b19c-40df-87c0-4b8fc8b4eb08.png)

## 코드 설명
```python
def dobak_on():
    for i in range(0, 16):
        if (i%2)==0:
            led[i] = ((5,0,0))
        elif (i%2) == 1:
            led[i] = ((0,0,5))
        if i == 0:
            led[i] = ((0,5,0))
```
LED의 불빛이 들어오게 하는 코드로 짝수는 빨강색, 홀수는 파란색, 그리고 0번째 LED는 초록색으로 불빛이 들어오게 한다.

```python
def spin(i):
    if (i%2)==0:
        led[i] = ((255,0,0))
    elif (i%2) == 1:
        led[i] = ((0,0,255))
    if i == 0:
        led[i] = ((0,255,0))
```
매개변수로 받은 i번째 LED의 불빛의 강도를 최대로 변경한다.
해당 코드를 통해 마치 롤렛이 돌아가는 듯한 느낌을 표현한다.
자세한 내용은 bits_operation에서 설명.

```python
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
        else:
            t += 1 * (rand/10)
    dobak_on()
    spin(now)
    return now
``` 
bits_operation이 입력받는 매개변수론 pixels(LED 배열), now(현재 롤렛의 공(가장 빛나는 LED)가 위치할 곳), t(롤렛이 돌아갈 시간)이 있으며, 반복문을 통해 t가 5보다 커질 때까지 반복을 시키며, 처음엔 모든 LED가 같은 밝기로 있게하였다가 바로 spin함수를 통해 now 위치의 LED만 최대 밝기로 켜지게 하며 이후엔 다음 LED가 켜지도록 now에 +1을 하고 시간을 랜덤하게 증가하도록 한다. 이때 now의 숫자는 16이 될 경우엔 해당 위치에 LED가 없기 때문에 처음 LED인 0으로 돌아가도록 if문을 활용하여 now를 0으로 변경하고, time에 경우엔 현재 시간마다 만약 t가 0.1보다 작으면 0.001부터 0.009까지의 랜덤한 수가 더해지도록 하였고, 1보다 작거나 같으면 0.1부터 0.9가 더해지도록 하였다.
이 반복문이 끝난 후엔 마지막으로 멈춘 공의 위치를 보여주기 위해 다시한번 dobak_on()과 spin(now)를 실행하여 LED를 업데이트한 후 함수를 종료한다.

```python
def printmoney(my_money):
    segment.fill(0)
    segment.print(my_money)
```
매개변수를 통해 현재 가진 돈을 입력받고, segment를 초기화 후 입력받은 값을 segments를 통해 출력한다.

```python
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
```
ch함수는 매개변수로 t(배팅 타입)과 money(배팅 금액)을 입력받고, t를 통해 자신이 어떤 것에 배팅을 하였는지를 LCD의 첫번째 줄에 출력을 하고, 두번째 줄엔 자신이 배팅한 금액을 출력한다.

```python
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
```  
bet은 배팅을 담당하는 함수로 현재 자신이 가진 돈 액수를 매개변수로 받으며, 첫번째로 자신이 어떤 것에 배팅을 할 것인지 입력을 받고
각 배팅 마다 필요로 하는 요구사항과 배팅 금액을 입력받아 ch함수를 통해 자신이 배팅한 타입과 금액을 출력하도록 하고 bits_operation을 통해 롤렛을 굴려 공이 멈춘 위치를 리턴 받는다.
이때 그 위치 값을 통해 사용자가 게임을 승리했는지 패배했는지 판단, 게임에 승리할 경우 배팅한 금액의 2배만큼 돌려받고, 패배 시엔 배팅한 금액을 잃으며, 그런 후의 자신이 가진 금액을 리턴한다.

```python
n = 0
my_money = 1000
CLCD.clear()
dobak_on()
while my_money != 0:
    printmoney(my_money)
    my_money = bet(my_money)
    time.sleep(1)
```   
코드의 메인부분
초기 자금은 1000으로 설정하고 LCD를 초기화하고 LED을 활성화시킨다.
이후엔 사용자가 가진 돈이 0이 될 때까지 게임을 반복시킨다.
