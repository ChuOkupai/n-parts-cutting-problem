from srcs import *
from sys import argv, stderr

def parse_args():
	if len(argv) != 4:
		print(f"Usage: {argv[0]} <length> <width> <number of parts>", file=stderr)
		exit(1)
	return map(int, argv[1:])

if __name__ == "__main__":
	try:
		[print(p) for p in nparts(*parse_args())]
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)
