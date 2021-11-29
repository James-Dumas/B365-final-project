import json, pandas as pd, numpy as np
from datetime import datetime

def timeNormal(st):
    #single digit hour
    if st[16] == ':':
        hour = int(st[15])
        if st[22] == 'p':
            hour += 12
        minute = int(st[18]) if st[17] == '0' else int(st[17:19])
        sec = int(st[21]) if st[20] == '0' else int(st[20:22])
    #double digit hour
    else:
        hour = int(st[15:17])
        if st[23] == 'p':
            if hour != 12:
                hour += 12
        else:
            if hour == 12:
                hour = 0
        minute = int(st[19]) if st[18] == '0' else int(st[18:20])
        sec = int(st[22]) if st[21] == '0' else int(st[21:23])
    return datetime(2021,11,int(st[0:2]),hour,minute,sec)

def createRow(f,i):
    bidders = f[i]['bidders']
    duration = f[i]['duration']
    startPrice = f[i]['start_price']
    startTime = timeNormal(f[i]['start_time'])
    sellPrice = f[i]['bids'][len(f[i]['bids'])-1]['price']
    finalBidTime = timeNormal(f[i]['bids'][len(f[i]['bids'])-1]['time'])
    return np.array([bidders,duration,startPrice,startTime,sellPrice,finalBidTime])

f = open('data/scraped/out_2021-11-28_03-28-13.json')
sales = json.load(f)

data = createRow(sales,0)
for i in range(1,len(sales)):
    data = np.vstack([data,createRow(sales,i)])
df = pd.DataFrame(data,columns=['Bidders','Duration','Start Price','Start Time','Sell Price','Final Bid Time'])
print(df)