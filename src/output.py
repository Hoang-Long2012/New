from enum import IntEnum
import sys
class InfoLevel(IntEnum):
	verbose = 2
	normal = 1
	quiet = 0
Current_Level = InfoLevel.normal
def setLevel(Level):
	global Current_Level
	Current_Level = Level
def log(MSG, Level, Stream=sys.stdout):
	if Current_Level >= Level:
		print(MSG, file=Stream)
def question(MSG):
	while True:
		try:
			Select = input(f"{MSG} (Y / N)? ").strip().lower()
		except EOFError:
			return False
		if Select in ["y", "yes"]:
			return True
		elif Select in ["n", "no"]:
			return False
		else:
			print("Invalid choice.", file=sys.stderr)
			continue