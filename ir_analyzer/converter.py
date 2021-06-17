#coding: utf-8
import pickle
import os
import numpy as np
#入力をなんか知らんがシンボル
#それらを一個づつindexで管理
#エンコード、および、デコードができる


class convert():
	convert_dict = {}
	index = 0
	def __init__(self):
		#なんか書く？(すでにあるパターンならそれを使う的な)
		if(os.path.exists("./pattern_list_in.pickle") is True):
			print("read!")
			self.pattern_list_in = self.pickle_load("./pattern_list_in.pickle")					
			self.index = len(self.pattern_list_in)

	
	def encode(self, sequence):
		tmp = []
		for i in sequence:	
			if(i in self.convert_dict.values()):#見たことあったら
				pass
			else: #なかったら
				self.convert_dict[self.index] = i
				self.index = self.index + 1
			key = [k for k, v in self.convert_dict.items() if v == i]
			tmp.append(key[0])
			#これでエンコード完了
		return tmp
	
	#変換済みのものを入力とする
	def decode(self, sequence):
		tmp = []
		for i in sequence: 
			tmp.append(self.convert_dict[i])
		return tmp

"""
sample = convert()
print(sample.encode(["あ", "ん", "ぱ", "ん", "ま", "ん"]))
sample.decode([0, 1, 2, 1, 3, 1])
"""