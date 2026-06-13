from enum import IntEnum
import sys
import fileinput
class __stdin__:
	pass
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
def getInput(File_List=None):
	Lines = []
	LineNumber = 0
	if File_List and isinstance(File_List, (str, list)):
		for LineNumber, Line in enumerate(fileinput.input(File_List, encoding="utf-8"), start=1):
			Lines.append(Line)
		return (LineNumber, Lines)
	else:
		for LineNumber, Line in enumerate(sys.stdin, start=1):
			Lines.append(Line)
		return (LineNumber, Lines)