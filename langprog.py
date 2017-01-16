# array = []

# for line in open("program"):
# 	for char in line.replace(' ', ''):
# 		array.append(char)

# print array

class Token(object):
    def __init__(self):
	    self.id = None
	    self.value = None


tokens = []

operators = ['+', '-', '*', '/', '^']

# put all of these in a map
NUMBER = 5
LETTER = 6
OPERATOR = 7
DQUOTE = 8
SQUOTE = 9
STRING = 10
DECIMAL = 11
VAR = 12
WS = 13
EQ = 14
VECOP = 15
PWR = 16
RB = 17
LB = 18
COMMA = 19
OTHER = 30

ES = 99		# End statement
EP = 100	# End program


lines = [
			"var a = 3.0 + 3.0;",
			"\"this is a string\"",
			"\"this\" + \"that\"",
			"3.0 + \"that\"",
			"a = 3.0^2",
			"a = //16",
			"a = /16",
			"a = [1, 2] .+ [3, 2]"
		]

# lines = [
# 			"3 + 4 * 8"
# 		]

line = ""

index = 0
currentChar = ''
charType = ''
numberString = ''
# make all of these things in an array and then a function; clearArray()
# use this to determine if the number is part of a var name or a string or is a number
currentTokenValue = ''
enclosing = False
decimal = False
decimalAmount = 0




def parse(tokens):

	# Parsing is not implemented
	print "\n\n", "PARSING"
	for token in tokens:
		print token.id, token.value
	return




def runTests():
	global index
	global lines
	global line
	for l in lines:
		line = l
		print "\n\n", line
		raw_input()

		getChar()
		while index < len(line) + 1:
			lex()
			# this might work
			#clearAll()

		print "\n------------------------\n         TOKENS\n------------------------\n"
		global tokens

		for token in tokens:
			print "ID:", str(token.id).ljust(2, ' '), "  |   Value:", token.value

		parse(tokens)

		tokens = []
		index = 0

	return


def clearAll():
	global charType
	global currentChar
	global numberString
	global decimalAmount
	charType = ""
	currentChar = ""
	numberString = ""
	decimalAmount = 0

	return


def addChar():
	global numberString
	numberString += currentChar
	return

def getChar():
	global index
	global line
	if index < len(line):
		global currentChar
		currentChar = line[index]
		index += 1
		determineChar()

	else:
		index += 1
		currentChar = 'EOF'
		print 'EOF'
		determineChar()
	return


def innerDetermine():
	global currentChar
	global charType
	global enclosing

	if currentChar.isdigit():
		print "digit"
		charType = NUMBER
	
	elif currentChar.isalpha():
		print "alpha"
		charType = LETTER
	
	elif currentChar in operators:
		print "operator"
		charType = OPERATOR

	# I think this only has implications in how alphas and stuff are handled
	elif currentChar == "\"":
		print "double quote"
		charType = DQUOTE

	elif currentChar == ".":
		print "decimal"
		charType = DECIMAL
		global decimal
		global decimalAmount
		decimal = True
		decimalAmount += 1

	elif currentChar == " " or currentChar == '\t':
		print "whitespace"
		charType = WS

	elif currentChar == "=":
		print "equals"
		charType = EQ

	elif currentChar == "[":
		print "left bracket"
		charType = LB

	elif currentChar == "]":
		print "right bracket"
		charType = RB

	elif currentChar == ",":
		print "comma"
		charType = COMMA

	elif currentChar == ";":
		print "end statement"
		charType = ES
	
	else:
		print "other"
		charType = OTHER

	return


def determineChar():
	global currentChar
	global charType
	global enclosing
	if currentChar != 'EOF':
		innerDetermine()
	else:
		print "end"
		charType = EP

	return

def lex():
	global charType
	global decimal
	global numberString
	global enclosing
	print charType

	if charType == NUMBER:
		numberString = ""
		print "NUMBER"
		addChar()
		getChar()
		print charType
		while charType == NUMBER or charType == DECIMAL:
			if charType == DECIMAL:
				global decimalAmount
				decimalAmount += 1
			print "next digit"
			addChar()
			getChar()
		token = Token()
		if decimal == True:
			print "decimalAmount", decimalAmount
			if decimalAmount > 2:
				print "Error: float number format; too many decimal points"
			else:
				token.value = float(numberString)
		else:
			token.value = int(numberString)
		token.id = NUMBER
		tokens.append(token)

		decimal = False
		decimalAmount = 0

		numberString = ""

	elif charType == LETTER:
		print "LETTER"
		addChar()
		getChar()
		print charType
		while charType == LETTER:
			print "next letter"
			addChar()
			getChar()

		token = Token()
		token.value = numberString
		token.id = VAR
		tokens.append(token)

		clearAll()

	elif charType == DECIMAL:
		print "DECIMAL"
		getChar()

	elif charType == OPERATOR:
		print "OPERATOR"
		
		if decimal:
			token = Token()
			token.value = "." + currentChar
			token.id = VECOP
			tokens.append(token)
			decimal = False
			decimalAmount = 0

		else:
			token = Token()
			token.value = currentChar
			token.id = OPERATOR
			tokens.append(token)

		getChar()

	elif charType == DQUOTE:
		getChar()
		print "START STRING"
		while charType != EP and charType != ES and charType != DQUOTE:
			print "string"
			addChar()
			getChar() 
		
		token = Token()
		token.value = numberString
		token.id = STRING
		tokens.append(token)
		print "END STRING"

		enclosing = not enclosing
		clearAll()

	elif charType == WS:
		if enclosing == False:
			clearAll()
		getChar()

	elif charType == EQ:
		print "EQUALS"
		token = Token()
		token.value = currentChar
		token.id = EQ
		tokens.append(token)

		getChar()

	elif charType == RB:
		print "RIGHT BRACKET"
		token = Token()
		token.value = currentChar
		token.id = RB
		tokens.append(token)

		getChar()

	elif charType == LB:
		print "LEFT BRACKET"

		token = Token()
		token.value = currentChar
		token.id = LB
		tokens.append(token)

		getChar()

	elif charType == COMMA:
		print "COMMA"

		token = Token()
		token.value = currentChar
		token.id = COMMA
		tokens.append(token)

		getChar()

	elif charType == ES:
		print "END STATEMENT"
		token = Token()
		token.value = currentChar
		token.id = ES
		tokens.append(token)

		getChar()

	elif charType == EP:
		print "END PROGRAM"

	else:
		print "OTHER"
		getChar()

	return #[some integer error value later on]


# need to also replace some other things depending on what we need, tabs, newlines
#line = line.replace(' ', '')

runTests()