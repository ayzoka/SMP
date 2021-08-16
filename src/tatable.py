import pandas as pd
import pandas_ta as ta

def tatable(stock_name,talist):
	df=pd.read_csv('./Data/'+str(stock_name)+'.csv')
	for x in talist:
		df = pd.concat([df, eval('df.ta.'+str(x)+'()')], axis=1)
	df.fillna(0,inplace=True)
	df.drop(['Unnamed: 0','timestamp', 'close', 'low', 'high', 'open'], inplace=True, axis=1)
	return df