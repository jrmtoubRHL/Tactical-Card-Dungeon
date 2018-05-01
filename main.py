# Buisson ou possible enemy escondido


from colorama import init, Fore, Style, Back

import random
import os
import time

import Control
print()
print()
print()
print()


USE_IDE = False


if USE_IDE != True:
	init(autoreset=True)

size_of_card = 6
dict_unicode = {'key1':     128477, 'key2': 128273, 'key3': 9919,
                'monster1': 128126, 'coin': 127765, 'Potion': 127826,
                'apple':    127822, 'chiken': 127831, 'chest': 9016,
                'pickaxe':  9935, 'bomb': 128163}

# init(convert=True)
monster = {'name':  ['Troll ', ' Bat  ', 'Skelet', ' Orc  ', ], 'uni': 128126,
           'life':  [3, 10], 'hit': [2, 7], 'drop': 2,
           'color': Fore.LIGHTCYAN_EX, 'id': 'monster', 'rank': -7}

coin = {'name':  ' Coin ', 'uni': 127765, 'drop': [2, 9],
        'color': Fore.LIGHTYELLOW_EX, 'id': 'coin', 'rank': 0}

Potion = {'name':  'Potion', 'uni': 127826, 'heal': [1, 3],
          'color': Fore.LIGHTGREEN_EX, 'id': 'potion', 'rank': +7}
Sword = {'name':  'Sword ', 'uni': 9935, 'hit': [1, 3], 'duration': 4,
         'color': Fore.LIGHTMAGENTA_EX, 'id': 'weapon', 'rank': +7}

hero = {'name':     ' HERO ', 'uni': 9935, 'life': [6, 9], 'hit': 1,
        'duration': 0, 'color': Fore.LIGHTWHITE_EX, 'id': 'hero',
        'max_life': 9}

chest = {'name':       'Chest ', 'color': Fore.LIGHTYELLOW_EX, 'id': 'chest',
         'randomdrop': [Sword, monster, coin, Potion], 'rank': +3}

trap = {'name': ' Trap ', 'hit': [2, 5], 'color': Fore.LIGHTBLUE_EX,
        'id':   'trap', 'pos': 'V ', 'rank': -3}

pick_randomcards = [monster,monster, coin, Sword, Potion, chest, trap]


class Card(object):

	def __init__(self, **kws):

		self.name = kws['name']
		self.color = kws['color']
		self.id = kws['id']
		self.life = kws.get('life')
		self.drop = kws.get('drop')
		self.hit = kws.get('hit')
		self.heal = kws.get('heal')
		self.duration = kws.get('duration')
		self.pos = kws.get('pos')
		self.randomdrop = kws.get('randomdrop')
		self.coins = 0
		# self.skin = chr(kws['uni'])
		if self.life and type(self.life) == list:
			self.life = random.randint(self.life[0], self.life[1])
		if self.drop and type(self.drop) == list:
			self.drop = random.randint(self.drop[0], self.drop[1])
		if self.hit and type(self.hit) == list:
			self.hit = random.randint(self.hit[0], self.hit[1])
		if self.heal and type(self.heal) == list:
			self.heal = random.randint(self.heal[0], self.heal[1])
		if self.randomdrop and type(self.randomdrop) == list:
			self.randomdrop = random.choice(self.randomdrop)
		if self.name and type(self.name) == list:
			self.name = random.choice(self.name)

	def match_up(self, encountred_card, hero_comefrom='r'):
		'''
		when two card collide
		:param encountred_card: the card hero is facing
		:param hero_comefrom:
		:return: new card, (in case chest is opened for exemple)
		'''
		self.stay = None
		if encountred_card.id == 'monster':
			life_enemy = encountred_card.life
			if self.hit == 0:
				self.life -= encountred_card.life
			if self.hit < life_enemy:
				if self.hit != 0:
					self.stay = True
				encountred_card.life -= self.hit
				self.hit = 0

			elif self.hit >= life_enemy:
				self.hit -= life_enemy
				encountred_card.life = 0

		elif encountred_card.id == 'potion':
			self.life = self.life + encountred_card.heal
			pass
		elif encountred_card.id == 'coin':
			self.coins += encountred_card.drop
			pass
		elif encountred_card.id == 'weapon':
			self.hit = encountred_card.hit
			pass
		elif encountred_card.id == 'chest':
			self.stay = True
			return Card(**encountred_card.randomdrop)
			pass
		elif encountred_card.id == 'trap':
			if hero_comefrom == 'u' and encountred_card.pos == '->':
				self.life = self.life - encountred_card.hit
			elif hero_comefrom == 'd' and encountred_card.pos == '<-':
				self.life = self.life - encountred_card.hit
			elif hero_comefrom == 'l' and encountred_card.pos == '^ ':
				self.life = self.life - encountred_card.hit
			elif hero_comefrom == 'r' and encountred_card.pos == 'V ':
				self.life = self.life - encountred_card.hit
			pass

		if self.life <= 0:
			self.life = 0
			print('GAMEOVER')


def int_2_show(num):
	if num == 0 or num == 0.0:
		result = '  '
	else:
		result = str(num)
		if len(result) == 1:
			result = result + ' '
	return result


def format_stats(card_dict):
	'''
	Convert each card into string ready to print ,
	:param card_dict:
	:return:
	'''
	result = ''
	if card_dict.id == 'hero':

		result += str(Fore.LIGHTGREEN_EX) + int_2_show(card_dict.life)
		result += '  '

		result += str(Fore.LIGHTRED_EX) + int_2_show(
			card_dict.hit)  # result += str(Fore.LIGHTWHITE_EX) + int_2_show(card_dict.duration)

	elif card_dict.id == 'monster':
		result += '  '

		result += str(Fore.LIGHTGREEN_EX) + int_2_show(card_dict.life)
		# result += str(Fore.LIGHTRED_EX) + int_2_show(card_dict.hit)
		result += '  '

	elif card_dict.id == 'coin':
		result += str(Fore.BLACK) + '  '
		result += str(Fore.LIGHTYELLOW_EX) + int_2_show(card_dict.drop)
		result += '  '


	elif card_dict.id == 'potion':
		result += '  '

		result += str(Fore.LIGHTGREEN_EX) + int_2_show(card_dict.heal)
		result += '  '
	elif card_dict.id == 'weapon':
		result += '  '
		result += str(Fore.LIGHTRED_EX) + int_2_show(card_dict.hit)
		# result += str(Fore.LIGHTWHITE_EX) + int_2_show(card_dict.duration)
		result += '  '


	elif card_dict.id == 'chest':
		result += str(Fore.BLACK) + '  '
		result += '  '
		result += '  '

	elif card_dict.id == 'trap':
		result += '  '
		result += str(Fore.LIGHTRED_EX) + int_2_show(card_dict.hit)
		result += str(Fore.LIGHTWHITE_EX) + card_dict.pos

		if card_dict.pos == 'V ':
			card_dict.pos = '<-'
		elif card_dict.pos == '<-':
			card_dict.pos = '^ '
		elif card_dict.pos == '^ ':
			card_dict.pos = '->'
		elif card_dict.pos == '->':
			card_dict.pos = 'V '

	result += Fore.WHITE
	return result




class Board(object):
	'''

	'''

	UP, DOWN, LEFT, RIGHT, PAUSE = 1, 2, 3, 4, 5

	def __init__(self, size_tup=(3, 4)):

		self.xy_size = size_tup
		self.hero_pos = [1, 1]
		self.cells = []
		self.moves = 0
		self.init_random_board()

	# todo fill with random cards (create func random)

	def random_card_spawn(self):

		return Card(**random.choice(pick_randomcards))

	def moveright(self):
		# implement matchup, return move or not

		change_card = self.HERO.match_up(
				self.cells[self.hero_pos[1]][self.hero_pos[0] + 1],
				hero_comefrom='l')

		if change_card:
			self.cells[self.hero_pos[1]][self.hero_pos[0] + 1] = change_card

		elif not self.HERO.stay:
			self.cells[self.hero_pos[1]][self.hero_pos[0] + 1] = self.HERO

			# move cards if hero not first column:
			if self.hero_pos[0] != 0:

				cards_to_move = list(range(self.hero_pos[0]))[::-1]

				for moving in cards_to_move:
					self.cells[self.hero_pos[1]][moving + 1] = \
					self.cells[self.hero_pos[1]][moving]

			self.cells[self.hero_pos[1]][0] = self.random_card_spawn()
			self.hero_pos[0] += 1

	def movedown(self):
		# print(self.hero_pos)

		change_card = self.HERO.match_up(
				self.cells[self.hero_pos[1] + 1][self.hero_pos[0]],
				hero_comefrom='u')
		if change_card:
			self.cells[self.hero_pos[1] + 1][self.hero_pos[0]] = change_card

		elif not self.HERO.stay:
			self.cells[self.hero_pos[1] + 1][self.hero_pos[0]] = self.HERO

			if self.hero_pos[1] == 1:  # hero not fisrt line, we move
				self.cells[1][self.hero_pos[0]] = self.cells[0][
					self.hero_pos[0]]
			elif self.hero_pos[1] == 2:
				self.cells[2][self.hero_pos[0]] = self.cells[1][
					self.hero_pos[0]]
				self.cells[1][self.hero_pos[0]] = self.cells[0][
					self.hero_pos[0]]
			elif self.hero_pos[1] == 3:
				self.cells[3][self.hero_pos[0]] = self.cells[2][
					self.hero_pos[0]]
				self.cells[2][self.hero_pos[0]] = self.cells[1][
					self.hero_pos[0]]
				self.cells[1][self.hero_pos[0]] = self.cells[0][
					self.hero_pos[0]]

			self.cells[0][self.hero_pos[0]] = self.random_card_spawn()
			self.hero_pos[1] += 1

	def moveleft(self):

		change_card = self.HERO.match_up(
				self.cells[self.hero_pos[1]][self.hero_pos[0] - 1],
				hero_comefrom='r')
		if change_card:
			self.cells[self.hero_pos[1]][self.hero_pos[0] - 1] = change_card

		elif not self.HERO.stay:
			self.cells[self.hero_pos[1]][self.hero_pos[0] - 1] = self.HERO

			if self.hero_pos[0] != self.xy_size[0]:
				# move cards if hero not last column:
				cards_to_move = list(range(self.xy_size[0]))[
				                self.hero_pos[0] + 1:]

				for moving in cards_to_move:
					self.cells[self.hero_pos[1]][moving - 1] = \
						self.cells[self.hero_pos[1]][moving]

			self.cells[self.hero_pos[1]][
				self.xy_size[0] - 1] = self.random_card_spawn()
			self.hero_pos[0] -= 1

	def moveup(self):
		# print(self.hero_pos)

		change_card = self.HERO.match_up(
				self.cells[self.hero_pos[1] - 1][self.hero_pos[0]],
				hero_comefrom='d')
		if change_card:
			self.cells[self.hero_pos[1] - 1][self.hero_pos[0]] = change_card

		elif not self.HERO.stay:
			self.cells[self.hero_pos[1] - 1][self.hero_pos[0]] = self.HERO

			if self.hero_pos[1] == 2:  # hero antelast line, we move
				self.cells[2][self.hero_pos[0]] = self.cells[3][
					self.hero_pos[0]]
			elif self.hero_pos[1] == 1:
				self.cells[1][self.hero_pos[0]] = self.cells[2][
					self.hero_pos[0]]
				self.cells[2][self.hero_pos[0]] = self.cells[3][
					self.hero_pos[0]]

			self.cells[self.xy_size[1] - 1][
				self.hero_pos[0]] = self.random_card_spawn()

			self.hero_pos[1] -= 1

	def init_random_board(self):
		self.cells = []
		for linee in range(self.xy_size[1]):

			one_line = []
			for pos in range(self.xy_size[0]):
				# todo
				if linee == self.hero_pos[1] and pos == self.hero_pos[0]:
					self.HERO = Card(**hero)
					one_line.append(self.HERO)
				else:
					one_line.append(self.random_card_spawn())
			self.cells.append(one_line)

	# print(self.cells)

	def boardToString(self, margins=2):
		"""
		return a string representation of the current board.
		input = list, of lines, (lines = lists of card dict object)
		"""
		caract_separator_horiz = '-'

		horizon_separator = '++'.join(
			[str(caract_separator_horiz * size_of_card)] * self.xy_size[0])

		# x_separator = (separator_chr[:-1]*(self.xy_size[0]))*2
		list_redable_lines = []  # *self.xy_size[0]]
		# print(list_redable_lines)
		for line in self.cells:
			line_statss = []
			line_names = []
			for card in line:

				one_card_stats = format_stats(card)

				one_card_name = str(card.color) + str(
						card.name[:size_of_card]) + Fore.WHITE

				line_statss.append(one_card_stats)
				line_names.append(one_card_name)

			list_redable_lines.append(line_names)
			list_redable_lines.append(line_statss)

		# list_redable_lines.append(x_separator[2:])
		# print(one_line)
		print(
			Fore.WHITE + caract_separator_horiz + horizon_separator + caract_separator_horiz)
		for numb, readable_line in enumerate(list_redable_lines):

			print('|' + '||'.join(readable_line) + '|')
			if numb % 2 != 0:
				print(
					Fore.WHITE + caract_separator_horiz + horizon_separator + caract_separator_horiz)
		print('Coins: {}, Moves: {}'.format(self.HERO.coins, self.moves))

		return


def clearScreen(ide=True):
	"""Clear the console"""

	if ide == False:
		os.system('cls' if os.name == 'nt' else 'clear')


# os.system('clear')


def readMove():
	"""
	read and return a move to pass to a board
	"""
	k = Control.getKey()
	return k


def main_loop(ide=True):
	b = Board()
	b.boardToString()
	# b.moveright()
	# b.boardToString()

	#
	while (True):

		if ide== True:

			m = input()
		else:
			init(autoreset=True)
			m = readMove()

		if (m == 72 or m == 'w') and b.hero_pos[1] >= 1:  # up
			clearScreen(ide=ide)
			b.moveup()
			b.boardToString()
			b.moves += 1

		if (m == 80 or m == 's') and b.hero_pos[1] <= b.xy_size[1] - 2:  # down
			clearScreen(ide=ide)
			b.movedown()
			b.boardToString()
			b.moves += 1

		if (m == 77 or m == 'd') and b.hero_pos[0] <= b.xy_size[
			0] - 2:  # right
			clearScreen(ide=ide)
			b.moveright()
			b.boardToString()
			b.moves += 1

		if (m == 75 or m == 'a') and b.hero_pos[0] >= 1:  # left
			clearScreen(ide=ide)
			b.moveleft()
			b.boardToString()
			b.moves += 1

		if (m == 'r'):  # reset
			b = Board()
			b.boardToString()
			b.moves += 1


main_loop(ide=USE_IDE)

# print(lolel.cells)
