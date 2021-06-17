#coding: utf-8
import numpy as np
from ir_analyzer import assign
import copy

class IR_analyser():
	def __init__(self, ir_num = 16):
		self.S_a = assign.Symbol_assignment(ir_num)
		
	def is_closure(self, pitch, duration):
		#IOI表現に変更
		IOI_pitch = []
		IOI_duraiton = []
		tmp_duration = 0
		integrated_rests = []
		for i in range(len(pitch)):
			if(pitch[i] == -1 and tmp_duration >= duration[i]):
				IOI_duraiton[-1] += duration[i]
				#消えた人たちを保存
			else:
				IOI_pitch.append(pitch[i])
				IOI_duraiton.append(duration[i])
				
			tmp_duration = duration[i]
		
		#print(IOI_pitch)
		#print(IOI_duraiton)
		closure_index = []
		for i, _duration in enumerate(IOI_duraiton):
			if(i > 0 and IOI_pitch[i] > 0):
				if(tmp__duration*2.0 <= _duration):
					closure_index.append(i)
			tmp__duration = _duration
		
		if(pitch[0] == -1):
			closure_index = np.array(closure_index)-1
			
		return closure_index
	
	#シンボル付与
	def ir_analysis_main(self, pitch, integrated_features, closure_index, maximum_sumbol_num = 2, use_beat = True, symbol_num = 16, beat_strength = 1.0):
		#データをとりあえず、クロージャ位置で分割
		closure_devided_features, closure_devided_index = self._split_features_on_closure(integrated_features, closure_index)
		symbol_matrix, symbol_start_matrix = self._assign_ir_symbol(pitch, closure_devided_features, closure_devided_index, symbol_num, maximum_sumbol_num)
		distance_from_symbol_start_note = self._distance_from_symbol_start_note(symbol_matrix, symbol_start_matrix)
		self._marge_symbol(distance_from_symbol_start_note, symbol_start_matrix)
		#print(distance_from_symbol_start_note)
		
		return symbol_matrix, symbol_start_matrix
		
	#シンボル付与
	def _assign_ir_symbol(self, pitch, closure_devided_features, closure_devided_index, symbol_num, maximum_sumbol_num):
		#分析結果を入れる行列
		symbol_matrix = np.zeros((len(pitch),  symbol_num))
		symbol_start_matrix =  np.zeros((len(pitch),  symbol_num))

		for i, x in enumerate(closure_devided_features):
			#特徴量の値に基づきソート
			for j in np.argsort(-np.array(x)):
				#クロージャを跨ぐ音符へのシンボル付与を避ける
				if(len(x) -2 >  j):
					#最大付与数よりも小さい場合
					#print(i, j)
					_index = closure_devided_index[i][j]
					if(np.sum(symbol_matrix[_index]) < maximum_sumbol_num and np.sum(symbol_matrix[_index+1]) < maximum_sumbol_num and np.sum(symbol_matrix[_index+2]) < maximum_sumbol_num):
						#symbol assignment
						#print(_index)
						pitch1 = pitch[_index]
						pitch2 = pitch[_index+1]
						pitch3 = pitch[_index+2]
						
						ir_symbol = self.S_a.symbol_assignment(pitch1, pitch2, pitch3)
						symbol_matrix[_index][ir_symbol] = 1
						symbol_matrix[_index+1][ir_symbol] = 1
						symbol_matrix[_index+2][ir_symbol] = 1
						
						symbol_start_matrix[_index][ir_symbol] = 1

		return symbol_matrix, symbol_start_matrix 
	 
	#割り振られたシンボルにおける相対的な位置 
	def _distance_from_symbol_start_note(self, symbol_matrix, symbol_start_matrix):
		from_start_note = []#np.array(symbol_matrix.shape)
		for i in range(len(symbol_matrix.T)):
			tmp = self._count_num(symbol_matrix.T[i], symbol_start_matrix.T[i])
			from_start_note.append(tmp)
		return np.array(from_start_note).T
	
	#4音以上連続するP、もしくはDを1つのシンボルとみなす
	def _marge_symbol(self, symbol_matrix, symbol_start_matrix):
		#if(symbol_matrix.shape[1] == 16):
			#print(symbol_matrix.T[0])
			#print(symbol_matrix.T[1])
			#print(symbol_matrix.T[8])
			#print("aaa")
		pass
		
	#4音以上からなるPとDを拍に基づき分割
	def _split_by_beat(self, symbol_matrix, symbol_start_matrix, beat, symbol_num):
		pass
		
	#クロージャで分割
	def _split_features_on_closure(self, integrated_features, closure_index):
		closure_devided_features = []
		closure_devided_index = []
		splited_features = []
		splited_index = []
		#これがよくわからない
		
		
		
		for i, value in enumerate(integrated_features):
			if(i in closure_index or i == len(integrated_features)-1):
				splited_features.append(value)
				splited_index.append(i)
				closure_devided_features.append(splited_features)
				closure_devided_index.append(splited_index)
				
				splited_features = [value]
				splited_index = [i]
			else:
				splited_features.append(value)
				splited_index.append(i)
			#closure_devided_features.append(splited_features)
			#closure_devided_index.append(splited_index)
		return closure_devided_features, closure_devided_index
		
	#dirty code
	def _count_num(self, a, b):
		a = list(a)
		b = list(b)
		tmp = copy.copy(a)
		tmp.append(0)
		
		endnote1 =[i for i, x in enumerate(np.diff(tmp)) if x == -1]
		tmp_endnote = [i-1 for i, x in enumerate(b) if i>0 and x==1]
		endnote2 = [i for i in tmp_endnote if a[i] == 1]
		startnote= [i for i, x in enumerate(b) if x==1]
		endnote = endnote1
		endnote.extend(endnote2)
		endnote = sorted(endnote)
		
		count_list = []
		count = 0
		s_pointer = 0
		e_pointer = 0
		for i in range(len(a)):
			if(i in startnote):
				count = 1
			elif(i-1 in endnote):
				count = 0
			elif(a[i] == 1):
				count += 1
			count_list.append(count)
		return count_list