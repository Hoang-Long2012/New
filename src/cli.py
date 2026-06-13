from output import setLevel, InfoLevel, log, __stdin__
import fs
import sys
import argparse
def getVersion():
	return "1.4"
def parseArgs():
	Parser = argparse.ArgumentParser(prog="New", description="Simple folder and file creation utility.", epilog="Read readme full at https://github.com/Hoang-Long2012/new", allow_abbrev=False)
	General = Parser.add_argument_group("General options")
	Folder = General.add_mutually_exclusive_group()
	Folder.add_argument("folder", nargs="*", type=str, metavar="[FOLDERS...]", help="Folders to create.")
	Folder.add_argument("-d", "--directory", nargs="+", type=str, metavar="[FOLDERS...]", help="Folders to create.")
	General.add_argument("-f", "--file", nargs="+", type=str, metavar="[FILES...]", help="Files to create.")
	File_Format = Parser.add_argument_group("File format options")
	File_Format = File_Format.add_mutually_exclusive_group()
	File_Format.add_argument("-b", "--byte", action="store_true", help="Create files in binary mode.")
	File_Format.add_argument("-e", "--encoding", type=str, metavar="[ENCODING...]", help="Encoding for created files.")
	Overwrite = Parser.add_argument_group("Overwrite options")
	Overwrite.add_argument("-o", "--overwrite", action="store_true", help="If created file exists then overwrite it.")
	Overwrite.add_argument("-y", "--yes", action="store_true", help="Overwrite without confirmation.")
	Timestamp = Parser.add_argument_group("Update timestamp options")
	Timestamp.add_argument("-a", "--access-time", metavar="[ACCESS TIME...]", help="Update access time.")
	Timestamp.add_argument("-m", "--modified-time", metavar="[MODIFIED TIME...]", help="Update modified time")
	Timestamp.add_argument("-t", "--time", metavar="[TIME...]", help="Update both access time and modified time")
	Timestamp.add_argument("-r", "--reference", type=str, metavar="[REFERENCE FILE...]", help="Copy timestamps from reference file. May be combined with either -a or -m, but not both")
	Timestamp.add_argument("-c", "--no-change-timestamp", action="store_false", default=True, help="Not change timestamp if file existed.")
	WriteOptions = Parser.add_argument_group("Write options")
	WriteOptions.add_argument("-w", "--write", nargs="?", type=str, const=__stdin__, default=None, metavar="[TEXT TO WRITE...]", help="Write content to file created, currently only testing with text files.")
	WriteOptions.add_argument("-T", "--template", nargs="+", type=str, default=None, metavar="[TEMPLATE FILES...]", help="Copy  files content specified to file created, currently only testing with text files.")
	Output = Parser.add_argument_group("Output options")
	Output = Output.add_mutually_exclusive_group()
	Output.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (show detailed logs).")
	Output.add_argument("-q", "--quiet", action="store_true", help="Suppress most output, only show critical errors.")
	Parser.add_argument("-V", "--version", action="version", version=f"%(prog)s version {getVersion()}", help="Show program version.")
	Args = Parser.parse_args()
	if Args.yes and not Args.overwrite:
		Parser.error("-y; --yes requires -o; --overwrite.")
	if not (Args.folder or Args.directory or Args.file):
		Parser.error("at least one of folder, -d/--directory or -f/--file is required")
	if (Args.write is not None or Args.template) and not Args.file:
		Parser.error("-w; --write or -T; --template requires -f; --file.")
	if Args.time and (Args.access_time or Args.modified_time or Args.reference):
		Parser.error("-t; --time cannot be used with [-a; --access-time], [-m; --modified-time] or [-r; --reference]")
	if not Args.no_change_timestamp and (Args.access_time or Args.modified_time or Args.reference or Args.time):
		Parser.error("-c; --no-change-timestamp cannot be used with timestamp options")
	if Args.reference and Args.access_time and Args.modified_time:
		Parser.error("-r; --reference cannot be used at the same time with both [-a; --access-time] and [-m; --modified-time]")
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