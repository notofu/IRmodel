import math
import numpy as np
from ir_analyzer import converter
import matplotlib.pyplot as plt
import copy
import glob


#条件付き確率の計算
class conditional_P():
	X = {} #出現回数
	X_bigram = {} #2-gram
	
	#data_listには(音高, 音価, 発音タイミング (3x音符長)の行列)のリスト
	def learn_model(self, data_list):
		for i in data_list: #ファイル名
			input_list = self.convert_Data(i) #変換するの？
			self._learn(input_list)
	
	#dataには(音高, 音価, 発音タイミング (3x音符長)の行列)
	def calc_model(self, data):
		calc_list = self.convert_Data(data)
		#print(calc_list)
		_calculated = [] #(0, 1, 2)音目
		#print(calc_list)
		#print(len(calc_list))
		for i in range(len(calc_list)-1):
			#print(calc_list[i])
			_calculated.append(self._calc((calc_list[i], calc_list[i+1])))
			
		_calculated.append(-100)
		_calculated.append(-100)
		#print(_calculated)
		return _calculated
	
	def convert_Data(self, data):
		input_list = []
		start_list = data[0]
		pitch_list = data[1]
		duration_list = data[2]
		
		#音程
		Δpitch_list = []
		for i in range(len(pitch_list) -1):
			if(pitch_list[i] == -1): #休符
				Δpitch_list.append(89)
			else:
				Δpitch_list.append(pitch_list[i+1] - pitch_list[i])
		
		#3つに分類
		d_Δpitch_list = []
		for i in Δpitch_list:
			
			if(i == 89):
				d_Δpitch_list.append(0)
			elif(i < 6):
				d_Δpitch_list.append(1)
			else:
				d_Δpitch_list.append(2)
			
			
		#IOIの差 #四捨五入します
		ioi_list = []
		for i in range(len(start_list) -1):
			ioi_list.append(np.round(start_list[i+1] - start_list[i], decimals=1))
		
		#durationの比
		_duration_list = []
		for i in range(len(start_list) -1):
			if(duration_list[i+1] / duration_list[i] <1.4):
				_duration_list.append(1)
			else:
				_duration_list.append(0)

		input_data = [] #入力データ
		
		for i in range(len(d_Δpitch_list)):
			input_data.append(str(d_Δpitch_list[i]))#+str(ioi_list[i]))
			
			#print(d_Δpitch_list[i], ioi_list[i])
		return input_data
			
			
	#ただ数を数えるだけ！
	def _learn(self, input_list):
		#X
		for i in input_list:
			if(i not in self.X):
				self.X[i] = 1
			else:
				self.X[i] += 1
		
		#bi-gram
		tmp_bigram = [(input_list[i], input_list[i+1]) for i in range(len(input_list)-1)] #bi-gram
		for j in tmp_bigram:
			if(j not in self.X_bigram):
				self.X_bigram[j] = 1
			else:
				self.X_bigram[j] += 1
	
	def _calc(self, tuple_):
		tmp1 = sum(self.X.values()) #合計値
		tmp2 = sum(self.X_bigram.values()) #合計値

		#対数
		return math.log(self.X_bigram[tuple_]/tmp2) - math.log(self.X[tuple_[0]]/tmp1)

"""確認用"""
"""
input_ = [1,2,3,4,5,2,3,2,4,6,4,3,4,5,3,3,5,1,4,6,7,4,1,3]
input_ = ["aaa", "sdfa", "asda"]
inputs = []
c_p = conditional_P()
for i in glob.glob('d1/*.mid'):
	inputs.append(i)
	

c_p.learn_model(inputs)
c_p.calc_model(inputs[0])
#print(c_p.calc(("aaa", "sdfa"))) #tupleで入力

c_p = conditional_P()
data_list = ["d1/30029_NoblesSeigneurs.mid"]
c_p.calc_model(data_list[0])
"""