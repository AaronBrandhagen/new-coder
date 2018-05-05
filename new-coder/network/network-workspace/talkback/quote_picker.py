from random import choice

class QuotePicker():
	def __init__(self, quotes_filename):
		with open('quotesFilename.txt') as quotes_file:
			self.quotes = quotes_file.readlines()
			
	def pick(self):
		return choice(self.quotes).strip()
	