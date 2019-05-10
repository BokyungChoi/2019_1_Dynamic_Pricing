import pandas as pd
import os 
import re
from datetime import datetime

os.chdir(r'C:\DATA\L.point2019\data')
os.listdir()

Session = pd.read_csv(r'C:\DATA\L.point2019\data\Session.csv')
Pruduct = pd.read_csv(r'C:\DATA\L.point2019\data\Pruduct.csv')
Custom = pd.read_csv(os.listdir()[0])
Master = pd.read_csv(os.listdir()[1])
Search1 = pd.read_csv(os.listdir()[3])
Search2 = pd.read_csv(os.listdir()[4])


# Session과 pruduct의 고유한 키값이 동일하다. 
# pruduct에 포함되지 않지만 Session에는 포함되는 데이터가 있으면 Session의 고유한 키값이 더 많아야한다. 

#%% data Cleansing & preprocessing
Session = pd.read_csv(r'C:\DATA\L.point2019\data\Session.csv')
Pruduct = pd.read_csv(r'C:\DATA\L.point2019\data\Pruduct.csv')

# 브랜드 이름에서 [],() 기호 제거.
Pruduct['PD_BRA_NM'] = list(map(lambda x:re.sub("[[,\](,)\s]", "",x),Pruduct['PD_BRA_NM']))

# 구매가격 변수를 str -> int 변환.
Pruduct['PD_BUY_AM'] = list(map(lambda x:x.replace(",",""),Pruduct['PD_BUY_AM']))
Pruduct['PD_BUY_AM'] = Pruduct['PD_BUY_AM'].astype(int)

# 구매개수 변수를 str&int -> int로 변환.
Pruduct['PD_BUY_CT'] = Pruduct['PD_BUY_CT'].astype(str)
Pruduct['PD_BUY_CT'] = list(map(lambda x:x.replace(",",""),Pruduct['PD_BUY_CT']))
Pruduct['PD_BUY_CT'] = Pruduct['PD_BUY_CT'].astype(int)

# SESS_DT을 월, 주, 요일로 변환. 
Session['SESS_DT'] = Session['SESS_DT'].astype(str) # int object is not subsriptable 
Session['SESS_DT'] = list(map(lambda x:x[0:4] +'-'+x[4:6]+'-'+x[6:8],Session['SESS_DT']))
Session['MONTH'] = list(map(lambda x:x[5:7],Session['SESS_DT']))

## 월요일을 기준으로 2018-04-02은  04-02 ~ 04-08에 해당. 
Session['WEEK'] = list(map(lambda x:datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%U-1'),Session['SESS_DT'])) 
Session['WEEK'] = list(map(lambda x:datetime.strptime(x, '%Y-%U-%w').strftime('%Y-%m-%d'),Session['WEEK'])) 

## 0 = 월요일, 6 = 일요일
Session['DAY'] = list(map(lambda x:datetime.strptime(x, '%Y-%m-%d').weekday(),Session['SESS_DT'])) 

## HOLLY DAY도 추후 만듭시다 ㅎㅎ 

# merge
raw = pd.merge(Pruduct,Custom, how = 'left', on = ['CLNT_ID']) 
raw = pd.merge(raw,Master, how = 'left', on = ['PD_C']) 
raw = pd.merge(raw,Session, how = 'left', on = ['CLNT_ID','SESS_ID']) 

