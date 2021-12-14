import sys

class CPU:
	def __init__(self, inp):
		self.mem = []
		self.readMem(inp)
		self.regs = [0]*8
		self.stack = []
		self.ptr = 0
		self.done = False
		self.inputq = []
		self.output = ""
	def readMem(self, inp):
		with open(inp, mode='rb') as f:
			read = f.read(2)
			while read:
				self.mem.append(int.from_bytes(read, "little"))
				read = f.read(2)
	def read(self, ptr):
		return self.parseNum(self.mem[ptr])
	def readArg(self, offset):
		return self.read(offset+self.ptr)

	def write(self, ptr, val):
		assert(32768<=self.mem[ptr]<32776)
		self.regs[self.mem[ptr]-32768] = val


	def parseNum(self, num): #return parsed number input
		if num<32768:
			return num
		if num<32776:
			return self.regs[num-32768]
		raise Exception("invalid input")
	
	def run(self, debug=False):
		while not self.done:
			# if self.readArg(0) == 20:
			# 	debug = True
			if debug:
				print("PTR: ",self.ptr)
				print("    MEM: ",[x if x<32768 else f"r{x-32768}" for x in self.mem[self.ptr:self.ptr+4]])
			self.step()
			if debug:
				print("    REGS:",self.regs)
				print("    STACK:",self.stack)

	def push(self, val):
		self.stack.append(val)
	def pop(self):
		return self.stack.pop(-1)

	def step(self):
		opc = self.mem[self.ptr]
		match opc:
			case 0:
				self.done = True
			case 1:
				self.write(self.ptr+1, self.readArg(2))
				self.ptr+=3
			case 2:
				self.push(self.readArg(1))
				self.ptr+=2
			case 3:
				self.write(self.ptr+1, self.pop())
				self.ptr+=2
			case 4:
				self.write(self.ptr+1, 1 if (self.readArg(2)==self.readArg(3)) else 0) 
				self.ptr+=4
			case 5:
				self.write(self.ptr+1, 1 if (self.readArg(2)>self.readArg(3)) else 0) 
				self.ptr+=4
			case 6:
				self.ptr=self.readArg(1)
			case 7:
				if self.readArg(1):
					self.ptr=self.readArg(2)
				else:
					self.ptr+=3
			case 8:
				if self.readArg(1) == 0:
					self.ptr=self.readArg(2)
				else:
					self.ptr+=3
			case 9:
				self.write(self.ptr+1, (self.readArg(2)+self.readArg(3))%32768) 
				self.ptr+=4
			case 10:
				self.write(self.ptr+1, (self.readArg(2)*self.readArg(3))%32768)
				self.ptr+=4
			case 11:
				self.write(self.ptr+1, (self.readArg(2)%self.readArg(3))%32768) 
				self.ptr+=4
			case 12:
				self.write(self.ptr+1, (self.readArg(2)&self.readArg(3)))
				self.ptr+=4
			case 13:
				self.write(self.ptr+1, (self.readArg(2)|self.readArg(3)))
				self.ptr+=4
			case 14:
				self.write(self.ptr+1, self.readArg(2)^0x7FFF)
				self.ptr+=3
			case 15:
				self.write(self.ptr+1, self.mem[self.readArg(2)])
				self.ptr+=3
			case 16:
				self.mem[self.readArg(1)] = self.readArg(2)
				self.ptr+=3
			case 17:
				self.push(self.ptr+2)
				self.ptr = self.readArg(1)
			case 18:
				p = self.pop()
				if p != None:
					self.ptr = p
				else:
					self.done = True
			case 19:
				print(chr(self.readArg(1)),end="")
				self.output += chr(self.readArg(1))
				self.ptr+=2
			case 20:
				while len(self.inputq)==0:
					self.inputq = list(input(">")+"\n")
				self.write(self.ptr+1, ord(self.inputq.pop(0)))
				self.ptr+=2
			case 21:
				self.ptr+=1
			case _:
				print("UNKNOWN OPC")
				print(self.mem[self.ptr])
				raise Exception("unknown opc")