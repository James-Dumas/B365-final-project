import json, pandas as pd, numpy as np, statistics as stat
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
    finalPrice = f[i]['bids'][len(f[i]['bids'])-1]['price']
    bidders = f[i]['bidders']
    duration = f[i]['duration']
    prices, times = [], []
    prices += [f[i]['start_price']]
    times += [timeNormal(f[i]['start_time'])]
    for j in range(len(f[i]['bids'])):
        prices += [f[i]['bids'][j]['price']]
        times += [timeNormal(f[i]['bids'][j]['time'])]
    priceDif = np.diff(prices)
    timeDif = [x.total_seconds() for x in np.diff(times)]
    priceDifMean = stat.mean(priceDif)
    priceDifSd = stat.stdev(priceDif) if len(priceDif) > 1 else 0
    timeDifMean = stat.mean(timeDif)
    timeDifSd = stat.stdev(timeDif) if len(timeDif) > 1 else 0
    return np.array([[finalPrice,bidders,duration,priceDifMean,priceDifSd,timeDifMean,timeDifSd]])

f = open('data/scraped/out_2021-11-28_03-28-13.json')
sales = json.load(f)

data = createRow(sales,0)
for i in range(1,len(sales)): 
    data = np.vstack([data,createRow(sales,i)])
df = pd.DataFrame(data,columns=['Final Price','Bidders','Duration','Price Dif Mean','Price Dif SD','Time Dif Mean','Time Dif SD'])
print(df)