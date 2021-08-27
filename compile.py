import re

varList = []

filepath = 'main.bas'
with open(filepath) as fp:
   lines = fp.readlines()

newFilePath="main.txt"
newFile = open(newFilePath, "w")



# Cycle through to plan out all the variables from dim statements and for loops
for line in lines:
	# Removes the comments/semicolons/newlines
	line = line.split(';')[0]
	# Don't process an empty line
	if len(line)==1:
		continue

	if re.findall("dim",line):
		regSplit = re.search('dim (.*)', line)
		print(regSplit.group(1))
		varList.append(regSplit.group(1))

	if re.findall("for ",line):
		regSplit = re.search('for (.*) from ([0-9]*) to ([0-9]*) step ([0-9]*)',line)
		if regSplit==None:
			print("For Loop Error")
		else: 
			print(regSplit.group(1))
			varList.append(regSplit.group(1))

# Cycle through all the vars and place them in memory
for var in varList:
	newFile.write("."+var+"\n")
	newFile.write("NOP 00\n")
	newFile.write("\n")

for line in lines:
	# Removes the comments/semicolons/newlines
	line = line.split(';')[0]
	# Don't process an empty line
	if len(line)==1:
		continue

	

