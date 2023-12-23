import os, sys
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description = "Create a directory structure with python starter files for each day of the advent calendar."
	)
	parser.add_argument("root", help="Name of the root directory.")
	parser.add_argument(
		"-f",
		help="Force create. Overrides previous files.",
		required=False,
		action='store_true'
	)
	args = parser.parse_args()

	root_created = False
	days_created = [False] * 25

	# Make sure the root directory exists
	if not os.path.exists(args.root):
		os.mkdir(args.root)
		root_created = True

	# Make each day of the advent calendar
	for i in range(1, 26):
		if not os.path.exists(f'{args.root}/day{i:02d}'):
			os.mkdir(f'{args.root}/day{i:02d}')
			days_created[i-1] = True

		if days_created[i-1] or args.f:
			# Create an empty file for the input
			with open(f'{args.root}/day{i:02d}/input{i:02d}.txt', 'w'):
				pass

			# Create a python script with boilerplate code for the solution
			with open(f'{args.root}/day{i:02d}/solve{i:02d}.py', 'w') as f:
				f.write('import os\n\n')
				f.write(f"input_file = os.path.join(os.path.dirname(__file__), 'input{i:02d}.txt')\n")
				f.write(f"with open(input_file) as f:\n")
				f.write(f"\tlines = f.read().splitlines()\n\n")
				f.write('def solve_part1():\n')
				f.write('\tpass\n\n')
				f.write('def solve_part2():\n')
				f.write('\tpass\n\n')
				f.write("print('Part 1:', solve_part1())\n")
				f.write("print('Part 2:', solve_part2())\n")
			days_created[i-1] = True

	if root_created:
		print(f"Created folder \"{args.root}\".")
	if any(days_created):
		print(f"Created {sum(days_created)} new days.")
	else:
		print("Nothing new created.")