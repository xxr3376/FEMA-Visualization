if __name__ == '__main__':
	M = 3
	TSgap = 4
	TSs = [14,21,28]
	I1s = [[4,23,35,71], \
			[4,110,157,203], \
			[4,110,203,332,333,380,362,433]]
	I2s = [[1], \
			[11,1,12,6], \
			[11,29,27,28]]
	I3s = [[[59,32],[31,10],[148,63]], \
			[[59,32],[225,247],[253,247],[150],[71]], \
			[[439,289],[71],[344,293],[345,326],[280,79,120]]]
	TSset,I1set,I2set,I3set = set(),set(),set(),set()
	for TS in TSs: TSset.add(TS)
	for item in I1s:
		for I1 in item: I1set.add(I1)
	for item in I2s:
		for I2 in item: I2set.add(I2)
	for item0 in I3s:
		for item1 in item0:
			for I3 in item1: I3set.add(I3)
	# load timestamp and name
	TS2timestamp = {}
	fr = open('input/mapT','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		TS,timestamp = int(arr[0]),int(arr[1])
		if not TS in TSset: continue
		TS2timestamp[TS] = timestamp
	fr.close()
	I12name = {}
	fr = open('input/mapI1','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		I1,name = int(arr[0]),arr[1]
		if not I1 in I1set: continue
		I12name[I1] = name
	fr.close()
	I22name = {}
	fr = open('input/mapI2','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		I2,name = int(arr[0]),arr[1]
		if not I2 in I2set: continue
		I22name[I2] = name
	fr.close()
	I32name = {}
	fr = open('input/mapI3','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		I3,name = int(arr[0]),arr[1]
		if not I3 in I3set: continue
		I32name[I3] = name
	fr.close()
	# co-authorship here
	I1aI1bNum = {}
	fr = open('input/matL1','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		I1a,I1b,Num = int(arr[0]),int(arr[1]),int(arr[2])
		if I1a in I12name and I1b in I12name:
			I1aI1b = str(I1a)+','+str(I1b)
			I1aI1bNum[I1aI1b] = Num
	fr.close()
	# output
	fw = open('visual.txt','w')
	for i in range(0,M):
		TSi = TSs[i]
		timestamp = TS2timestamp[TSi]
		fw.write('*' + str(timestamp)+ '*\n')
		I1i,I2i,I3i = I1s[i],I2s[i],I3s[i]
		I3set = set()
		for I1 in I1i: I1set.add(I1)
		for I2 in I2i: I2set.add(I2)
		for item in I3i:
			for I3 in item: I3set.add(I3)
		nI1i,nI2i,nI3i,nI3set = len(I1i),len(I2i),len(I3i),len(I3set)
		I12B,I22B,I32B = {},{},{}
		I1I22B,I2I32B = {},{}
		# tensor here
		fr = open('input/tsrX','rb')
		fr.readline()
		for line in fr:
			arr = line.strip('\r\n').split(',')
			TS,I1,I2,I3 = int(arr[0]),int(arr[1]),int(arr[2]),int(arr[3])
			if TS <= TSi-TSgap: continue
			if TS > TSi: continue
			if I1 in I1i:
				if not I1 in I12B: I12B[I1] = 0
				I12B[I1] += 1
			if I2 in I2i:
				if not I2 in I22B: I22B[I2] = 0
				I22B[I2] += 1
			if I3 in I3set:
				if not I3 in I32B: I32B[I3] = 0
				I32B[I3] += 1
			if I1 in I12B and I2 in I22B:
				I1I2 = str(I1)+','+str(I2)
				if not I1I2 in I1I22B:
					I1I22B[I1I2] = 0
				I1I22B[I1I2] += 1
			if I2 in I22B and I3 in I32B:
				I2I3 = str(I2)+','+str(I3)
				if not I2I3 in I2I32B:
					I2I32B[I2I3] = 0
				I2I32B[I2I3] += 1
		fr.close()
		EXP = 0.5
		I1Bs,I2Bs,I3Bs = [],[],[]
		temp = 0.0
		for I1 in I1i:
			b = 0.0
			if I1 in I12B: b = I12B[I1]
			temp += (1.0*b)**EXP
		for I1 in I1i:
			b = 0.0
			if I1 in I12B: b = I12B[I1]
			I1Bs.append((1.0*b)**EXP/temp)
		temp = 0.0
		for I2 in I2i:
			b = 0.0
			if I2 in I22B: b = I22B[I2]
			temp += (1.0*b)**EXP
		for I2 in I2i:
			b = 0.0
			if I2 in I22B: b = I22B[I2]
			I2Bs.append((1.0*b)**EXP/temp)
		temp = 0.0
		for item in I3i:
			s = 0.0
			for I3 in item:
				b = 0.0
				if I3 in I32B: b = I32B[I3]
				s += b
			temp += (1.0*s)**EXP
		for item in I3i:
			s = 0.0
			for I3 in item:
				b = 0.0
				if I3 in I32B: b = I32B[I3]
				s += b
			I3Bs.append((1.0*s)**EXP/temp)
		temp = 0.0
		for b in I1Bs: temp = max(temp,b)
		for j in range(0,nI1i): I1Bs[j] /= temp
		temp = 0.0
		for b in I2Bs: temp = max(temp,b)
		for j in range(0,nI2i): I2Bs[j] /= temp
		temp = 0.0
		for b in I3Bs: temp = max(temp,b)
		for j in range(0,nI3i): I3Bs[j] /= temp
		# output
		for j in range(0,nI1i):
			I1 = I1i[j]
			I1name = I12name[I1]
			fw.write(str(I1)+'|'+I1name+'|'+str(I1Bs[j])+'\n')
		fw.write('\n')
		for j in range(0,nI2i):
			I2 = I2i[j]
			I2name = I22name[I2]
			fw.write(str(I2)+'|'+I2name+'|'+str(I2Bs[j])+'\n')
		fw.write('\n')
		for j in range(0,nI3i):
			item = I3i[j]
			s = ''
			for I3 in item:
				I3name = I32name[I3]
				s += ' '+I3name
			s += '|'+str(I3Bs[j])
			fw.write(s[1:]+'\n')
		fw.write('\n')
		for x in range(0,nI1i-1):
			I1x = I1i[x]
			I1xname = I12name[I1x]
			for y in range(x+1,nI1i):
				I1y = I1i[y]
				I1yname = I12name[I1y]
				I1min,I1max = min(I1x,I1y),max(I1x,I1y)
				I1aI1b = str(I1min)+','+str(I1max)
				num = 0
				if I1aI1b in I1aI1bNum: num = I1aI1bNum[I1aI1b]
				fw.write(str(I1x)+';'+I1xname+'|'+str(I1y)+';'+I1yname+'|'+str(num)+'\n')
		fw.write('\n')
		for x in range(0,nI1i):
			I1 = I1i[x]
			I1name = I12name[I1]
			for y in range(0,nI2i):
				I2 = I2i[y]
				I2name = I22name[I2]
				I1I2 = str(I1)+','+str(I2)
				if I1I2 in I1I22B:
					num = I1I22B[I1I2]
					fw.write(str(I1)+';'+I1name+'|'+str(I2)+';'+I2name+'|'+str(num)+'\n')
		fw.write('\n')
		for x in range(0,nI2i):
			I2 = I2i[x]
			I2name = I22name[I2]
			for j in range(0,nI3i):
				num = 0
				item = I3i[j]
				s = ''
				for I3 in item:
					I2I3 = str(I2)+','+str(I3)
					if I2I3 in I2I32B: num += I2I32B[I2I3]
					I3name = I32name[I3]
					s += ' '+I3name
				s = s[1:]
				if num == 0: continue
				fw.write(str(I2)+';'+I2name+'|'+s+'|'+str(num)+'\n')
		fw.write('\n')
	fw.close()
