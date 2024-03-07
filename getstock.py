import yfinance as yf
import os
from datetime import date, datetime
from pandas import DataFrame

#Declear today's date and locate the folder
today = str(date.today())
path = os.path.join(str(os.getcwd()), today)

perid = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
interval = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

msft = yf.Ticker("MSFT")
aapl = yf.Ticker("AAPL")
nvda = yf.Ticker("NVDA")
amd = yf.Ticker("AMD")
intel = yf.Ticker("INTC")
goog = yf.Ticker("GOOG")
amzn = yf.Ticker("AMZN")
tsla = yf.Ticker("TSLA")
meta = yf.Ticker("META")

complist = [msft, aapl, nvda, amd, intel, goog, amzn, tsla, meta]


#Print News
def getnews(complist):
    for comp in complist:
        cname = str(comp)[-5:-1]
    
        if "<" in cname:
            cname = cname.replace("<", "")
        fpath = os.path.join(path, cname+".txt")
        news = comp.news
        f = open(fpath, "w")
        print(f"News of {cname}\n")
        f.write(f"News of {cname}\n\n")
        for article in news:
            ts = article['providerPublishTime']
            time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{article['title']}\n{article['publisher']}\n{article['link']}")
            f.writelines(f"{article['title']}\n")
            f.writelines(f"{time}\n")
            f.writelines(f"{article['publisher']}\n")
            f.writelines(f"{article['link']}\n")
            f.writelines("\n")
        print("\n")
    
        f.close()
        comp.get_shares_full(start = "2020-01-01", end = None)

def getprice(p):
    for comp in complist:
        print(comp.history(period=p))

def download(p):
    for comp in complist:
        data = yf.download(str(comp)[-5:-1].replace("<", ""), period = p)
        DataFrame(data).to_csv(os.path.join(path, str(comp)[-5:-1].replace("<", "") + ".csv"))

#Detect if today's News exist
if not os.path.exists(path):

    #Create folder to store news
    os.mkdir(today)

    #Download News as txt
    getnews(complist)

for i in perid:
    print(i)
p = input("Get history data of shares\nEnter the desired period:")
getprice(p)

choice = input("Download as Excel?(y/n): ")
if choice == "y" or choice == "Y":
    download(p)
