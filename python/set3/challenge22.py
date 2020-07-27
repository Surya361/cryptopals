import random
import datetime
import time
from mt import MT

def routine() -> int:
    time.sleep(random.randint(40,1000)) 
    mt = MT(int(datetime.datetime.now().strftime("%s")))
    time.sleep(random.randint(40,1000))
    return mt.random()

def guess_seed(startTimeStamp: int, duration: int, prng: int) -> int:
    for i in range(startTimeStamp, startTimeStamp+duration):
        mt = MT(i)
        if mt.random() == prng:
            return i

if __name__ == "__main__":
    #print(routine())
    print(guess_seed(1595770118, 1000,1247227929 ))
    
