from output import InfoLevel, log, question, getInput, __stdin__
import os
import shutil
import stime
import sys
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
def createFolder(Dirs, Overwrite=False, Sure=False, ChangeTimestamp=True, AccessTime=None, ModifiedTime=None, Reference=None):
	if not isinstance(Dirs, list):
		log(f"{str(Dirs)} is invalid.", InfoLevel.quiet, sys.stderr)
		return None
	for Dir in Dirs:
		if not isinstance(Dir, str):
			log(f"{Dir} is invalid.", InfoLevel.quiet, sys.stderr)
			continue
		Dir = os.path.abspath(Dir)
		Ref = resolveReference(Reference, Dir)
		if os.path.exists(Dir):
			if not os.path.isdir(Dir):
				log(f"{Dir} is not a directory.", InfoLevel.quiet, sys.stderr)
				continue
			if not shouldOverwrite(Overwrite, Sure, Dir):
				if ChangeTimestamp:
					stime.updateTime(Dir, *getTime(Ref, AccessTime, ModifiedTime))
				continue
			try:
				shutil.rmtree(Dir)
				log(f"Removed {Dir}", InfoLevel.verbose)
			except PermissionError:
				log(f"Permission denied: {Dir}", InfoLevel.quiet, sys.stderr)
				continue
			except OSError as Error:
				log(f"Failed to remove {Dir}\n{Error}", InfoLevel.quiet, sys.stderr)
				continue
		try:
			os.makedirs(Dir, exist_ok=True)
			log(f"Created {Dir}", InfoLevel.verbose)
			if ChangeTimestamp and os.path.exists(Ref):
				stime.updateTime(Dir, *getTime(Ref, AccessTime, ModifiedTime))
		except PermissionError:
			log(f"Permission denied: {Dir}", InfoLevel.quiet, sys.stderr)
			continue
		except OSError as Error:
			log(f"Cannot create directory {Dir}.\n{Error}", InfoLevel.quiet, sys.stderr)
			continue
def createFile(Files, Byte=False, Encoding="utf-8", Overwrite=False, Sure=False, ChangeTimestamp=True, AccessTime=None, ModifiedTime=None, Reference=None, Write=None, Template_List=None):
	if not isinstance(Files, list):
		log(f"{str(Files)} is invalid.", InfoLevel.quiet, sys.stderr)
		return None
	for File_Path in Files:
		if not isinstance(File_Path, str):
			log(f"{File_Path} is invalid.", InfoLevel.quiet, sys.stderr)
			continue
		File_Path = os.path.abspath(File_Path)
		Ref = resolveReference(Reference, File_Path)
		Exists = os.path.exists(File_Path)
		if Exists:
			if not os.path.isfile(File_Path):
				log(f"{File_Path} is a directory.", InfoLevel.quiet, sys.stderr)
				continue
			if not shouldOverwrite(Overwrite, Sure, File_Path):
				if ChangeTimestamp:
					stime.updateTime(File_Path, *getTime(Ref, AccessTime, ModifiedTime))
				continue
			Mode = "wb" if Byte else "w"
		else:
			Mode = "xb" if Byte else "x"
		try:
			Parent = os.path.dirname(File_Path)
			if Parent:
				os.makedirs(Parent, exist_ok=True)
			if Byte:
				with open(File_Path, Mode, buffering=0):
					pass
			else:
				with open(File_Path, Mode, encoding=Encoding if Encoding else "utf-8") as File:
					LineNumber = 0
					Total_Characters = 0
					if Template_List and isinstance(Template_List, list):
						log("Reading template...", InfoLevel.verbose)
						Count, Lines = safeInput(Template_List, Encoding)
						LineNumber += Count or 0
						if Lines is not None:
							File.writelines(Lines)
							Total_Characters += len("".join(Lines))
					if Write is __stdin__:
						log("Reading from standard input. Press Ctrl+Z then Enter on Windows or Control+D on Linux, MacOS to finish, Ctrl+C to cancel.", InfoLevel.normal)
						Count, Lines = safeInput()
						LineNumber += Count or 0
						if Lines is not None:
							File.writelines(Lines)
							Total_Characters += len("".join(Lines))
					elif Write is not None:
						Decoded = Write
						try:
							Decoded = Write.encode().decode("unicode_escape")
							File.write(Decoded)
						except (ValueError, UnicodeError, UnicodeDecodeError):
							log(f"Warning: Invalid escape sequence, writing raw text: {Decoded}", InfoLevel.normal, sys.stderr)
							File.write(Write)
						Written_Lines = Decoded.count("\n") + (1 if Decoded else 0)
						LineNumber += Written_Lines
						Total_Characters += len(Decoded)
					log(f"Wrote {LineNumber} lines and {Total_Characters} Characters to {File_Path}", InfoLevel.verbose)
			if Exists:
				log(f"Overwritten {File_Path}", InfoLevel.verbose)
			else:
				log(f"Created {File_Path}", InfoLevel.verbose)
			if ChangeTimestamp and os.path.exists(Ref):
				stime.updateTime(File_Path, *getTime(Ref, AccessTime, ModifiedTime))
		except PermissionError:
			log(f"Permission denied: {File_Path}", InfoLevel.quiet, sys.stderr)
			continue
		except OSError as Error:
			log(f"Cannot create file {File_Path}.\n{Error}", InfoLevel.quiet, sys.stderr)
			continue