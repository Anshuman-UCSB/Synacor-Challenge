from synacor import CPU
import struct


c = CPU("challenge.bin")
# c.mem[321] = 292
while "self-test complete, all tests pass\n\
The self-test completion code is: VefSvEfYlEJe" not in c.output:
	c.step()
print("\n",c.ptr)
# TODO: figure out how to skip self test

# c.run(True)
# for p, v in enumerate(c.mem):
# 	print(str(p)+":", v)
# print(c.regs)