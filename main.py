import subprocess
import time
from datetime import datetime
import pytz
from random import randint

print("""modes 
1. normal mode 
2. stops automatically after call cut
3. extrime mode (call until manually stop)
""")

def stop_until_time(t, m):
    zone = pytz.timezone("Asia/Kolkata")
    n = datetime.now(zone).timetuple()
    print(n)
    print(f"n.tmhour={n.tm_hour}...tm_min={n.tm_min} ")
    print(f"t={t}....m={m}")
    while n.tm_hour < t or m > n.tm_min:
        time.sleep(10)
        n = datetime.now(zone).timetuple()

def shutdown_devices():
    subprocess.run("adb shell reboot -p", shell=True)
    time.sleep(2)
    subprocess.run("init 0", shell=True)

def call_action(phone_number, call_cut_duration):
    subprocess.run(f"adb shell am start -a android.intent.action.CALL -d tel:{phone_number}", shell=True)
    time.sleep(call_cut_duration)
    subprocess.run("adb shell input keyevent KEYCODE_ENDCALL", shell=True)
    time.sleep(2)

mode = input("enter mode: ")
phone_number = input("phone number? ")
t = int(input("enter hour: "))
m = int(input("enter minute : "))

if mode=='1' or mode=='3':
    if mode!='3':
        call_count = int(input("how many times call? : "))
    call_cut_duration = int(input("call duration ? "))
    shutdown = input("shutdown autometically(y/n)? ")

    stop_until_time(t, m)

    if mode=='1':
        for i in range(call_count):
            call_action(phone_number, call_cut_duration)

    if mode=='3':
        while True:
            call_action(phone_number, call_cut_duration)

    if shutdown.lower()=='y':
        shutdown_devices()


if mode=='2':
    shutdown = input("shutdown autometically(y/n)? ")
    
    stop_until_time(t, m)

    stop_calling = False
    while True:
        subprocess.run(f"adb shell am start -a android.intent.action.CALL -d tel:{phone_number}", shell=True)
        time.sleep(2)
        for i in range(29):
            with open("call_status.txt", 'w') as file:
                subprocess.run("adb shell dumpsys telephony.registry | grep mCallState",stdout=file, shell=True)
            with open("call_status.txt", 'r') as file:    
                call_state = file.readline().strip()
            if call_state == 'mCallState=0':
                stop_calling = True
                break
            time.sleep(0.9)
        if stop_calling==True:
            print("\n\nshe HUNG UP the call !!!!\n")
            break
        subprocess.run("adb shell input keyevent KEYCODE_ENDCALL", shell=True)
        time.sleep(3)

    if shutdown.lower()=='y':
        shutdown_devices()
    

    