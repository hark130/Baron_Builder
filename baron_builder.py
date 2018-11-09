#################################################
#################### IMPORTS ####################
#################################################

from baron_builder_features import bbf01_BP_sub_menu, bbf01_BP_available
from baron_builder_features import bbf02_STAB_sub_menu, bbf02_STAB_available
from baron_builder_features import bbf06_GOLD_sub_menu, bbf06_GOLD_available
from baron_build_file_mgmt import list_save_games
from baron_build_file_mgmt import locate_save_games
from baron_build_file_mgmt import user_file_menu
from collections import OrderedDict
from stat import S_ISREG, ST_CTIME, ST_MODE, ST_MTIME
from zks_file_class import ZksFile              # ZksFile class
import os                                       # environ, path.join, getuid, path.isdir, system
import sys                                      # version_info

#################################################
#################### MACROS #####################
#################################################

# OPERATING SYSTEM
OS_UNKNOWS = 0  # Unknows OS
OS_LINUX = 1    # All *nix
OS_WINDOWS = 2  # All Windows
OS_APPLE = 3    # All OS/?
# USER TOLERANCE
MAX_ERRS = 3    # Maximum number of bad user answers tolerated before giving up
# DIRECTORY NAMES
TOP_DIR = "Baron_Builder"  # Store everything in there
ARCHIVE_DIR = "Archive"    # Move archived save files here
BACKUP_DIR = "Backup"      # Backup save files here
WORKING_DIR = "Working"    # Use this directory to unarchive and modify save games


#################################################
#################### GLOBALS ####################
#################################################

# SUPPORTED OPERATING SYSTEMS
supportedOSGlobal = [ OS_LINUX, OS_WINDOWS, OS_APPLE ]
# PYTHON MINIMUM VERSION REQUIRED
minMajNum = 3  # Minimum Python version major number
minMinNum = 5  # Minimum Python version minor number
minMicNum = 2  # Minimum Python version micro number
# OPERATING SYSTEM SAVE GAME LOCATIONS
# Linux - /home/user/.config/unity3d/Owlcat Games/Pathfinder Kingmaker/Saved Games
nixSaveGamePath = os.path.join(".config", "unity3d", "Owlcat Games", "Pathfinder Kingmaker", "Saved Games")
# Windows - C:\Users\user\AppData\LocalLow\Owlcat Games\Pathfinder Kingmaker\Saved Games
winSaveGamePath = os.path.join("AppData", "LocalLow", "Owlcat Games", "Pathfinder Kingmaker", "Saved Games")
# Apple - /home/user/Library/Application\ Support/unity.Owlcat\ Games.Pathfinder\ Kingmaker/Saved\ Games 
macSaveGamePath = os.path.join("Library", "Application Support", "unity.Owlcat Games.Pathfinder Kingmaker", "Saved Games")
numBadAnswers = 0  # Current number of bad answers


#################################################
################### FUNCTIONS ###################
#################################################


def check_py_ver(majNum, minNum, micNum):
    '''
        PURPOSE - Check the python version against a minimum
        INPUT
            majNum - Integer representing the minimum Python major version
            minNum - Integer representing the minimum Python minor version
            micNum - Integer representing the minimum Python micro version
        OUTPUT
            True if version meets minimums
            False otherwise
        NOTE
            If majNum, minNum, or micNum are None then that check is skipped
    '''
    # LOCAL VARIABLES
    retVal = True
    verTuple = ()

    # INPUT VALIDATION
    if not isinstance(majNum, int) and majNum is not None:
        raise TypeError("majNum is of type {}".format(type(majNum)))
    elif not isinstance(minNum, int) and majNum is not None:
        raise TypeError("minor number is of type {}".format(type(minNum)))
    elif not isinstance(micNum, int) and majNum is not None:
        raise TypeError("micro number is of type {}".format(type(micNum)))

    # CHECK VERSION
    verTuple = sys.version_info

    if isinstance(verTuple, tuple):
        # Major
        if retVal and majNum is not None:
            if majNum > verTuple.major:
                retVal = False
        # Minor
        if retVal and minNum is not None and majNum == verTuple.major:
            if minNum > verTuple.minor:
                retVal = False
        # Micro
        if retVal and micNum is not None and majNum == verTuple.major and minNum == verTuple.minor:
            if micNum > verTuple.micro:
                retVal = False
    else:
        raise TypeError("sys.version_info returned a non-tuple")

    # DONE
    return retVal


def determine_os():
    '''
        PURPOSE - Determine the basic operating system of the host
        INPUT - None
        OUTPUT - See OPERATAING SYSTEM macros
        NOTE
            This function does not determine *supported* OSs, only the current OS
    '''
    # LOCAL VARIABLES
    retVal = OS_UNKNOWS
    osStr = ""

    # CHECK OS
    osStr = sys.platform

    if isinstance(osStr, str):
        if osStr.startswith("freebsd"):
            retVal = OS_LINUX
        elif osStr.startswith("linux"):
            retVal = OS_LINUX
        elif osStr.startswith("win"):
            retVal = OS_WINDOWS
        elif osStr.startswith("cygwin"):
            retVal = OS_WINDOWS
        elif osStr.startswith("darwin"):
            retVal = OS_APPLE
        elif osStr.startswith("os2"):
            retVal = OS_APPLE
        else:
            retVal = OS_UNKNOWS
    else:
        raise TypeError("sys.platform returned a non-string")

    # DONE
    return retVal


def clear_screen(operSys):
    '''
        PURPOSE - Clear the screen
        INPUT
            operSys - See OPERATAING SYSTEM macros
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
    '''
    # LOCAL VARIABLES
    retVal = True
    supportedOS = supportedOSGlobal

    # INPUT VALIDATION
    if not isinstance(operSys, int):
        raise TypeError('Operating system is of type "{}" instead of integer'.format(type(operSys)))
    elif operSys not in supportedOS:
        raise ValueError("Operating system value is unknown")

    # CLEAR SCREEN
    if OS_LINUX == operSys or OS_APPLE == operSys:
        os.system("clear")
        # print("\n\n\n")  # DEBUGGING
    elif OS_WINDOWS == operSys:
        os.system("cls")
        # print("\n\n\n")  # DEBUGGING
    else:
        raise RuntimeError("Consider updating supportedOS list or control flow in clear_screen()")

    # DONE
    return retVal


def user_mod_menu(operSys, saveGameObj):
    '''
        PURPOSE - Allow a user to decide how to edit a given save game
        INPUT
            operSys - See OPERATAING SYSTEM macros
            saveGameObj - ZksFile object for a selected save game
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
    '''
    # LOCAL VARIABLES
    retVal = True
    supportedOS = supportedOSGlobal
    selection = 0  # Main menu selection
    tempInt = 0  # Temporary integer
    userClose = False  # User indicate to close the current save game
    userSave = False  # User indication they want to save
    userExit = False  # User indication they want to exit/quit
    curSaveGame = ""  # Current save game being edited
    f01Exists = False  # Set to True if saveGameObj.zPlayFile.jDict["Kingdom"]["BP"] exists
    f02Exists = False  # Set to True if saveGameObj.zPlayFile.jDict["Kingdom"]["Unrest"] exists
    f06Exists = False  # Set to True if saveGameObj.zPlayFile.jDict["Money"] exists
    userMenuDict = OrderedDict()  # Ordered dict of menu choices to build when determining save game maturity
    menuChoiceOrd = 97  # Ordinal for the first menu choice


    # GLOBAL VARIABLES
    global numBadAnswers

    # INPUT VALIDATION
    if not isinstance(operSys, int):
        raise TypeError('Operating system is of type "{}" instead of integer'.format(type(operSys)))
    elif operSys not in supportedOS:
        raise ValueError("Operating system value is unknown")
    elif not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))
    else:
        curSaveGame = saveGameObj.zName

    # DETERMINE SAVE GAME MATURITY
    # Feature 1
    f01Exists = bbf01_BP_available(saveGameObj)
    # Feature 2
    f02Exists = bbf02_STAB_available(saveGameObj)
    # Feature 6
    f06Exists = bbf06_GOLD_available(saveGameObj)

    # BUILD FEATURE DICTIONARY
    # Feature 1
    if f01Exists is True:
        userMenuDict[chr(menuChoiceOrd)] = tuple(("Change Build Points (BPs)", "Feature01"))
        menuChoiceOrd += 1
    # Feature 2
    if f02Exists is True:
        userMenuDict[chr(menuChoiceOrd)] = tuple(("Set Kingdom Unrest", "Feature02"))
        menuChoiceOrd += 1
    # Feature 6
    if f06Exists is True:
        userMenuDict[chr(menuChoiceOrd)] = tuple(("Change gold", "Feature06"))
        menuChoiceOrd += 1
    
    # CLEAR SCREEN
    clear_screen(operSys)

    while retVal and numBadAnswers <= MAX_ERRS:
        print("")  # Blank line
        # PRINT MENU
        # Print options
        print("SAVE GAME FILE MODIFICATIONS")
        print("Editing:\t{}\n".format(curSaveGame))
        # print("(c) Change Build Points (BPs)")  # Feature 1
        # print("(b) Change Kingdom Stability")  # Feature 2
        # print("(a) Change gold")  # Feature 6
        for key in userMenuDict.keys():
            print("({}) {}".format(key, userMenuDict[key][0]))
        print("")
        print('Type "clear" to clear the screen')
        print('Type "open" to open a new file')
        print('Type "save" to save the changes')
        print('Type "close" to close the file without saving')
        print('Type "quit" to save and exit this program')

        # Take input
        selection = input("Make your selection [Quit]:  ")
        clear_screen(operSys)

        # Modify input
        if len(selection) == 0:
            selection = "quit"
        else:
            selection = selection.lower()
            if selection in userMenuDict.keys():
                selection = userMenuDict[selection][1]

        # Execute selection
        if "clear" == selection:
            numBadAnswers = 0
            clear_screen(operSys)
        elif "open" == selection:
            numBadAnswers = 0
            print('\nNOT IMPLEMENTED\nChoose "close", then "quit", and start again instead')  # Placeholder
            pass
        elif "save" == selection:
            numBadAnswers = 0
            userSave = True
        elif "close" == selection:
            numBadAnswers = 0
            if are_you_sure("close the file without saving") is True:
                userClose = True
        elif "quit" == selection:
            numBadAnswers = 0
            userSave = True
            userExit = True
        elif "Feature01" == selection:
            numBadAnswers = 0
            if isinstance(saveGameObj, ZksFile) is True:
                try:
                    retVal = bbf01_BP_sub_menu(saveGameObj, numBadAnswers, MAX_ERRS)
                except Exception as err:
                    print("\nUnable to modify current build points")
                    print(repr(err))
                    retVal = False
                else:
                    if retVal is True:
                        numBadAnswers = 0
            else:
                print("Save game has already been closed")
                numBadAnswers += 1
        elif "Feature02" == selection:
            numBadAnswers = 0
            if isinstance(saveGameObj, ZksFile) is True:
                try:
                    retVal = bbf02_STAB_sub_menu(saveGameObj, numBadAnswers, MAX_ERRS)
                except Exception as err:
                    print("\nUnable to modify kingdom's unrest level")
                    print(repr(err))
                    retVal = False
                else:
                    if retVal is True:
                        numBadAnswers = 0
            else:
                print("Save game has already been closed")
                numBadAnswers += 1
        elif "Feature06" == selection:
            numBadAnswers = 0
            if isinstance(saveGameObj, ZksFile) is True:
                try:
                    retVal = bbf06_GOLD_sub_menu(saveGameObj, numBadAnswers, MAX_ERRS)
                except Exception as err:
                    print("\nUnable to modify gold amount")
                    print(repr(err))
                    retVal = False
                else:
                    if retVal is True:
                        numBadAnswers = 0
            else:
                print("Save game has already been closed")
                numBadAnswers += 1
        else:
            print("\nInvalid selection.  Try again.")
            numBadAnswers += 1

        # MENU ACTIONS
        # Save
        if userSave is True and isinstance(saveGameObj, ZksFile) is True:
            print("\nSaving any changes to {}".format(saveGameObj.zName))
            saveGameObj.update_zks()
            userSave = False
        elif userSave is True and saveGameObj is None:
            print("Save game has already been closed")
            numBadAnswers += 1

        # Close
        if userClose is True and isinstance(saveGameObj, ZksFile) is True:
            print("\nClosing {} without saving".format(saveGameObj.zName))
            saveGameObj.close_zks()
            saveGameObj = None
            curSaveGame = "None"
            userClose = False
        elif userClose is True and saveGameObj is None:
            print("Save game has already been closed")
            numBadAnswers += 1

        # Quit
        if userExit is True:
            print("\nExiting Baron Builder")
            userExit = False
            break

    # DONE
    print("")  # Blank line
    return retVal


def are_you_sure(actionStr=""):
    '''
        PURPOSE - Verify the user knows what they're doing
        INPUT
            actionStr - Optional string to confirm with the user
        OUTPUT
            If they're sure, True
            If not, False
            On error, Exception
        NOTES
            Too many bad answers will eventually return False
    '''
    # LOCAL VARIABLES
    retVal = False
    selection = ""

    # GLOBAL VARIABLES
    global numBadAnswers

    # INPUT VALIDATION
    if not isinstance(actionStr, str):
        raise TypeError('Action string is of type "{}" instead of string'.format(type(actionStr)))

    # PROMPT USER
    if len(actionStr) > 0:
        print('\nAre you sure you want to "{}"?'.format(actionStr))
    else:
        print("\nAre you sure?")

    while numBadAnswers <= MAX_ERRS:
        # Take input
        selection = input("Enter Y or [N]  ")

        # Modify input
        if len(selection) == 0:
            selection = "N"
        else:
            selection = selection.upper()

        # Parse input
        if "Y" == selection:
            retVal = True
            break
        elif "N" == selection:
            retVal = False
            break
        else:
            print("Invalid selection.  Try again.")
            numBadAnswers += 1

    # DONE
    return retVal


def main():
    # LOCAL VARIABLES
    retVal = True          # Indicates flow control success
    operSys = OS_UNKNOWS   # Operating system macro
    saveGamePath = ""      # Absolute path to save games
    saveGameFileList = []  # List of save game files
    fileNum = None         # Index into saveGameFileList the user selected
    absSaveGameFile = ""   # Absolute filename for the chosen save game
    saveGameObj = None     # Store the ZksFile object here

    # GLOBAL VARIABLES
    global numBadAnswers

    # WORK
    # Verify Python Version
    if retVal:
        try:
            retVal = check_py_ver(minMajNum, minMinNum, minMicNum)
        except Exception as err:
            print('check_py_ver() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
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
            print('determine_os() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
        else:
            if operSys == OS_UNKNOWS:
                print("Unable to identify the current operating system.")
                retVal = False
            else:
                pass

    # Locate Save Games
    if retVal:
        try:
            saveGamePath = locate_save_games(operSys)
        except Exception as err:
            print('locate_save_games() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
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
            print('list_save_games() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
        else:
            if len(saveGameFileList) <= 0:
                print("Unable to locate any save game files in directory.")
                retVal = False

    # Choose Save Game
    if retVal:
        try:
            fileNum = user_file_menu(operSys, saveGamePath, saveGameFileList)
        except Exception as err:
            print('user_file_menu() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
            pass
        else:
            if fileNum < 0:
                print("A save game was not selected.")
                retVal = False
            else:
                absSaveGameFile = os.path.join(saveGamePath, saveGameFileList[fileNum])

    # Instantiate Save File Object
    if retVal:
        try:
            saveGameObj = ZksFile(absSaveGameFile)
        except Exception as err:
            print('ZksFile() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
        else:
            pass

    # Unarchive Save File
    if retVal:
        try:
            saveGameObj.unpack_file(os.path.join(saveGamePath, TOP_DIR, WORKING_DIR))
        except Exception as err:
            print('ZksFile.unpack_file() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
        else:
            pass

    # Load Unarchived Json Files
    if retVal:
        try:
            saveGameObj.load_data()
        except Exception as err:
            print('ZksFile.load_data() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
        else:
            pass

    # Print Menu
    if retVal:
        try:
            retVal = user_mod_menu(operSys, saveGameObj)
        except Exception as err:
            print('user_mod_menu() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
        else:
            pass

    # DEBUGGING
    # print("retVal:             \t{}".format(retVal))
    # print("Operating system:   \t{}".format(operSys))
    # print("Save game directory:\t{}".format(saveGamePath))

    # DONE
    return retVal


if __name__ == "__main__":
    if main():
        print("Success!")  # DEBUGGING
        pass
    else:
        print("FAIL!")  # DEBUGGING
        pass
