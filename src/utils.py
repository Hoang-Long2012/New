from output import question, log, InfoLevel, getInput
import sys
import os
import glob
def pattern(Patterns):
	if not isinstance(Patterns, list):
		log(f"{Patterns} must be list.")
		return None
	Result = []
	for Pattern in Patterns:
		if not isinstance(Pattern, str):
			log(f"{Pattern} must be string.")
			continue
		Files = glob.glob(Pattern)
		if Files:
			Result.extend(Files)
		else:
			Result.append(Pattern)
	return Result
def readBinaryTemplate(Template_List):
	Chunks = []
	if not isinstance(Template_List, list):
		log(f"{Template_List} is invalid.", InfoLevel.quiet, sys.stderr)
		return None
	for Template in Template_List:
		if not isinstance(Template, str):
			log(f"{Template} is invalid.", InfoLevel.quiet, sys.stderr)
			continue
		if Template == "-":
			log("Reading from standard input. Press Ctrl+Z then Enter on Windows or Control+D on Linux, MacOS to finish, Ctrl+C to cancel.", InfoLevel.normal)
			_, Lines = safeInput()
			if Lines is not None:
				try:
					Hex = bytes.fromhex("".join(Lines))
					Chunks.append(Hex)
				except ValueError:
					Lines = "\n".join(Lines)
					log(f"Error: Invalid hex string: {Lines}", InfoLevel.quiet, sys.stderr)
					continue
		Template = os.path.abspath(Template)
		if not os.path.exists(Template):
			log(f"Template not found: {Template}", InfoLevel.quiet, sys.stderr)
			continue
		if not os.path.isfile(Template):
			log(f"{Template} is not a file.", InfoLevel.quiet, sys.stderr)
			continue
		try:
			with open(Template, "rb") as File:
				Chunks.append(File.read())
				continue
		except PermissionError as Error:
			log(f"Cannot access to template:\n{Error}", InfoLevel.quiet, sys.stderr)
			continue
		except OSError as Error:
			log(f"Cannot read template:\n{Error}", InfoLevel.quiet, sys.stderr)
			continue
	if not Chunks:
		log("No valid binary templates found", InfoLevel.normal)
	return b"".join(Chunks)
def safeInput(File_List=None, Encoding="utf-8"):
	try:
		return getInput(File_List, Encoding)
	except FileNotFoundError as Error:
		log(f"Template not found:\n{Error}", InfoLevel.quiet, sys.stderr)
		return (None, None)
	except PermissionError as Error:
		log(f"Cannot access to template:\n{Error}", InfoLevel.quiet, sys.stderr)
		return (None, None)
	except OSError as Error:
		log(f"Cannot read template:\n{Error}", InfoLevel.quiet, sys.stderr)
		return (None, None)
	except KeyboardInterrupt:
		log("Canceled.", InfoLevel.verbose)
		return (None, None)
def shouldOverwrite(Overwrite, Sure, Path):
	if not Overwrite:
		Type = "Directory" if os.path.isdir(Path) else "File"
		log(f"{Type} already exists: {Path}", InfoLevel.normal)
		return False
	if Sure:
		return True
	return question(f"Are you sure you want to overwrite {Path}", Enter=False)
def resolveReference(Ref, Fallback):
	if Ref is None:
		return Fallback
	if isinstance(Ref, str) and os.path.exists(Ref):
		return Ref
	log(f"Warning: Reference {Ref} invalid, using {Fallback}", InfoLevel.normal, sys.stderr)
	return Fallback
def getTime(Ref, AccessTime, ModifiedTime):
	Stat = os.stat(Ref)
	return (AccessTime if AccessTime is not None else Stat.st_atime, ModifiedTime if ModifiedTime is not None else Stat.st_mtime)