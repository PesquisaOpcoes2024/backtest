# é necessário rodar primeiro o comando 'pip install Metatrader5'
# é também necessário criar um arquivo de texto na pasta que possua 
# o login do MetaTrader5 na primeira linha e a senha na segunda
# %%
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import csv

filename = 'trade.csv'
f = csv.writer(open(filename, 'w', newline=''))
f.writerow(['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real'])

login, password = open('credentials.txt').read().split()
mt5.initialize(login=int(login), password=password, server='mt5.xpi.com.br:443')

#ticks
ticks = mt5.copy_ticks_range(
    'PETR4',
    datetime(2024, 5, 1),
    datetime(2024, 6, 1), 
    #extremamente importante se atentar a essas datas selecionadas
    mt5.COPY_TICKS_TRADE
)

df_ticks = pd.DataFrame(ticks)
df_ticks["time"]=pd.to_datetime(df_ticks["time"], unit='s')
df_ticks["time_msc"]=pd.to_datetime(df_ticks["time"], unit='s')
#print(df_ticks)


for index, row in df_ticks.iterrows():
    time = row["time"]
    bid = row["bid"]
    ask = row["ask"]
    last = row["last"]
    volume = row["volume"]
    time_msc = row["time_msc"]
    flags = row["flags"]
    volume_real = row["volume_real"]
    #print(f"Time: {time}, Bid: {bid}")
    f.writerow([time, bid, ask, last, volume, time_msc, flags, volume_real])

#for index, row in df_ticks.iterrows():
#    f.writerow([row["time"], row["bid"], row["ask"], row["last"], row["volume"], row["time_msc"], row["flags"], row["volume_real"]])

#bid_example = df_ticks.iloc[0]['bid']
#print("BID TESTE: " + str(bid_example))
print("Dados exportados para trade.csv")
# %%
