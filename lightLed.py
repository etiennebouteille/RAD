
from gpiozero import LED
print("PIN : ")
ledpin = input()

led = LED(ledpin)

while True:
    print("Status : ")
    status = input()
    if status == 1:
        led.on()
    elif status == 0:
        led.off()
    else:
        print("error")
    print (led.value)
