#################################################
#################### IMPORTS ####################
#################################################

from baron_builder_features import bbf01_BP_sub_menu
from baron_builder_features import bbf02_STAB_sub_menu
from baron_builder_features import bbf06_GOLD_sub_menu
from stat import S_ISREG, ST_CTIME, ST_MODE, ST_MTIME
from zks_file_class import ZksFile              # ZksFile class
import pwd                                      # getpwuid
import os                                       # path.join, getuid, path.isdir, system
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


def locate_save_games(operSys):
    '''
        PURPOSE - Find the absolute path to the save games directory
        INPUT
            operSys - See OPERATAING SYSTEM macros
        OUTPUT
            On success, String holding the absolute path to the save games
            If not found, empty string
            On failure, Exception
    '''
    # LOCAL VARIABLES
    retVal = ""    # Absolute path of the save games directory
    supportedOS = supportedOSGlobal
    userName = ""  # User name of the user
    homeDir = ""   # Home directory of the user
    relDir = ""    # Relative directory of the save games

    # INPUT VALIDATION
    if not isinstance(operSys, int):
        raise TypeError('Operating system is of type "{}" instead of integer'.format(type(operSys)))
    elif operSys not in supportedOS:
        raise ValueError("Operating system value is unknown")

    # DETERMINE USER NAME
    if OS_LINUX == operSys:
        userName = pwd.getpwuid(os.getuid()).pw_name
        homeDir = pwd.getpwuid(os.getuid()).pw_dir
        relDir = nixSaveGamePath
    elif OS_WINDOWS == operSys:
        userName = pwd.getpwuid(os.getuid()).pw_name
        homeDir = pwd.getpwuid(os.getuid()).pw_dir
        relDir = winSaveGamePath
    elif OS_APPLE == operSys:
        userName = pwd.getpwuid(os.getuid()).pw_name
        homeDir = pwd.getpwuid(os.getuid()).pw_dir
        relDir = macSaveGamePath
    else:
        raise RuntimeError("Consider updating supportedOS list or control flow in locate_save_games()")

    # CONSTRUCT HOME DIRECTORY
    if len(homeDir) == 0 and isinstance(userName, str) and len(userName) > 0:
        pass  # Already constructed?

    # FIND SAVE GAMES
    if isinstance(homeDir, str) and len(homeDir) > 0:
        retVal = os.path.join(homeDir, relDir)
        if not os.path.isdir(retVal):
            print("Unable to locate save game directory at:\n{}".format(retVal))  # DEBUGGING
            retVal = ""
    else:
        raise RuntimeError('Invalid home directory of type "{}" and length "{}"'.format(type(homeDir), len(homeDir)))

    # DONE
    return retVal


def list_save_games(operSys, saveGamePath, fileExt="zks"):
    '''
        PURPOSE - Provide a time-sorted list of all the save games in a given path, starting with
            the most recently modified
        INPUT
            operSys - See OPERATAING SYSTEM macros
            saveGamePath - Relative or absolute path to check for save games
            fileExt - File extension to look for (default: zks)
        OUTPUT
            On success, list of file names
            On failure, empty list
            On error, Exception
        NOTES
            This function will not add an periods (.) to the file extension
            This function will sort the file names so the most recent modification is first
    '''
    # LOCAL VARIABLES
    retVal = []  # List of file names sorted by modification time, descending
    supportedOS = supportedOSGlobal
    rawTupList = []  # Unsorted list of tuples
    sortBy = None  # Set this to ST_MTIME for *nix and ST_CTIME for Windows

    # INPUT VALIDATION
    if not isinstance(saveGamePath, str):
        raise TypeError('Save game path is of type "{}" instead of string'.format(type(saveGamePath)))
    elif len(saveGamePath) <= 0:
        raise ValueError("Invalid directory length")
    elif not isinstance(operSys, int):
        raise TypeError('Operating system is of type "{}" instead of integer'.format(type(operSys)))
    elif operSys not in supportedOS:
        raise ValueError("Operating system value is unknown")
    elif not isinstance(fileExt, str):
        raise TypeError('File extension is of type "{}" instead of string'.format(type(fileExt)))
    elif not os.path.isdir(saveGamePath):
        raise RuntimeError('Directory "{}" does not exist'.format(saveGamePath))

    # SET SORT BY
    if OS_LINUX == operSys or OS_APPLE == operSys:
        sortBy = ST_MTIME
    elif OS_WINDOWS == operSys:
        sortBy = ST_CTIME
    else:
        raise RuntimeError("Consider updating supportedOS list or control flow in list_save_games()")


    # GET THE SAVE GAME FILE LIST
    # Get the list of tuples
    rawTupList = [ (os.stat(os.path.join(saveGamePath, file)), file) for file in os.listdir(saveGamePath) if os.path.isfile(os.path.join(saveGamePath, file)) and file.endswith(fileExt) ]
    # Leave only regular files
    rawTupList = [ (stat[sortBy], file) for stat, file in rawTupList if S_ISREG(stat[ST_MODE]) ]
    # Sort the raw tuples into a file list
    retVal = [ sortedFile for stat, sortedFile in sorted(rawTupList, reverse=True) ]

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


def user_file_menu(operSys, saveGamePath, saveGameFileList):
    '''
        PURPOSE - Allow the user to choose a save game file to edit
        INPUT
            operSys - See OPERATAING SYSTEM macros
            saveGamePath - Relative or absolute path to check for save games
            saveGameFileList - Sorted list of save games found in saveGamePath
        OUTPUT
            On success, index of file selected from saveGameFileList
            On failure, -1
            On error, Exception
    '''
    # LOCAL VARIABLES
    retVal = -1
    supportedOS = supportedOSGlobal
    selection = 0  # Index into saveGameFileList
    page = 1  # Set of 10 save game files to display
    numFiles = 0  # Number of save games in list

    # GLOBAL VARIABLES
    global numBadAnswers

    # INPUT VALIDATION
    if not isinstance(operSys, int):
        raise TypeError('Operating system is of type "{}" instead of integer'.format(type(operSys)))
    elif operSys not in supportedOS:
        raise ValueError("Operating system value is unknown")
    elif not isinstance(saveGamePath, str):
        raise TypeError('Save game path is of type "{}" instead of string'.format(type(saveGamePath)))
    elif len(saveGamePath) <= 0:
        raise ValueError("Invalid directory length")
    elif not isinstance(saveGameFileList, list):
        raise TypeError('Save game file list is of type "{}" instead of list'.format(type(saveGameFileList)))
    elif len(saveGameFileList) <= 0:
        raise ValueError("Invalid file name list length")
    else:
        numFiles = len(saveGameFileList)

    # CLEAR SCREEN
    clear_screen(operSys)

    while numBadAnswers <= MAX_ERRS:
        # CLEAR SCREEN
        # clear_screen(operSys)

        print("")  # Blank line
        # print("Num files:\t{}".format(numFiles))  # DEBUGGING
        # print("Save Game #0:\t{}".format(saveGameFileList[0]))  # DEBUGGING

        # PRINT SAVE FILES
        # Verify files exist
        if numFiles > ((page - 1) * 10):
            # There's files
            for fileNum in range((page - 1) * 10, page * 10):
                if fileNum < numFiles:
                    print("#{}:\t{}".format(fileNum + 1, saveGameFileList[fileNum]))
                else:
                    print("")  # Print a blank line as a placeholder for missing files
            # break  # DEBUGGING
        else:
            # Not enough files
            # Print no more files to view
            pass
            # break  # DEBUGGING

        # NOTE: Print "end of list" or something similar when printing the last section
        if numFiles - (page * 10) <= numFiles % 10:
            # Last page
            print("<<< END OF LIST >>>")
        else:
            print("")  # Print a blank line to maintain vertical spacing

        # PRINT MENU
        print("")  # Blank line

        # Print options
        print("SAVE GAME SELECTION")
        print("Enter the number of the save game you want to edit")
        print("-or-")
        print('Type "top" to see the first page of files')
        print('Type "up" to see the previous page of files')
        print('Type "down" to see the next page of files')
        print('Type "bottom" to see the last page of files')
        print('Type "quit" to exit this program')

        # Take input
        selection = input("Make your selection [Down]:  ")

        # Modify input
        if len(selection) == 0:
            selection = "down"
        else:
            selection = selection.lower()

        # Execute selection
        if "top" == selection:
            page = 1
            numBadAnswers = 0
            clear_screen(operSys)
        elif "up" == selection:
            if 1 == page:
                print("\n<<< TOP OF LIST >>>")
                print("Invalid selection.  Try again.")
                numBadAnswers += 1
            else:
                page -= 1
                numBadAnswers = 0
                clear_screen(operSys)
        elif "down" == selection:
            if numFiles - (page * 10) <= numFiles % 10:
                print("\n<<< END OF LIST >>>")
                print("Invalid selection.  Try again.")
                numBadAnswers += 1
            else:
                page += 1
                numBadAnswers = 0
                clear_screen(operSys)
        elif "bottom" == selection:
            if 0 == numFiles % 10:
                page = int(((numFiles - (numFiles % 10)) / 10))
            else:
                page = int(((numFiles - (numFiles % 10)) / 10) + 1)
            numBadAnswers = 0
            clear_screen(operSys)
        elif "quit" == selection:
            numBadAnswers = 0
            retVal = -1
            break
        else:
            try:
                retVal = int(selection)
                retVal -= 1
            except Exception as err:
                print(repr(err))  # DEBUGGING
                print("\nInvalid selection.  Try again.")
                numBadAnswers += 1
            else:
                if retVal < 0 or retVal >= numFiles:
                    print("\nInvalid selection.  Try again.")
                    numBadAnswers += 1
                else:
                    break

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
    
    # CLEAR SCREEN
    clear_screen(operSys)

    while retVal and numBadAnswers <= MAX_ERRS:
        print("")  # Blank line
        # PRINT MENU
        # Print options
        print("SAVE GAME FILE MODIFICATIONS")
        print("Editing:\t{}\n".format(curSaveGame))
        print("(a) Change Build Points (BPs)")
        print("(b) Change Kingdom Stability")
        print("(c) Change gold")
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
        elif "a" == selection:
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
        elif "b" == selection:
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
        elif "c" == selection:
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
                # print("Current OS:\t{}".format(operSys))  # DEBUGGING
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

    # Template Code Block
    if retVal:
        try:
            pass
        except Exception as err:
            # print('_____() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            # retVal = False
            pass
        else:
            pass

    # DEBUGGING
    print("retVal:             \t{}".format(retVal))
    print("Operating system:   \t{}".format(operSys))
    print("Save game directory:\t{}".format(saveGamePath))
    # for file in saveGameFileList:
    #     print(file)

    # DONE
    return retVal


if __name__ == "__main__":
    if main():
        print("Success!")  # DEBUGGING
        pass
    else:
        print("FAIL!")  # DEBUGGING
        pass
