import requests
import pandas as pd
import numpy as np
import json
import datetime

def get_data(symbol):
    cookies = {
        '_ga': 'GA1.2.1084037441.1629279591',
        'ASP.NET_SessionId': 'dq2fo5maa2zofyk3jwhfyvsj',
        '_gid': 'GA1.2.1351672617.1629727710',
        '_gat_gtag_UA_63076930_1': '1',
        'i18next': 'fa',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://dev.tsetmc.com/Loader.aspx?ParTree=151323&i=2400322364771558 ',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('functionType', 'history'),
        ('symbol', symbol),
        ('resolution', '5'),
        # ('from', '1596412800'),
        # ('to', '1629727810'),
    )

    response = requests.get('http://dev.tsetmc.com/tsev2/data/TradingViewInfo.aspx', headers=headers, params=params, cookies=cookies, verify=False)

    string=response.content.decode('utf-8')
    ddata=json.loads(string)
    data=pd.DataFrame(ddata)
 
    return(data)

# get_data().to_csv('rData.csv', sep=',', encoding='utf-8')
# import requests
def get_addres(persian_name):
    cookies = {
        '_ga': 'GA1.2.1084037441.1629279591',
        'ASP.NET_SessionId': 'dq2fo5maa2zofyk3jwhfyvsj',
        '_gid': 'GA1.2.1351672617.1629727710',
        '_gat_gtag_UA_63076930_1': '1',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=9211775239375291',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('skey', persian_name),
    )

    response = requests.get('http://www.tsetmc.com/tsev2/data/search.aspx', headers=headers, params=params, cookies=cookies, verify=False)

   
    return(response.text.split(",")[2])
def read_price(nam_id='34557241988629814',date='20210823'):
    cookies = {
    '_ga': 'GA1.2.1084037441.1629279591',
    'ASP.NET_SessionId': 'dq2fo5maa2zofyk3jwhfyvsj',
    '_gid': 'GA1.2.1351672617.1629727710',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Referer': 'http://cdn.tsetmc.com/History/34557241988629814/20210815',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get('http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceHistory/'+nam_id+'/'+date, headers=headers, cookies=cookies, verify=False)
    string=response.content.decode('utf-8')
    return(pd.DataFrame(json.loads(string)['closingPriceHistory']))
def to_datetime(i):
    #     
    i=i[0]
    # print(i)
    return(datetime.datetime(int(i[:4]),int(i[4:6]),int(i[6:8]),int(i[8:10]),int(i[10:12]),int(i[12:14])))
def find_chart_candle_tresh(time_index,delta):
    res=[0]
    for j in range(1000):
        ee=((time_index-(time_index.iloc[res[-1]]-datetime.timedelta(0,delta)))[0].dt.total_seconds()).abs().argsort()[0]
        if ee==res[-1]:
            break
        else:
            res.append(ee)
    res.append(len(time_index)-2)
    return(res)
def price_to_chart(price,date,time_frame="1h"):
    if time_frame[-1]=="s":
        time_frame=int(time_frame[:-1])
    elif time_frame[-1]=="m":
        time_frame=int(time_frame[:-1])*60
    elif time_frame[-1]=="h":
        time_frame=int(time_frame[:-1])*3600
    elif time_frame[-1]=="D":
        time_frame=int(time_frame[:-1])*3600*14

    pr=price
    tot_vol=price.qTotTran5J
    # time=price.hEven
    # s=np.array(pr.hEven)%100
    # m=(np.array(pr.hEven)%10000-s)/100
    # h=(np.array(pr.hEven)-m*100-s)/10000
    # df=pd.DataFrame()
    # df["h"]=h
    # df["m"]=m
    # df["s"]=s
    # reso=time_frame[-1]

    z=np.array([""]*len(pr))
    z[(pr.hEven//100000==0)]="0"
    time=z+np.array(pr.hEven.astype(str))
    st=date+time##date
    st=st.reshape(-1,1)
    time_index=pd.DataFrame(np.apply_along_axis(to_datetime,1,st))
    res=find_chart_candle_tresh(time_index,time_frame)
    Open=[]
    High=[]
    Low=[]
    Close=[]
    Vol=[]
    index=time_index.iloc[res[1:]]
    for i in range(len(res)-1):
        Close.append(pr.pDrCotVal[res[i]])
        High.append(pr.pDrCotVal[res[i]:res[i+1]].max())
        Low.append(pr.pDrCotVal[res[i]:res[i+1]].min())
        Open.append(pr.pDrCotVal[res[i+1]])
        Vol.append(pr.qTotTran5J[res[i]]-pr.qTotTran5J[res[i+1]])
        
    data_res=pd.DataFrame()
    data_res["date"]=np.array(index)[:,0]
    data_res["Close"]=Close
    data_res["High"]=High
    data_res["Low"]=Low
    data_res["Open"]=Open
    data_res["Vol"]=Vol
    return(data_res.iloc[:-1][::-1])

def histo_data(symb,time_frame="14h",start=None,end=None):
    addres=get_addres(symb)
    dmy=False
    now=datetime.datetime.now().date()
    dmy=time_frame[-1] in "DMY"
    if dmy:
        r_time_frame=time_frame
        time_frame="14h"
    
        
#     return(DMY(pr))
    if start==None:
        raise("start is empty")
    else:
        start=datetime.date(int(start[:4]),int(start[4:6]),int(start[6:8]))
    if end==None:
        end=now
    else:
        end=datetime.date(int(end[:4]),int(end[4:6]),int(end[6:8]))
    day=start
    pr=pd.DataFrame()
#     print(type(day))
    while day<=end:
        date=str(day).replace("-","")
        new=read_price(addres,date)
        try:
            pr=pr.append(price_to_chart(new,date,time_frame),ignore_index=1)
        except:pass
#         print(new)
        day=day+datetime.timedelta(1,0)
    if dmy:
        return(DMY(pr,r_time_frame))
    return(pr)
        
    
    
    
        
        
def DMY(pr,time_frame):
    if time_frame[-1]=="D":
        time_frame=int(time_frame[:-1])
    elif time_frame[-1]=="M":
        time_frame=int(time_frame[:-1])*30
    elif time_frame[-1]=="y":
        time_frame=int(time_frame[:-1])*12*30
    res=list(np.arange(0,len(pr),time_frame))
    time_index=pr.date
    Open=[]
    High=[]
    Low=[]
    Close=[]
    Vol=[]
    index=time_index.iloc[res[1:]]
    for i in range(len(res)-1):
        Open.append(pr.Open[res[i]])
        High.append(pr.High[res[i]:res[i+1]].max())
        Low.append(pr.Low[res[i]:res[i+1]].min())
        Close.append(pr.Close[res[i+1]])
        Vol.append(pr.Vol[res[i]]+pr.Vol[res[i+1]])
        
    data_res=pd.DataFrame()
    data_res["date"]=np.array(index)[:]
    data_res["Close"]=Close
    data_res["High"]=High
    data_res["Low"]=Low
    data_res["Open"]=Open
    data_res["Vol"]=Vol
    return(data_res.iloc[:-1])
    
    
    
    
        

# if __name__=="__main__":
#     # print(get_addres("ملت"))
#     get_data(get_addres("ذوب")).to_csv('rData.csv', sep=',', encoding='utf-8')
# print(price_to_chart(read_price(get_addres("وبملت"),"20210202"),"20210202",time_frame="1D"))
print(histo_data("ذوب",start="20210810",time_frame="1D"))
