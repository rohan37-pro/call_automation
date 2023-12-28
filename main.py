import subprocess
import time
from datetime import datetime
import pytz
from random import randint


phone_number = input("phone number? ")
t = int(input("enter hour: "))
m = int(input("enter minute : "))
call_count = int(input("how many times call? : "))
call_cut = int(input("call duration ? "))
cut = input("stop when she cut(y/n)? : ")
shutdown = input("shutdown autometically(y/n)? ")

zone = pytz.timezone("Asia/Kolkata")
n = datetime.now(zone).timetuple()
while n.tm_hour < t and m < n.tm_min:
    time.sleep(30)
    n = datetime.now(zone).timetuple()

ver = ''
for i in range(call_count):
    subprocess.run(f"adb shell am start -a android.intent.action.CALL -d tell:{phone_number}", stdout=ver, shell=True)
    print(f"ver is {ver}")
    time.sleep(randint(call_cut, call_cut+10))
    subprocess.run("adb shell input keyevent KEYCODE_ENDCALL")
    