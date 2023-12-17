import os

# Five of a kind, where all five cards have the same label: AAAAA
FIVE_OF_A_KIND = 7
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
FOUR_OF_A_KIND = 6
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
FULL_HOUSE = 5
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
THREE_OF_A_KIND = 4
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
TWO_PAIR = 3
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
ONE_PAIR = 2
# High card
HIGH_CARD = 1

card_strength = {
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
	'T': 10,
	'J': 11,
	'Q': 12,
	'K': 13,
	'A': 14
}

def find_type(cards, part):
	card_counts = {}
	for c in cards:
		old_value = card_counts.get(c, 0)
		card_counts[c] = old_value + 1

	if part == 1:
		counts_list = sorted(list(card_counts.values()), reverse=True)
	else:
		jokers = card_counts.pop('J', 0)
		counts_list = sorted(list(card_counts.values()), reverse=True)
		if jokers == 5:
			counts_list = [0]
		counts_list[0] += jokers

	result = 0
	match counts_list[0]:
		case 5:
			result = FIVE_OF_A_KIND
		case 4:
			result = FOUR_OF_A_KIND
		case 3:
			if counts_list[1] == 2:
				result = FULL_HOUSE
			else:
				result = THREE_OF_A_KIND
		case 2:
			if counts_list[1] == 2:
				result = TWO_PAIR
			else:
				result = ONE_PAIR
		case _:
			result = HIGH_CARD
	return result

input_file = os.path.join(os.path.dirname(__file__), 'input7.txt')
with open(input_file) as f:
	lines = f.read().splitlines()
	hands = [(cards, int(bid)) for cards, bid in [x.split() for x in lines]]

def calc_result(hands):
	return sum((rank+1)*hand[1] for rank, hand in enumerate(hands))

def calc_strength(cards):
	return tuple(map(card_strength.get, cards))

def solve_part1():
	cmp = lambda hand: (find_type(hand[0], part=1), calc_strength(hand[0]))
	return calc_result(sorted(hands, key=cmp))

def solve_part2():
	card_strength['J'] = 1
	cmp = lambda hand: (find_type(hand[0], part=2), calc_strength(hand[0]))
	return calc_result(sorted(hands, key=cmp))

print(f'Part 1: {solve_part1()}') # 248217452
print(f'Part 2: {solve_part2()}') # 245576185
