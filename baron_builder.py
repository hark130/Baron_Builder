#################################################
#################### IMPORTS ####################
#################################################

from baron_builder_features import user_feature_menu
from baron_builder_features import bbf01_BP_sub_menu, bbf01_BP_available
from baron_builder_features import bbf02_STAB_sub_menu, bbf02_STAB_available
from baron_builder_features import bbf06_GOLD_sub_menu, bbf06_GOLD_available
from baron_builder_imports import OS_UNKNOWS
from baron_builder_imports import supportedOSGlobal
from baron_builder_imports import minMajNum, minMinNum, minMicNum
from baron_builder_imports import TOP_DIR, WORKING_DIR
from baron_builder_file_mgmt import list_save_games, locate_save_games, user_file_menu
from baron_builder_utilities import check_py_ver, determine_os
from zks_file_class import ZksFile              # ZksFile class
import os                                       # environ, path.join, getuid, path.isdir, system


#################################################
################### FUNCTIONS ###################
#################################################


def main():
    # LOCAL VARIABLES
    retVal = True          # Indicates flow control success
    operSys = OS_UNKNOWS   # Operating system macro
    saveGamePath = ""      # Absolute path to save games
    saveGameFileList = []  # List of save game files
    fileNum = None         # Index into saveGameFileList the user selected
    absSaveGameFile = ""   # Absolute filename for the chosen save game
    saveGameObj = None     # Store the ZksFile object here
    numBadAnswers = 0      # Number of consecutive bad answers given by user

    # WORK
    # Verify Python Version
    if retVal:
        try:
            retVal = check_py_ver(minMajNum, minMinNum, minMicNum)
        except Exception as err:
            print('check_py_ver() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            if not retVal:
                print("Incorrect version of Python.\nWritten for Python {}.{}.{}.".format(minMajNum, minMinNum, minMicNum))
                retVal = False

    # Check OS
    if retVal:
        try:
            operSys = determine_os()
        except Exception as err:
            print('determine_os() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            if operSys == OS_UNKNOWS:
                print("Unable to identify the current operating system.")
                retVal = False
            elif operSys not in supportedOSGlobal:
                print("Operating system is not supported.")
                retVal = False
            else:
                pass

    # Locate Save Games
    if retVal:
        try:
            saveGamePath = locate_save_games(operSys)
        except Exception as err:
            print('locate_save_games() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            if len(saveGamePath) <= 0:
                print("Unable to locate the save game directory.")
                retVal = False

    # Parse Save Games
    if retVal:
        try:
            saveGameFileList = list_save_games(operSys, saveGamePath)
        except Exception as err:
            print('list_save_games() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            if len(saveGameFileList) <= 0:
                print("Unable to locate any save game files in directory.")
                retVal = False

    # Choose Save Game
    if retVal:
        try:
            fileNum = user_file_menu(operSys, saveGamePath, saveGameFileList, numBadAnswers)
        except RuntimeError as err:
            if "Quit" == str(err):
                retVal = False
            else:
                raise err
        except Exception as err:
            print('user_file_menu() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            if isinstance(fileNum, bool) and fileNum is False:
                retVal = False
            elif isinstance(fileNum, int) and 0 > fileNum:
                print("A save game was not selected.")
                retVal = False
            else:
                numBadAnswers = 0
                # Update save game file list in case save games were deleted
                saveGameFileList = list_save_games(operSys, saveGamePath)
                absSaveGameFile = os.path.join(saveGamePath, saveGameFileList[fileNum])

    # Instantiate Save File Object
    if retVal:
        try:
            saveGameObj = ZksFile(absSaveGameFile)
        except Exception as err:
            print('ZksFile() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            pass

    # Unarchive Save File
    if retVal:
        try:
            saveGameObj.unpack_file(os.path.join(saveGamePath, TOP_DIR, WORKING_DIR))
        except Exception as err:
            print('ZksFile.unpack_file() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            pass

    # Load Unarchived Json Files
    if retVal:
        try:
            saveGameObj.load_data()
        except Exception as err:
            print('ZksFile.load_data() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            pass

    # Print Menu
    if retVal:
        try:
            retVal = user_feature_menu(operSys, saveGameObj, numBadAnswers)
        except Exception as err:
            print('user_feature_menu() raised "{}" exception'.format(str(err)))  # DEBUGGING
            retVal = False
        else:
            numBadAnswers = 0

    # DEBUGGING
    # print("retVal:             \t{}".format(retVal))
    # print("Operating system:   \t{}".format(operSys))
    # print("Save game directory:\t{}".format(saveGamePath))

    # DONE
    return retVal


if __name__ == "__main__":
    if main():
        # print("Success!")  # DEBUGGING
        pass
    else:
        # print("FAIL!")  # DEBUGGING
        pass
