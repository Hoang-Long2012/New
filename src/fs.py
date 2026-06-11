from output import InfoLevel, log, question
import os
import shutil
import sys
import stime
def shouldOverwrite(Overwrite, Sure, Path):
	if not Overwrite:
		Type = "Directory" if os.path.isdir(Path) else "File"
		log(f"{Type} already exists: {Path}", InfoLevel.normal)
		return False
	if Sure:
		return True
	return question(f"Are you sure you want to overwrite {Path}")
def createFolder(Dirs, Overwrite=False, Sure=False, ChangeTimestamp=True, AccessTime=None, ModifiedTime=None):
	if not isinstance(Dirs, list):
		log(f"{str(Dirs)} is invalid.", InfoLevel.quiet, sys.stderr)
		return None
	for Dir in Dirs:
		if not isinstance(Dir, str):
			log(f"{Dir} is invalid.", InfoLevel.quiet, sys.stderr)
			continue
		Dir = os.path.abspath(Dir)
		if os.path.exists(Dir):
			if not os.path.isdir(Dir):
				log(f"{Dir} is not a directory.", InfoLevel.quiet, sys.stderr)
				continue
			if not shouldOverwrite(Overwrite, Sure, Dir):
				if ChangeTimestamp:
					stime.updateTime(Dir, AccessTime, ModifiedTime)
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
			if ChangeTimestamp:
				stime.updateTime(Dir, AccessTime, ModifiedTime)
		except PermissionError:
			log(f"Permission denied: {Dir}", InfoLevel.quiet, sys.stderr)
			continue
		except OSError as Error:
			log(f"Cannot create directory {Dir}.\n{Error}", InfoLevel.quiet, sys.stderr)
			continue
def createFile(Files, Byte=False, Encoding="utf-8", Overwrite=False, Sure=False, ChangeTimestamp=True, AccessTime=None, ModifiedTime=None):
	if not isinstance(Files, list):
		log(f"{str(Files)} is invalid.", InfoLevel.quiet, sys.stderr)
		return None
	for File in Files:
		if not isinstance(File, str):
			log(f"{File} is invalid.", InfoLevel.quiet, sys.stderr)
			continue
		File = os.path.abspath(File)
		Exists = os.path.exists(File)
		if Exists:
			if not os.path.isfile(File):
				log(f"{File} is a directory.", InfoLevel.quiet, sys.stderr)
				continue
			if not shouldOverwrite(Overwrite, Sure, File):
				if ChangeTimestamp:
					stime.updateTime(File, AccessTime, ModifiedTime)
				continue
			Mode = "wb" if Byte else "w"
		else:
			Mode = "xb" if Byte else "x"
		try:
			Parent = os.path.dirname(File)
			if Parent:
				os.makedirs(Parent, exist_ok=True)
			if Byte:
				with open(File, Mode, buffering=0):
					pass
			else:
				with open(File, Mode, encoding=Encoding if Encoding else "utf-8",):
					pass
			if Exists:
				log(f"Overwritten {File}", InfoLevel.verbose)
			else:
				log(f"Created {File}", InfoLevel.verbose)
			if ChangeTimestamp:
				stime.updateTime(File, AccessTime, ModifiedTime)
		except PermissionError:
			log(f"Permission denied: {File}", InfoLevel.quiet, sys.stderr)
			continue
		except OSError as Error:
			log(f"Cannot create file {File}.\n{Error}", InfoLevel.quiet, sys.stderr)
			continue