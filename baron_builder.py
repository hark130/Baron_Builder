#################################################
#################### IMPORTS ####################
#################################################

import pwd                                      # getpwuid
import os                                       # path.join, getuid, path.isdir
from stat import S_ISREG, ST_CTIME, ST_MODE, ST_MTIME
import sys                                      # version_info

#################################################
#################### MACROS #####################
#################################################

# OPERATING SYSTEM
OS_UNKNOWS = 0  # Unknows OS
OS_LINUX = 1    # All *nix
OS_WINDOWS = 2  # All Windows
OS_APPLE = 3    # All OS/?

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
nixSaveGamePath =  os.path.join(".config", "unity3d", "Owlcat Games", "Pathfinder Kingmaker", "Saved Games")
# Windows - C:\Users\user\AppData\LocalLow\Owlcat Games\Pathfinder Kingmaker\Saved Games
winSaveGamePath =  os.path.join("AppData", "LocalLow", "Owlcat Games", "Pathfinder Kingmaker", "Saved Games")
# Apple - /home/user/Library/Application\ Support/unity.Owlcat\ Games.Pathfinder\ Kingmaker/Saved\ Games 
macSaveGamePath =  os.path.join("Library", "Application Support", "unity.Owlcat Games.Pathfinder Kingmaker", "Saved Games")

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


def list_save_games(saveGamePath, operSys, fileExt="zks"):
    '''
        PURPOSE - Provide a time-sorted list of all the save games in a given path, starting with
            the most recently modified
        INPUT
            saveGamePath - Relative or absolute path to check for save games
            operSys - See OPERATAING SYSTEM macros
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


def main():
    # LOCAL VARIABLES
    retVal = True          # Indicates flow control success
    operSys = OS_UNKNOWS   # Operating system macro
    saveGamePath = ""      # Absolute path to save games
    saveGameFileList = []  # List of save game files

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

    # Parse Save Games
    if retVal:
        try:
            saveGameFileList = list_save_games(saveGamePath, operSys)
        except Exception as err:
            print('list_save_games() raised "{}" exception'.format(err.__str__()))  # DEBUGGING
            retVal = False
        else:
            if len(saveGameFileList) <= 0:
                print("Unable to locate any save game files in directory.")


    # Print Menu
    if retVal:
        pass

    # DEBUGGING
    print("retVal:             \t{}".format(retVal))
    print("Operating system:   \t{}".format(operSys))
    print("Save game directory:\t{}".format(saveGamePath))
    for file in saveGameFileList:
        print(file)

    # DONE
    return retVal


if __name__ == "__main__":
    if main():
        print("Success!")  # DEBUGGING
        pass
    else:
        print("FAIL!")  # DEBUGGING
        pass
