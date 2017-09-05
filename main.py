# main.py -- put your code here!
from machine import ADC
#from deepsleep import DeepSleep
import time
import usocket
numADCreadings = const(500)

#ds = DeepSleep()

# get the wake reason and the value of the pins during wake up
#wake_s = ds.get_wake_status()
#print(wake_s)

#if wake_s['wake'] == deepsleep.PIN_WAKE:
#    print("Pin wake up")
#elif wake_s['wake'] == deepsleep.TIMER_WAKE:
#    print("Timer wake up")
#else:  # deepsleep.POWER_ON_WAKE:
#    print("Power ON reset")

#ds.enable_pullups('P17')  # can also do ds.enable_pullups(['P17', 'P18'])
#ds.enable_wake_on_fall('P17') # can also do ds.enable_wake_on_fall(['P17', 'P18'])


def sendRequest(val):
#    try:
        sock = usocket.socket()
        sockaddr = usocket.getaddrinfo('35.176.234.59', 8086)[0][-1]
        sock.connect(sockaddr)
        sock.send(b"POST /write?db=glances HTTP/1.1\r\nHost: 35.176.234.59:8086\r\nUser-Agent: curl/7.47.0\r\nAccept: */*\r\nContent-Length: 42\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nposttest_metrix,host=posttest value=%2.4f\r\n" % val)
        status = str(sock.readline(), 'utf8')
        print(status)
        #code = status.split(" ")[1]
        sock.close()
        return 1

#    except Exception:
#        print("HTTP request failed")
#        return 0

adc = ADC(0)
adc_c = adc.channel(pin='P16')
adc_c()
x = 0
while x < 9000:
    x += 1
    y = 0
    total = 0
    while y < numADCreadings:
      y += 1
      total += adc_c.value() / 98.46
      time.sleep(0.01)
      #print("total: %15.13f " % total)
    val = total/y
    print("Final voltage: %2.4f" % val)
    print("About to send")
    sendRequest(val)
    print("Done sending - about to sleep")
    #ds.go_to_sleep(5)  # go to sleep for 60 seconds
    time.sleep(5)
