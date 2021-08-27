ROM_START="0100"

characters={
	'0':"00",
	'1':"01",
	'2':"02",
	'3':"03",
	'4':"04",
	'5':"05",
	'6':"06",
	'7':"07",
	'8':"08",
	'9':"09",
	'A':"0A",
	'B':"0B",
	'C':"0C",
	'D':"0D",
	'E':"0E",
	'F':"0F",
	'G':"10",
	'H':"11",
	'I':"12",
	'J':"13",
	'K':"14",
	'L':"15",
	'M':"16",
	'N':"17",
	'O':"18",
	'P':"19",
	'Q':"1A",
	'R':"1B",
	'S':"1C",
	'T':"1D",
	'U':"1E",
	'V':"1F",
	'W':"20",
	'X':"21",
	'Y':"22",
	'Z':"23",
	'+':"24",
	'-':"25",
	'*':"26",
	'/':"27",
	'=':"28",
	':':"29",
	' ':"2A",
	'<':"2B"
}


def hexToBin(num,size):
	#return format(int(num), '0'+str(size)+'b')
	return bin(int(num, 16))[2:].zfill(size)

def NOP():
	newline="0000"
	temp="00000000"
	try:
		temp=hexToBin(command[1],8)
	except:
		temp="00000000"
	return newline+temp
def LDQ():
	newline="0010"
	try:
		temp=hexToBin(command[1],8)
	except:
		print("ERROR, needs data")
		temp="00000000"
	return newline+temp

def LDB():
	newline="0011"
	try:
		temp=hexToBin(command[1],8)
	except:
		print("ERROR, needs data")
		temp="00000000"
	return newline+temp

#LDA DOESNT HAVE ANY OTHER DATA
def LDA():
	return "000100000000"

def CPY():
	newline="0100"
	try:
		temp=hexToBin(command[1],4)
		temp2=hexToBin(command[2],4)
	except:
		print("ERROR, needs two datas")
		temp="00000000"
	return newline+temp+temp2

def JMP():
	newline="0101"
	try:
		temp=hexToBin(command[1],8)
	except:
		print("ERROR, needs data")
		temp="00000000"
	return newline+temp

def STO():
	newline="0110"
	return newline+"00000000"

def STQ():
	newline="1000"
	try:
		temp=hexToBin(command[1],8)
	except:
		print("ERROR, needs data")
		temp="00000000"
	return newline+temp

def convertStrings(lines):
	i=0
	StringsToAdd=[]
	numString=0
	for line in lines:
		if line.startswith('"'):
			print("STARTING MATHCING LINE")
			# It adds a space at the end for some reason
			string1=line.replace('"','')[:-1]
			print(string1)

			string=[]
			for char in string1:
				print(char)
				string.append("NOP "+characters[char])
			string.append("NOP FF")

			StringsToAdd.append(string)
			lines[i]="STRING"+str(numString)
			numString=numString+1
		i+=1

	loc=0
	for line in lines:
		if line.startswith("STRING"):
			stringNumber=line[6:]
			print(StringsToAdd[int(stringNumber)])

			lines[loc]=StringsToAdd[int(stringNumber)][0]
			i=1
			while(StringsToAdd[int(stringNumber)][i]!="NOP FF"):
				print(StringsToAdd[int(stringNumber)][i])
				lines.insert(loc+i,StringsToAdd[int(stringNumber)][i])
				i=i+1
			lines.insert(loc+i,"NOP 2B")
		loc=loc+1
			
	print("LENGTH OF LIST: ",len(StringsToAdd))
	if len(StringsToAdd)>0:
		while(loc<len(StringsToAdd)):
			index=int(StringsToAdd[loc])
			print("inserting at ",index)
			step=0
			while StringsToAdd[loc+step+1]!="NOP FF":
				print("INSERTING: ",StringsToAdd[loc+step+1]," @ ",index+step)
				lines.insert(index+step,StringsToAdd[loc+step+1])
				step=step+1
			loc=loc+step+2

	return lines

#Add this in later. Automate HL and maybe loops Other stuff too that changes LIneNumbers
def convertMacros(lines):
	return lines

def convertLabels(lines):
	print("IN LABELS")
	labelDict={}
	i=0
	for line in lines:
		if line.startswith("."):
			labelName=line[1:].strip('\n')
			#ADD ONE TO ADVANCED PAST THE LABEL
			labelAddrDec=int(ROM_START,16)+i+1
			labelAddrHex=hex(labelAddrDec).split('x')[-1].upper()
			while(len(labelAddrHex)<4):
				labelAddrHex="0"+labelAddrHex
			labelDict[labelName]=labelAddrHex
			lines[i]="NOP 00"
		i=i+1


	#DONE With Defining Labels now plug them in
	i=0
	for line in lines:
		hit=False
		HorL=""
		if "H(" in line:
			hit=True
			HorL="H"
		if "L(" in line:
			hit=True
			HorL="L"
		if(hit==True):
			oldline=line
			for item,value in labelDict.items():
				if(HorL=='H'):
					line=line.replace("H("+item+")",value[:2])
				else:
					line=line.replace("L("+item+")",value[2:])

			print("Altering line from:",oldline," to ",line)
			print("replaced: ",lines[i])
			lines[i]=line
			print("to: ",lines[i])
		i=i+1
	return lines


 
MEMORY=[]

filepath = 'prog.txt'
with open(filepath) as fp:
   lines = fp.readlines()

# Removes Whitspace and full line comments
lines=[x for x in lines if (x!="\n" and not x.startswith("--"))]

lines=convertStrings(lines)
lines=convertMacros(lines)
lines=convertLabels(lines)

i=0
for line in lines:
	writeToFile=True
	print("READING LINE #"+str(i)+" : "+line)
	newline=""
	command=line.rstrip().split()

	# I'm Not sure why I added this but I am keeping it for now
	if(len(command)==0):
		print("HERE")
		continue

	#NOP -- 0000 <Number in Bin> or zeroes if no number specified
	if command[0]=="NOP":
		newline=NOP()
	#LDA doesnt have any other data
	elif command[0]=="LDA":
		newline=LDA()
	elif command[0]=="LDQ":
		newline=LDQ()
	elif command[0]=="LDB":
		newline=LDB()
	elif command[0]=="CPY":
		newline=CPY()
	elif command[0]=="JMP":
		newline=JMP()
	elif command[0]=="STO":
		newline=STO()
	elif command[0]=="STQ":
		newline=STQ()
	elif command[0]=="HLT":
		newline="1111"
		newline=newline+"00000000"
	else:
		writeToFile=False	

	if writeToFile==True:
		MEMORY.append(newline)
		print("newline IS : "+str(pow(2,8)+i)+" "+newline)


f = open("rom.txt", "w")
for i in range(0,len(MEMORY)):
	f.write(MEMORY[i]+"\n")
f.close()
