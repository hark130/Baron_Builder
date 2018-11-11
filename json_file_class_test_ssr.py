from baron_builder_imports import saveGameJson
from json_file_class import JsonFile
import os


def main():
	# LOCAL VARIABLES
	retVal = True
	sgjNixFile = None     # Full path to the ./Test_Files/Linux/saveGameJson
	sgjWinFile = None     # Full path to the ./Test_Files/Windows/saveGameJson
	sgjNixJsonObj = None  # JsonFile object containing the linux save game json file
	sgjWinJsonObj = None  # JsonFile object containing the windows save game json file

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
	for key in sgjWinJsonObj.jDict.keys():
		print("{} : {}".format(key, sgjWinJsonObj.jDict[key]))

	# DONE
	return retVal


if __name__ == "__main__":
	main()