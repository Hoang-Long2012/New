from output import setLevel, InfoLevel, log
import fs
import sys
import argparse
def getVersion():
	return "1.2"
def parseArgs():
	Parser = argparse.ArgumentParser(prog="new", description="Simple folder and file creation utility.")
	Parser.add_argument("folder", nargs="+", type=str, metavar="FOLDERS", help="Folders to create.")
	Parser.add_argument("-d", "--directory", nargs="+", type=str, metavar="FOLDERS", help="Folders to create.")
	Parser.add_argument("-f", "--file", nargs="+", type=str, metavar="FILES", help="Files to create.")
	Parser.add_argument("-b", "--byte", action="store_true", help="Create files in binary mode.")
	Parser.add_argument("-e", "--encoding", type=str, metavar="ENCODING", help="Encoding for created files.")
	Parser.add_argument("-o", "--overwrite", action="store_true", help="If created file exists then overwrite it.")
	Parser.add_argument("-y", "--yes", action="store_true", help="Overwrite without confirmation.")
	Parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (show detailed logs).")
	Parser.add_argument("-q", "--quiet", action="store_true", help="Suppress most output, only show critical errors.")
	Parser.add_argument("-V", "--version", action="version", version=f"%(prog)s version {getVersion()}", help="Show program version.")
	return Parser.parse_known_args()
def main():
	Args, Unknown = parseArgs()
	if Args.quiet and Args.verbose:
		log("Cannot use -q; --quiet and -v; --verbose at the same time.", InfoLevel.quiet, sys.stderr)
		sys.exit(2)
	if Args.quiet:
		setLevel(InfoLevel.quiet)
	elif Args.verbose:
		setLevel(InfoLevel.verbose)
	else:
		setLevel(InfoLevel.normal)
	if Unknown:
		Unknown_STR = ", ".join(Unknown)
		log(f"Unknown arguments: {Unknown_STR}", InfoLevel.quiet, sys.stderr)
		sys.exit(2)
	if Args.yes and not Args.overwrite:
		log("-y; --yes requires -o; --overwrite.", InfoLevel.quiet, sys.stderr)
		sys.exit(2)
	Folders = []
	if Args.folder:
		Folders.extend(Args.folder)
	if Args.directory:
		Folders.extend(Args.directory)
	if Folders:
		fs.createFolder(Folders, Args.overwrite, Args.yes)
	if Args.file:
		if Args.byte and Args.encoding:
			log("Cannot use -e; --encoding with -b; --byte.", InfoLevel.quiet, sys.stderr)
			sys.exit(2)
		fs.createFile(Args.file, Args.byte, Args.encoding, Args.overwrite, Args.yes)
	sys.exit(0)