import os
import sys
import argparse
def createFolder(Dirs):
	if not isinstance(Dirs, list):
		print(f"{str(Dirs)} is invalid.")
		return None
	for Dir in Dirs:
		if not isinstance(Dir, str):
			print(f"{Dir} is invalid.")
			continue
		if os.path.isdir(Dir):
			print(f"{Dir} already exists.")
			continue
		try:
			Dir = os.path.abspath(Dir)
			os.makedirs(Dir, exist_ok=True)
		except PermissionError:
			print(f"Permission denied: {Dir}")
			continue
def createFile(Files, Encoding="utf-8"):
	if not isinstance(Files, list):
		print(f"{str(Files)} is invalid.")
		return None
	for File in Files:
		if not isinstance(File, str):
			print(f"{File} is invalid.")
			continue
		if os.path.isfile(File):
			print(f"{File} already exists.")
			continue
		File = os.path.abspath(File)
		try:
			Parent = os.path.dirname(File)
			if Parent:
				os.makedirs(Parent, exist_ok=True)
			with open(File, "x", encoding=Encoding if Encoding else "utf-8"):
				pass
		except FileExistsError:
			print(f"{File} already exists.")
			continue
		except PermissionError:
			print(f"Permission denied: {File}")
			continue
def getVersion():
	return "1.0"
def parseArgs():
	Parser = argparse.ArgumentParser(prog="New", description="Simple folder and file creation utility.")
	Parser.add_argument("folder", nargs="*", type=str, metavar="FOLDERS", help="Folders to create.")
	Parser.add_argument("-f", "--file", nargs="*", type=str, metavar="FILES", help="Files to create.")
	Parser.add_argument("-e", "--encoding", type=str, default="utf-8", metavar="ENCODING", help="Encoding for created files.")
	Parser.add_argument("-V", "--version", action="version", version=f"%(prog)s version {getVersion()}", help="Show program version.")
	return Parser.parse_known_args()
def main():
	Args, Unknown = parseArgs()
	if Unknown:
		Unknown_STR = ", ".join(Unknown)
		print(f"Unknown arguments: {Unknown_STR}")
		sys.exit(2)
	if Args.folder:
		createFolder(Args.folder)
	if Args.file:
		createFile(Args.file, Args.encoding)
	sys.exit(0)
if __name__ == "__main__":
	main()