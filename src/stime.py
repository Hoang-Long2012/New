from output import InfoLevel, log
from datetime import datetime
import os
import sys
def formatTime(Time_Str, Pattern):
	try:
		return datetime.strptime(Time_Str, Pattern).timestamp()
	except ValueError:
		return None
def expandFormats(Format):
	yield Format
	if Format.endswith("%M"):
		yield Format + ":%S"
		yield Format + ":%S.%f"
def parseTime(Time_Str):
	if Time_Str is None:
		return None
	if isinstance(Time_Str, (int, float)):
		return float(Time_Str)
	Formats = [
		"%Y-%m-%dT%H:%M:%S",
		"%Y-%m-%dT%H:%M:%S%z",
		"%Y-%m-%d",
		"%Y/%m/%d",
		"%Y_%m_%d",
		"%Y%m%d%H%M",
		"%Y%m%d",
		"%Y-%m-%d %H:%M",
		"%Y_%m_%d %H:%M",
		"%Y/%m/%d %H:%M",
		"%Y:%m:%d %H:%M",
		"%Y %m %d %H:%M",
		"%Y%m%d%H%M.%S",
		"%Y%m%d%H%M%S",
	]
	for Format in Formats:
		for RealFormat in expandFormats(Format):
			Time = formatTime(Time_Str, RealFormat)
			if Time is None:
				continue
			return Time
	raise ValueError(f"Invalid time format: {Time_Str}")
def updateTime(Path, AccessTime=None, ModifiedTime=None):
	Stat = os.stat(Path)
	try:
		Atime = parseTime(AccessTime)
	except ValueError:
		log(f"Warning: Access time invalid: {AccessTime}", InfoLevel.normal, sys.stderr)
		Atime = None
	try:
		Mtime = parseTime(ModifiedTime)
	except ValueError:
		log(f"Warning: Modified time invalid: {ModifiedTime}", InfoLevel.normal, sys.stderr)
		Mtime = None
	Atime_final = Atime if Atime is not None else Stat.st_atime
	Mtime_final = Mtime if Mtime is not None else Stat.st_mtime
	os.utime(Path, (Atime_final, Mtime_final))
	log(f"Updated {Path} atime={Atime_final} mtime={Mtime_final}", InfoLevel.verbose)