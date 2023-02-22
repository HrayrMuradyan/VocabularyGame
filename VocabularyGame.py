import textract
import numpy as np

class VocGame:
	def __init__(self, filepath):
		self.filepath = filepath
		self.options = ['a','b','c','d']

	def extract_text(self):
		text = textract.process(self.filepath)
		text = text.decode("utf-8")
		return text

	def get_dict_words(self, text):
		text = text.split('\n\n')
		splitted = [x.split(' – ') for x in text]
		self.words = {x[0]: x[1] for x in splitted}
		self.wordlist = list(self.words.keys())
		self.deflist = list(self.words.values())

	def create_question(self, word):
		definition = self.words[word]
		wordlist = [word]
		deflist = [self.words[word]]
		for i in range(3):
			choice = np.random.choice(self.deflist, replace=False)
			while choice == definition:
				choice = np.random.choice(self.deflist, replace=False)
			deflist.append(choice)
		np.random.shuffle(deflist)
		answer = self.options[deflist.index(definition)]
		question_dict = dict(zip(self.options, deflist))
		return question_dict, answer

	def game(self):
		shuffled = self.wordlist.copy()
		np.random.shuffle(shuffled)
		iterator = iter(shuffled)
		user_input = None
		print("--- Welcome to the Vocabulary Game! ---")
		print("If you want to play the game, type: START")
		print("If you want to exit the game, type: EXIT")
		valid_input = False
		while not valid_input:
			user_input = input('Valid inputs: "START", "EXIT": ').lower()
			if user_input == 'exit' or user_input == 'end':
				print("The game exited")
				return 
			elif user_input == 'start':
				valid_input = True
			else:
				print('Invalid input. Type START or EXIT.')
				continue
		print("\nStarting the game...")
		wrong_answers = 0
		correct_answers = 0
		counter = 0
		try:
			while user_input != 'exit' or user_input != 'end':
				word = next(iterator)
				question, answer = self.create_question(word)
				print("What is the definition of the given word ---> %s" % (word))
				print("Options to choose from: ")
				for opt, defin in question.items():
					print("%s: %s" % (opt, defin))
				print('\n') 
				valid_input = False
				while not valid_input:
					user_input = input('Valid inputs: "a", "b", "c", "d", "EXIT": ').lower()
					if user_input == answer:
						correct_answers += 1
						valid_input = True
						print(">> Correct! <<\n")
					elif (user_input in self.options) and (user_input != answer):
						wrong_answers += 1
						valid_input = True
						print('<< Wrong! >>\n')
						print('Right answer: %s\n' % (answer))
					elif user_input == 'exit':
						print('Exiting the game...')
						return "Game exited"
					else:
						print('Write a valid answer! Available options: "a", "b", "c", "d", "EXIT"')
				counter += 1
		except StopIteration:
			print("You answered to all questions. End of the game.")
		finally:
			print("\nNumber of words shown: %s" % (counter))
			print("Number of correct answered questions: %s" % (correct_answers))
			print("Number of wrong answered questions: %s" % (wrong_answers))

if __name__ == "__main__":
	vocGame = VocGame('Vocabulary.docx')
	text = vocGame.extract_text()
	vocGame.get_dict_words(text)
	vocGame.game()
