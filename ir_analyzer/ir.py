#coding: utf-8
from ir_analyzer import make_data
from ir_analyzer import analysis
from ir_analyzer import conditional_probability as CP
import numpy as np
import matplotlib.pyplot as plt

class IR_main():
	#使用するルールを決定
	def __init__(self, beat = 1.0, use_beat = True, use_training_data = True, use_closure = True, maximum_sumbol_num = 2, num_of_symbols = 16):
		self.boundary = beat
		self.use_beat = use_beat
		self.use_training_data = use_training_data
		self.use_closure = use_closure
		self.maximum_sumbol_num = maximum_sumbol_num
		self.makedata = make_data.Data()
		self.ir_analysis = analysis.IR_analyser(num_of_symbols)
		self.c_p = CP.conditional_P()

	
	#inputをpitchと音価とビートにしてしまう方が良い説
	def ir_main(self, file_name):
		onset, pitch, duration, beat, integrated_rests =  self._get_features(file_name)
		
		#クロージャ推定
		closure_index = self.ir_analysis.is_closure(pitch, duration)
		
		#休符を削除
		_onset, _pitch, _duration, _beat, rest_index = self._pop_rest(onset, pitch, duration, beat)
		#print("onset")
		#print(_pitch)
		#音高遷移の学習
		c_p = CP.conditional_P()
		training_data = [[_onset, _pitch, _duration, _beat]]
		c_p.learn_model(training_data) 
		likelihood_list = c_p.calc_model([_onset, _pitch, _duration, _beat])#, integrated_rests) 
		likelihood_list = np.exp(likelihood_list)
		#ビートと音高遷移を統合
		integrated_features = np.array((likelihood_list)/np.max(np.abs(likelihood_list)) + np.array(_beat))
		
		#シンボル付与
		#print(closure_index)
		symbols, symbol_start_notes, distance_from_symbol_start_note = self.ir_analysis.ir_analysis_main(_pitch, integrated_features, closure_index, maximum_sumbol_num = self.maximum_sumbol_num)
		
		#シンボル開始音からの距離
		
		#休符を復元
		symbols = self._insert_rests(symbols, rest_index, integrated_rests)
		symbol_start_notes = self._insert_rests(symbol_start_notes, rest_index, integrated_rests)
		distance_from_symbol_start_note = self._insert_rests(distance_from_symbol_start_note, rest_index, integrated_rests)
		
		onset, pitch, duration, beat = self.makedata.make_data(file_name)
		return symbols, symbol_start_notes, onset, pitch, duration, beat, closure_index, distance_from_symbol_start_note

		
	#連続する休符を1つにまとめる（MIDIを入力とする場合には不要）
	def _get_features(self, file_name):
		onset, pitch, duration, beat = self.makedata.make_data(file_name)
		onset, pitch, duration, beat, integrated_rests = self._integrate_rests(onset, pitch, duration, beat)
		return onset, pitch, duration, beat, integrated_rests
	
	#休符を除去する(IR分析の対象外なので)
	def _pop_rest(self, onset, pitch, duration, beat):
		rest_index = []
		for i, x in enumerate(pitch):
			if(x == -1):
				rest_index.append(i)
		
		dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
		return dellist(onset, rest_index), dellist(pitch, rest_index), dellist(duration, rest_index), dellist(beat, rest_index), rest_index
	
	#plot
	def plot_ir(self, start, end, symbols, pitch):
		fig, ax1 = plt.subplots()
		colorlist = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#e41a1c', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', "b"]
		ax1.plot(pitch[start: end]) 
		ax2 = ax1.twinx()
		if(symbols.shape[1] == 16):
			plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], ["P(up)", "D", "R(up)", "IP(up)", "VP(up)", "IR(up)", "VR(up)", "ID(up)", "P(down)", "R(down)", "IP(down)", "VP(down)", "IR(down)", "VR(down)", "ID(down)"])
		else:
			plt.yticks([0, 1, 2, 3, 4, 5, 6, 7], ["P", "D", "R", "IP", "VP", "IR", "VR", "ID"])
		tmp_ = 0
		for i in symbols[start:end].T:
			count_ = 0
			for j in i:
				if(j >= 1):
					ax2.scatter(count_, j*tmp_, color = colorlist[tmp_], marker = "X")
				count_ =  count_ + 1
			tmp_ = tmp_+1
		#ax1.title.set_text(text + name)
		plt.show()
		
	#消えてしまった全ての休符を復元
	def _insert_rests(self, matrix, rest_index, integrated_rests):
		for i in rest_index:
			matrix = np.insert(matrix, i, -1, axis=0)
		for i in integrated_rests:
			matrix = np.insert(matrix, i, -1, axis=0)
		return matrix
			
	#連続する休符を統合
	def _integrate_rests(self, onset, pitch, duration, beat):
		tmp_pitch = 0
		integrated_rests = []
		integrated_onset = []
		integrated_pitch = []
		integrated_duration = []
		integrated_beat = []
		
		for i in range(len(pitch)):
			if(tmp_pitch == -1 and pitch[i] == -1):
				integrated_duration[-1] += duration[i]
				integrated_rests.append(i)
			else:
				integrated_onset.append(onset[i])
				integrated_pitch.append(pitch[i])
				integrated_duration.append(duration[i])
				integrated_beat.append(beat[i])

			tmp_pitch = pitch[i]
		return integrated_onset, integrated_pitch, integrated_duration, integrated_beat, integrated_rests

"""
#確認用
ir = IR_main(maximum_sumbol_num = 3, num_of_symbols = 16)
symbols, symbol_onsetnotes, onset, pitch, duration, beat = ir.ir_main("pretender.xml")
ir.plot_ir(0, 5000, symbols, pitch)
ir.plot_ir(0, 5000, symbol_onsetnotes, pitch)
"""
