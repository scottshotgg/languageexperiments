string = "33.99 + 3"

result = 0.0
index = 0
periodIndex = 0
lastChar = ""
lastToken = 0
variable = ""
period = False


def getChar():
	global string
	global index
	global lastChar
	try:
		char = string[index]
		index += 1
		print char
		return char
	except IndexError as ie:
		return 0

def period():
	# this needs to be changed to be the number and not the sting
	if lastToken == 1 and (determineChar(getChar()) == 1):
		print "float"
		global periodIndex
		periodIndex += 1
		period = True

# build this thing out and make it auto assign the tokens, the end user does not need to know the tokenization
# as long as the program keeps up with the tokens
symbolMap = {
	".": period
}


def determineChar(char):

	if char != 0 and not char.isspace(): 
		if char.isdigit():
			print char
			global lastToken
			lastToken = 1
			global result
			global periodIndex
			global period
			if period:
				result = result + (float(char) * pow(10, -periodIndex))
				periodIndex += 1
			else:
				result += float(char)
		#else lastToken == 

		elif char.isalpha():
			global lastToken
			lastToken = 2
			if determineChar(getChar()) == 2:
				global variable
				variable = variable + char
			print "this is a variable", variable[::-1]
				
		elif char in symbolMap:
			symbolMap[char]()

	return lastToken


# strip out the whitespace chars
string = string.replace(" ", "")


for x in range(len(string) - 1):
	determineChar(getChar())

print result