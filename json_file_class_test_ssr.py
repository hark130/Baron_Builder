from baron_builder_imports import saveGameJson
from json_file_class import JsonFile
from collections import OrderedDict
import os


def main():
	# LOCAL VARIABLES
	retVal = True
	sgjNixFile = None     # Full path to the ./Test_Files/Linux/saveGameJson
	sgjWinFile = None     # Full path to the ./Test_Files/Windows/saveGameJson
	sgjNixJsonObj = None  # JsonFile object containing the linux save game json file
	sgjWinJsonObj = None  # JsonFile object containing the windows save game json file
	sgjNixLowVer = 10000  # Store the lowest save game version here
	sgjWinLowVer = 10000  # Store the lowest save game version here

	# PARSE JSON FILES
	# Linux
	sgjNixFile = os.path.join(os.getcwd(), "Test_Files", "Linux", saveGameJson)
	sgjNixJsonObj = JsonFile(sgjNixFile)
	sgjNixJsonObj.read_json_file()
	sgjNixJsonObj.parse_json_contents()
	# Windows
	sgjWinFile = os.path.join(os.getcwd(), "Test_Files", "Windows", saveGameJson)	
	sgjWinJsonObj = JsonFile(sgjWinFile)	
	sgjWinJsonObj.read_json_file()	
	sgjWinJsonObj.parse_json_contents()

	# REVERSE FUZZINEER JSON FILES
	# Linux
	# for key in sgjNixJsonObj.jDict.keys():
		# print("{} : {}".format(key, sgjNixJsonObj.jDict[key]))

	for entry in sgjNixJsonObj.jDict["Files"]:
		# print(entry)  # 1
		# print(entry.keys())  # 2
		# 3
		# if entry["Filename"].startswith("Auto"):
		# 	print(entry)
		# 	# print(type(entry))
		# 	sgjNixJsonObj.jDict["Files"].remove(entry)
		# 4
		if sgjNixLowVer > entry["Version"]:
			sgjNixLowVer = entry["Version"]

	print("Lowest Linux save game version is {}".format(sgjNixLowVer))

	# for entry in sgjNixJsonObj.jDict["Files"]:
	# 	print(entry["Filename"])

	# Windows
	# for key in sgjWinJsonObj.jDict.keys():
		# print("{} : {}".format(key, sgjWinJsonObj.jDict[key]))

	for entry in sgjWinJsonObj.jDict["Files"]:
		# print(entry)  # 1
		# print(entry.keys())  # 2
		# print(entry["Filename"])
		# 4
		if sgjWinLowVer > entry["Version"]:
			sgjWinLowVer = entry["Version"]

	print("Lowest Windows save game version is {}".format(sgjWinLowVer))

	# DONE
	return retVal


if __name__ == "__main__":
	main()