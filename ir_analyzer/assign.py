#coding: utf-8

class Symbol_assignment():
	def __init__(self, ir_num = 16):
		self.ir_num = ir_num
		self.switch = 0
	
	def symbol_assignment(self, pitch1, pitch2, pitch3):
		if(self.ir_num == 16):
			return self.ir_16(pitch1, pitch2, pitch3)
		elif(self.ir_num == 8):
			return self.ir_8(pitch1, pitch2, pitch3)
		else:
			print("ERROR: set 16 or 8 for num_of_symbols")
			exit()
	
	def ir_8(self, pitch1, pitch2, pitch3, threshold = 7):		   
		up = (pitch2- pitch1) #これが正か負か
		self.threshold = threshold
		
		P_w = self._pitch_width(pitch1, pitch2, pitch3, self.threshold) 
		S_d = self._same_direction(pitch1, pitch2, pitch3)
		pid = self._PID(pitch1, pitch2, pitch3, self.threshold)
		prd = self._PRD(pitch1, pitch2, pitch3, self.threshold)
		
		#print(P_w, S_d, pid, prd)
		#P_u: 0, D:1 , R_u:2, IP_u:3,	   VP_u:4,	 IR_u:5,	 VR_u:6,	 ID_u:7
		#P_d: 8,		  R_d: 9, IP_d: 10,   VP_d: 11, IR_d: 12,   VR_d: 13,   ID_d: 14, other: 15
		pattern = "NO"
		if(P_w == "00" and S_d == "yes" and pid == "yes" and prd == "yes"):
			return 1 #"D"
		elif(P_w == "SS(=)" and S_d == "no" and pid == "yes" and prd == "no"):
			return 7
		elif(P_w == "SS" or P_w == "SS(=)"):
			if(S_d == "yes" and pid == "yes" and prd == "yes"):
				return 0
			elif(S_d == "no" and pid == "yes" and prd == "no"):
				return 3
		elif(P_w == "SL" and S_d == "yes" and pid == "no" and prd == "yes"):
			return 4
		elif(P_w == "SL" and S_d == "no" and pid == "no" and prd == "no"):
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)
		elif(P_w == "LS" and S_d == "yes" and pid == "yes" and prd == "no"):
			return 5
		elif(P_w == "LS" and S_d == "no" and pid == "yes" and prd == "yes"):
			return 2 #R
		elif(P_w == "LL" and S_d == "yes" and pid == "no" and prd == "no"):
			#return 8#15 #"-"
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)
		elif(P_w == "LL" and S_d == "no" and pid == "no" and prd == "yes"):
			return 6 #VR
			
		if(P_w == "SL" and S_d == "no" and pid == "no" and prd == "no"):
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)#8#15 #"-"
		elif(P_w == "LL" and S_d == "yes" and pid == "no" and prd == "not"):
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)#8#15 #"-"
		else:
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)

	def ir_16(self, pitch1, pitch2, pitch3, threshold = 7):		   
		up = (pitch2- pitch1) #これが正か負か
		self.threshold = threshold
		
		P_w = self._pitch_width(pitch1, pitch2, pitch3, self.threshold) 
		S_d = self._same_direction(pitch1, pitch2, pitch3)
		pid = self._PID(pitch1, pitch2, pitch3, self.threshold)
		prd = self._PRD(pitch1, pitch2, pitch3, self.threshold)
		
		#print(P_w, S_d, pid, prd)
		#P_u: 0, D:1 , R_u:2, IP_u:3,	   VP_u:4,	 IR_u:5,	 VR_u:6,	 ID_u:7
		#P_d: 8,		  R_d: 9, IP_d: 10,   VP_d: 11, IR_d: 12,   VR_d: 13,   ID_d: 14, other: 15
		pattern = "NO"
		if(P_w == "00" and S_d == "yes" and pid == "yes" and prd == "yes"):
			return 1 #"D"
		elif(P_w == "SS(=)" and S_d == "no" and pid == "yes" and prd == "no"):
			if(up > 0): #ID
				return 7
			else:
				return 14
		elif(P_w == "SS" or P_w == "SS(=)"):
			if(S_d == "yes" and pid == "yes" and prd == "yes"):
				if(up > 0): #P
					return 0
				elif(up<0):
					return 8
							
			elif(S_d == "no" and pid == "yes" and prd == "no"):
				if(up >= 0): #IP
					return 3
				elif(up <= 0):
					return 10
		elif(P_w == "SL" and S_d == "yes" and pid == "no" and prd == "yes"):
				if(up > 0): #VP
					return 4
				elif(up < 0):
					return 11
		elif(P_w == "SL" and S_d == "no" and pid == "no" and prd == "no"):
			#return 8#15 #"-"
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)
		elif(P_w == "LS" and S_d == "yes" and pid == "yes" and prd == "no"):
			if(up > 0): #IR
				return 5
			elif(up < 0):
				return 12

		elif(P_w == "LS" and S_d == "no" and pid == "yes" and prd == "yes"):
			if(up > 0): #R
				return 2
			elif(up < 0):
				return 9

		elif(P_w == "LL" and S_d == "yes" and pid == "no" and prd == "no"):
			#return 8#15 #"-"
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)
		elif(P_w == "LL" and S_d == "no" and pid == "no" and prd == "yes"):
			if(up > 0): #VR
				return 6
			elif(up < 0):
				return 13

		if(P_w == "SL" and S_d == "no" and pid == "no" and prd == "no"):
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)#8#15 #"-"
		elif(P_w == "LL" and S_d == "yes" and pid == "no" and prd == "not"):
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)#8#15 #"-"
		else:
			return self._reccuresive(pitch1, pitch2, pitch3, self.threshold)

	
	def _reccuresive(self, pitch1, pitch2, pitch3, threshold):
		#print(threshold)
		#print(pitch1, pitch2, pitch3[1]- pitch1, pitch2, pitch3[0], pitch1, pitch2, pitch3[2]-pitch1, pitch2, pitch3[1])
		if(self.switch == 0):
			threshold = 0
			self.switch = 1
			
		if(self.threshold < 100):
			#print("========", threshold)
			if(self.ir_num == 16):
				tmp = self.ir_16(pitch1, pitch2, pitch3, threshold+1)
			else:
				tmp = self.ir_8(pitch1, pitch2, pitch3, threshold+1)
			#print(tmp)
		else:
			tmp = 8
		self.switch = 0
		return tmp#8#15 #"?"
		

	#Return L or S
	def _ReturnLorS(self, pitch1, pitch2, threshold):
		if(abs(pitch1 - pitch2)  == 0):
			return 0
		if(abs(pitch1 - pitch2)  >= threshold):
			return "L"
		if(abs(pitch1 - pitch2)  < threshold):
			return "S"
		return "OTHER"

	#同方向
	def _same_direction(self, pitch1, pitch2, pitch3):
		d1 = pitch2 - pitch1
		d2 = pitch3 - pitch2

		if(d1 == 0 and d2 == 0):
			return "yes"
		elif(d1*d2 >= 0):
			return "yes"
		else:
			return "no"

	#音程の大きさ
	def _pitch_width(self, pitch1, pitch2, pitch3, threshold):
		if(pitch1 == pitch2 and pitch2 == pitch3):
			return "00"
		elif(abs(pitch1 - pitch2)  == abs(pitch2-pitch3) and abs(pitch1 - pitch2) < threshold):
			return "SS(=)"
		elif(abs(pitch1 - pitch2)  < threshold and abs(pitch2 - pitch3)  < threshold):
			return "SS"
		elif(abs(pitch1 - pitch2)  < threshold and abs(pitch2 - pitch3)  >= threshold):
			return "SL"
		elif(abs(pitch1 - pitch2)  >= threshold and abs(pitch2 - pitch3)  < threshold):
			return "LS"
		elif(abs(pitch1 - pitch2)  >= threshold and abs(pitch2 - pitch3)  >= threshold):
			return "LL"
		else:
			return "TheOtherPattern"


	def _PID(self, pitch1, pitch2, pitch3, threshold):
		if(self._ReturnLorS(pitch1, pitch2, threshold) == "S" or self._ReturnLorS(pitch1, pitch2, threshold) == 0):
			if(abs(abs(pitch2 - pitch3) - abs(pitch1 - pitch2)) <=4):
				return "yes"
			else:
				#print("aaaa", abs(pitch2 - pitch3),  abs(pitch1 - pitch2))
				return "no"
		if(self._ReturnLorS(pitch1, pitch2, threshold) == "L" and abs(pitch1 - pitch2)  > abs(pitch2 - pitch3) ):
			return "yes"
		else:
			return "no"

	#6半音のときエラーが出るかも
	def _PRD(self, pitch1, pitch2, pitch3, threshold):
		if(self._ReturnLorS(pitch1, pitch2, threshold) == "S" or self._ReturnLorS(pitch1, pitch2, threshold) == 0):
			if(self._same_direction(pitch1, pitch2, pitch3) == "yes"):
				return "yes"
			else:
				return "no"
		elif(self._ReturnLorS(pitch1, pitch2, threshold) == "L" and self._same_direction(pitch1, pitch2, pitch3) == "no"):
			return "yes"
		else:
			return "no"
