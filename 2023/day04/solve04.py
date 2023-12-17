# Exercise 4
# Author: Kristin Avans
# Optimized part 2 by me.
import os

# Part 1
def find_win(string):  
	splitted = string.split("|")
	my_nr = splitted[1].split()
	win_nr = splitted[0].split(":")[1].split()

	total_win = 0
	nr_of_win_cards = 0
	for nr in win_nr:
		if nr in my_nr:
			total_win = max(1, total_win*2)
			nr_of_win_cards += 1
	return(total_win, nr_of_win_cards)

input_file = os.path.join(os.path.dirname(__file__), 'input04.txt')
with open(input_file) as f:
	lines = f.readlines()
	final_win = 0
	for l in lines:
		win_current, nr_of_win_cards = find_win(l)
		final_win += win_current
		
print(f'Part 1: {final_win}') # 21919


# Part 2
def get_wins(card, list_of_numbers):
	answer = 1
	if list_of_numbers[card] == 0:
		return 1
	else:
		for i in range(card + 1, card + card_wins[card] + 1):
			answer = answer + get_wins(i, list_of_numbers)
		return(answer)


with open(input_file) as f:
	lines = f.readlines()
	card_wins = [0]
	for l in lines:
		_, nr_of_win_cards = find_win(l)
		card_wins.append(nr_of_win_cards)
	
	total_nr_cards = [1] * len(card_wins)
	total_nr_cards[0] = 0
	#total_nr_cards = 0
	for card in range(1, len(card_wins)):
		for add in range(card_wins[card]):
			if card + add + 1 < len(total_nr_cards):
				total_nr_cards[card + add + 1] += total_nr_cards[card]
	#	total_nr_cards = total_nr_cards + get_wins(card, card_wins)
		
print(f'Part 2: {sum(total_nr_cards)}') # 9881048
#print(f'Part 2: {total_nr_cards}') # 9881048
