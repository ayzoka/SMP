import pandas as pd
import numpy as np 
import math
from tatable import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM

# FUNCTION TO CREATE 1D DATA INTO TIME SERIES DATASET
# THIS FUNCTION CAN BE USED TO CREATE A TIME SERIES DATASET FROM ANY 1D ARRAY
def new_dataset(dataset,ta_ind, step_size):
	data_X, data_Y = [], []
	for i in range(len(dataset)-step_size-1):
		a = dataset[i:(i+step_size), :]
		a = np.concatenate((a,ta_ind[i:(i+step_size), :]), axis=-1)
		data_X.append(a)
		data_Y.append(dataset[i + step_size, :])
	return np.array(data_X), np.array(data_Y),


def evaluate(stock_name, talist):
	# FOR REPRODUCIBILITY
	np.random.seed(7)

	# IMPORTING DATASET
	dataset = pd.read_csv('./Data/'+str(stock_name)+'.csv', usecols=[1, 2, 3, 4])
	df = tatable(stock_name, talist)
	df=df.reindex(index=df.index[::-1])
	dataset = dataset.reindex(index=dataset.index[::-1])

	# TAKING DIFFERENT INDICATORS FOR PREDICTION
	OHLC_avg = dataset.mean(axis=1)

	# PREPARATION OF TIME SERIES DATASE
	OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg), 1))  # 1664
	scaler = MinMaxScaler(feature_range=(0, 1))
	OHLC_avg = scaler.fit_transform(OHLC_avg)
	scaler_ta=MinMaxScaler(feature_range=(0,1))
	df_ta=scaler_ta.fit_transform(df)
	# TRAIN-TEST SPLIT
	train_OHLC = int(len(OHLC_avg) * 0.75)
	x=int(len(OHLC_avg) * 0.75)
	test_OHLC = len(OHLC_avg) - train_OHLC
	train_OHLC, test_OHLC = OHLC_avg[0:train_OHLC,
									:], OHLC_avg[train_OHLC:len(OHLC_avg), :]
	train_ta, test_ta = df_ta[0:x, :], df_ta[x:len(OHLC_avg),:]
	# TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
	trainX, trainY = new_dataset(train_OHLC,train_ta, 1)
	testX, testY = new_dataset(test_OHLC,test_ta, 1)
	# RESHAPING TRAIN AND TEST DATA
	trainX = np.reshape(trainX, (trainX.shape[0], 4, trainX.shape[1]))
	testX = np.reshape(testX, (testX.shape[0], 4, testX.shape[1]))
	step_size = 1
	testY=np.reshape(testY,(-1))
	trainY = np.reshape(trainY, (-1))


	# LSTM MODEL
	model = Sequential()
	model.add(LSTM(32, input_shape=(4, step_size), return_sequences=True))
	model.add(LSTM(16))
	model.add(Dense(1))
	model.add(Activation('linear'))

	# MODEL COMPILING AND TRAINING
	# Try SGD, adam, adagrad and compare!!!
	model.compile(loss='mean_squared_error', optimizer='adagrad')
	model.fit(trainX, trainY, epochs=5, batch_size=1, verbose=2)

	# PREDICTION
	trainPredict = model.predict(trainX)
	testPredict = model.predict(testX)

	# DE-NORMALIZING FOR PLOTTING
	trainPredict = scaler.inverse_transform(trainPredict)
	trainY = scaler.inverse_transform([trainY])
	testPredict = scaler.inverse_transform(testPredict)
	testY = scaler.inverse_transform([testY])


	# TRAINING RMSE
	trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))

	# TEST RMSE
	testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
	return [trainScore, testScore]
