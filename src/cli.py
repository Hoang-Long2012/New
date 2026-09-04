from output import setLevel, InfoLevel, __stdin__
import fs
import sys
import argparse
def getVersion():
	return "1.9"
def validateArgs(Args, Parser):
	if Args.folder and Args.directory:
		Parser.error("-d; --directory cannot be used with folder positional argument.")
	if Args.yes and not Args.overwrite:
		Parser.error("-y; --yes requires -o; --overwrite.")
	if not (Args.folder or Args.directory or Args.file):
		Parser.error("at least one of folder, -d/--directory or -f/--file is required.")
	if (Args.write is not None or Args.template) and not Args.file:
		Parser.error("-w; --write or -T; --template requires -f; --file.")
	if Args.time and (Args.access_time or Args.modified_time or Args.reference):
		Parser.error("-t; --time cannot be used with [-a; --access-time], [-m; --modified-time] or [-r; --reference].")
	if not Args.no_change_timestamp and (Args.access_time or Args.modified_time or Args.reference or Args.time):
		Parser.error("-c; --no-change-timestamp cannot be used with timestamp options.")
	if Args.reference and Args.access_time and Args.modified_time:
		Parser.error("-r; --reference cannot be used at the same time with both [-a; --access-time] and [-m; --modified-time].")
def parseArgs():
	Parser = argparse.ArgumentParser(prog="New", description="%(prog)s: Simple folder and file creation utility.", usage="%(prog)s [OPTIONS] [FOLDERS ...]", epilog="For more information, see the full README:\nhttps://github.com/Hoang-Long2012/new", formatter_class=argparse.RawTextHelpFormatter, allow_abbrev=False, add_help=False)
	Parser.add_argument("folder", nargs="*", type=str, metavar="FOLDERS", help="Folders to create.")
	General = Parser.add_argument_group("General options")
	General.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
	General.add_argument("-V", "--version", action="version", version=f"%(prog)s version {getVersion()}", help="Show the program version number and exit.")
	General.add_argument("-d", "--directory", nargs="+", type=str, metavar="FOLDERS", help="Folders to create.")
	General.add_argument("-f", "--file", nargs="+", type=str, metavar="FILES", help="Files to create.")
	File_Format = Parser.add_argument_group("File format options")
	File_Format = File_Format.add_mutually_exclusive_group()
	File_Format.add_argument("-b", "--byte", action="store_true", help="Create files in binary mode.")
	File_Format.add_argument("-e", "--encoding", type=str, metavar="ENCODING", help="Encoding for created files.")
	Overwrite = Parser.add_argument_group("Overwrite options")
	Overwrite.add_argument("-o", "--overwrite", action="store_true", help="Overwrite existing files.")
	Overwrite.add_argument("-y", "--yes", action="store_true", help="Overwrite existing files without confirmation.")
	Timestamp = Parser.add_argument_group("Timestamp options")
	Timestamp.add_argument("-a", "--access-time", metavar="TIME", help="Set the access time.")
	Timestamp.add_argument("-m", "--modified-time", metavar="TIME", help="Set the modified time.")
	Timestamp.add_argument("-t", "--time", metavar="TIME", help="Set both the access and modified times.")
	Timestamp.add_argument("-r", "--reference", type=str, metavar="FILE", help="Copy timestamps from file.")
	Timestamp.add_argument("-c", "--no-change-timestamp", action="store_false", default=True, help="Do not change timestamps of existing files.")
	WriteOptions = Parser.add_argument_group("Write options")
	WriteOptions.add_argument("-w", "--write", nargs="?", type=str, const=__stdin__, default=None, metavar="CONTENT", help="Write content to the created file.\nIf CONTENT is omitted, read from stdin.")
	WriteOptions.add_argument("-T", "--template", nargs="+", type=str, default=None, metavar="FILES", help="Copy template file contents to the created file.\nUse '-' to read the template from stdin.")
	Output = Parser.add_argument_group("Output options")
	Output = Output.add_mutually_exclusive_group()
	Output.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
	Output.add_argument("-q", "--quiet", action="store_true", help="Suppress most output.")
	Args = Parser.parse_args()
	validateArgs(Args, Parser)
	return Args
def main():
	Args = parseArgs()
	if Args.quiet:
		setLevel(InfoLevel.quiet)
	elif Args.verbose:
		setLevel(InfoLevel.verbose)
	else:
		setLevel(InfoLevel.normal)
	if Args.time:
		Args.access_time = Args.time
		Args.modified_time = Args.time
	if Args.folder or Args.directory:
		fs.createFolder(Args.folder or Args.directory, Args.overwrite, Args.yes, Args.no_change_timestamp, Args.access_time, Args.modified_time, Args.reference)
	if Args.file:
		fs.createFile(Args.file, Args.byte, Args.encoding, Args.overwrite, Args.yes, Args.no_change_timestamp, Args.access_time, Args.modified_time, Args.reference, Args.write, Args.template)
	sys.exit(0)