import math
import time
from random import randint

def generateCode(codes):
	while True:
		code = randint(1000, 9999)
		if not code in codes:
			return code

def takeTime():
	return time.time()

def getTimeout(end):
	return end - takeTime()

