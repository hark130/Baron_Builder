'''
    PURPOSE - Organize all of the file management functionality implemented for Baron Builder
'''


#################################################
#################### IMPORTS ####################
#################################################

from baron_builder_imports import MAX_ERRS
from baron_builder_imports import nixSaveGamePath, winSaveGamePath, macSaveGamePath
from baron_builder_imports import OS_UNKNOWS, OS_LINUX, OS_WINDOWS, OS_APPLE
from baron_builder_imports import TOP_DIR, ARCHIVE_DIR, BACKUP_DIR, WORKING_DIR, BACKUP_EXT
from baron_builder_imports import supportedOSGlobal
from baron_builder_utilities import clear_screen
from stat import S_ISREG, ST_CTIME, ST_MODE, ST_MTIME
from zks_file_class import ZksFile
import os
import shutil
import sys


#################################################
#################### MACROS #####################
#################################################



#################################################
#################### GLOBALS ####################
#################################################



#################################################
################### FUNCTIONS ###################
#################################################


def user_file_menu(operSys, saveGamePath, saveGameFileList, curNumBadAns):
    '''
        PURPOSE - Top level menu leading to all file-related functionality
        INPUT
            operSys - See OPERATAING SYSTEM macros
            saveGamePath - Relative or absolute path to check for save games
            saveGameFileList - Sorted list of save games found in saveGamePath
            curNumBadAns - Current number of incorrect answers to track error tolerance
        OUTPUT
            On success...
                Open save game - index of file selected from saveGameFileList
                Backup save games - True
                Restore save games - True
                Archive save games - True
                Clean working directory - True
            On error, Exception
    '''
    # LOCAL VARIABLES
    retVal = True
    supportedOS = supportedOSGlobal
    fileNum = None                # Index of the user-selected file
    numBadAnswers = curNumBadAns  # Current number of bad answers
    selection = 0                 # User menu selection
    tempRetVal = 0                # File index to backup/archive
    backupZksFile = None          # ZksFile object to backup/archive
    workDirExists = None          # Set this to true if a working directory already existed
    zksWorkDir = ""               # Store the path of the full working directory here before ZksFile.close_zks()

    # GLOBAL VARIABLES

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
    elif not isinstance(curNumBadAns, int):
        raise TypeError('Current number of bad answers is of type "{}" instead of integer'.format(type(curNumBadAns)))
    elif curNumBadAns > MAX_ERRS:
        raise RuntimeError("Exceeded maximum bad answers")
    else:
        pass

    # CLEAR SCREEN
    clear_screen(operSys)

    # PRINT MENU
    while numBadAnswers <= MAX_ERRS:
        print("")  # Blank line
        # PRINT MENU
        # Print options
        print("SAVE GAME FILE MANAGEMENT")
        print("(a) Edit a save game")
        print("(b) Backup save game(s)")
        print("(c) Archive save game(s)")
        print("(d) Restore save game(s)")
        print("(e) Clean working directory")
        print("(f) Help")
        print("")
        print('Type "clear" to clear the screen')
        print('Type "quit" to exit this program')

        # Take input
        selection = input("Make your selection [a]:  ")
        clear_screen(operSys)

        # Modify input
        if len(selection) == 0:
            selection = "a"
        else:
            selection = selection.lower()

        # Execute selection
        if "clear" == selection:
            numBadAnswers = 0
            clear_screen(operSys)
        elif "quit" == selection:
            numBadAnswers = 0
            raise RuntimeError("Quit")
        elif "a" == selection:
            fileNum = user_file_selection_menu(operSys, saveGamePath, saveGameFileList, numBadAnswers)
            break
        elif "b" == selection:
            numBadAnswers = 0
            # Choose file to backup
            try:
                fileNum = user_file_selection_menu(operSys, saveGamePath, saveGameFileList, numBadAnswers)
            except Exception as err:
                print('user_file_selection_menu() raised "{}" exception'.format(str(err)))  # DEBUGGING
                retVal = False
                break
            else:
                if 0 > fileNum or fileNum >= len(saveGameFileList):
                    print("user_file_selection_menu() failed to return a proper file index")  # DEBUGGING
                    retVal = False
                    break
                else:
                    print("\nBacking up file:\t{}".format(saveGameFileList[fileNum]))
                    numBadAnswers = 0
            # Backup file
            try:
                retVal = backup_a_file(os.path.join(saveGamePath, saveGameFileList[fileNum]),
                                       os.path.join(saveGamePath, TOP_DIR, BACKUP_DIR), BACKUP_EXT)
            except Exception as err:
                print('backup_a_file() raised "{}" exception'.format(str(err)))  # DEBUGGING
                retVal = False
                break
            else:
                if retVal is False:
                    print("backup_a_file() failed to backup the file")  # DEBUGGING
                    break
                else:
                    print("Successfully backed up file")
        elif "c" == selection:
            print("Archive feature not yet implemented")  # PLACEHOLDER
            numBadAnswers += 1
            continue  # I don't want the half-implemented code (see below) executed yet
            # FUTURE NOTES
            # 1. Does working directory already exist?  If yes, leave it.  If no, clean up afterwards
            # 2. saveGame = ZksFile()
            # 3. saveGame.unpack_file(os.path.join(TOP_DIR, WORKING_DIR))
            # 4. saveGame.archive(os.path.join(TOP_DIR, ARCHIVE_DIR))
            # 5. Remove original save game from list of saves
            # 6. Delete original save game
            # The following code block was to be used for backup purposes until I decided to merely copy
            # backups and REcompress archives.  It's a start towards Feature 05 but it's not everything.
            tempRetVal = user_file_selection_menu(operSys, saveGamePath, saveGameFileList, numBadAnswers)
            try:
                backupZksFile = ZksFile(os.path.join(saveGamePath, saveGameFileList[tempRetVal]))
                if os.path.isdir(os.path.join(saveGamePath,TOP_DIR, WORKING_DIR, backupZksFile.zModDir)):
                    print("{} exists".format(os.path.join(saveGamePath,TOP_DIR, WORKING_DIR, backupZksFile.zModDir)))  # DEBUGGING
                    workDirExists = True
                else:
                    print("{} does not exist".format(os.path.join(saveGamePath,TOP_DIR, WORKING_DIR, backupZksFile.zModDir)))  # DEBUGGING
                    workDirExists = False
                backupZksFile.unpack_file(os.path.join(saveGamePath, TOP_DIR, WORKING_DIR))
                backupZksFile.archive(os.path.join(saveGamePath, TOP_DIR, BACKUP_DIR))
                zksWorkDir = backupZksFile.fullWorkPath
                backupZksFile.close_zks()
            except Exception as err:
                print('ZksFile() raised "{}" exception'.format(str(err)))  # DEBUGGING
                retVal = False
                break
            else:
                if workDirExists is False:
                    empty_a_dir(zksWorkDir)
                    remove_a_dir(zksWorkDir)
                    zksWorkDir = None
        elif "d" == selection:
            print("Restore feature not yet implemented")  # PLACEHOLDER
            numBadAnswers += 1
            continue
        elif "e" == selection:
            empty_a_dir(os.path.join(saveGamePath, TOP_DIR, WORKING_DIR))
        elif "f" == selection:
            print("A - 'Editing a save game' will allow you to modify certain aspects of that save file.")
            print("B - 'Backing up a save' will copy a save game file into a back up directory.\n    High speed but no compression.")
            print("C - 'Archiving a save' will move a save game into an archive directory.\n    Slow speed, some compression but this may speed up game load times.")
            print("D - 'Restore save games' will allow you to recover backup and archive save games, overwriting your current save.")
            print("E - 'Clean working directory' will manually clear the temporary files created during file manipulation.")
            print("F - I just wanted to give the user some insight into what is happening without lengthy documentation.")
            print("")
        else:
            print("\nInvalid selection.")
            numBadAnswers += 1
            if numBadAnswers <= MAX_ERRS:
                print("Try again.")

    # DONE
    if numBadAnswers > MAX_ERRS:
        raise RuntimeError("Exceeded maximum bad answers")

    return retVal


def user_file_selection_menu(operSys, saveGamePath, saveGameFileList, curNumBadAns):
    '''
        PURPOSE - Allow the user to choose a save game file to edit
        INPUT
            operSys - See OPERATAING SYSTEM macros
            saveGamePath - Relative or absolute path to check for save games
            saveGameFileList - Sorted list of save games found in saveGamePath
            curNumBadAns - Current number of incorrect answers to track error tolerance
        OUTPUT
            On success, index of file selected from saveGameFileList
            On error, Exception
        EXCEPTIONS
            Runtime("Quit") - User selects quit from menu without selecting a save game
    '''
    # LOCAL VARIABLES
    retVal = -1
    supportedOS = supportedOSGlobal
    selection = 0  # Index into saveGameFileList
    page = 1  # Set of 10 save game files to display
    numFiles = 0  # Number of save games in list
    numBadAnswers = curNumBadAns  # Current number of bad answers

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
    elif not isinstance(curNumBadAns, int):
        raise TypeError('Current number of bad answers is of type "{}" instead of integer'.format(type(curNumBadAns)))
    elif curNumBadAns > MAX_ERRS:
        raise RuntimeError("Exceeded maximum bad answers")
    else:
        numFiles = len(saveGameFileList)

    # CLEAR SCREEN
    clear_screen(operSys)

    while numBadAnswers <= MAX_ERRS:

        print("")  # Blank line

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
        print("Enter the number of the save game you want")
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
            raise RuntimeError("Quit")
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
    if numBadAnswers > MAX_ERRS:
        raise RuntimeError("Exceeded maximum bad answers")
    elif -1 == retVal:
        raise RuntimeError("Quit")

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
    try:
        if OS_LINUX == operSys:
            userName = os.environ["USER"]
            homeDir = os.environ["HOME"]
            relDir = nixSaveGamePath
        elif OS_WINDOWS == operSys:
            userName = os.environ["USERNAME"]
            homeDir = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"])
            relDir = winSaveGamePath
        elif OS_APPLE == operSys:
            userName = os.environ["USER"]
            homeDir = os.environ["HOME"]
            relDir = macSaveGamePath
    except Exception as err:
        print(repr(err))  # DEBUGGING
        userName = ""
        homeDir = ""
        relDir = ""

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


def empty_a_dir(oldPath):
    '''
        PURPOSE - Empty an old directory of all files and directories without deleting it
        INPUT
            oldPath - Directory to empty
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTE
            This function is recursive.
            It is also recursive.
    '''
    # LOCAL VARIABLES
    retVal = True

    # INPUT VALIDATION
    if not isinstance(oldPath, str):
        raise TypeError('Old path is of type "{}" instead of string'.format(type(oldPath)))
    elif len(oldPath) <= 0:
        raise ValueError("Invalid path length")
    elif not os.path.exists(oldPath):
        raise OSError("Path does not exist")
    elif not os.path.isdir(oldPath):
        raise OSError("Path is not a path")

    # EMPTY DIRECTORY
    print("Cleaning Up [", end = "")
    sys.stdout.flush()
    for entry in os.listdir(oldPath):
        if retVal is False:
            break

        if os.path.isdir(os.path.join(oldPath, entry)):
            # print("Removing dir {}".format(os.path.join(oldPath, entry)))  # DEBUGGING
            retVal = remove_a_dir(os.path.join(oldPath, entry))
            if retVal is False:
                print("X", end = "")
                sys.stdout.flush()
                break
            else:
                print(".", end = "")
                sys.stdout.flush()
        elif os.path.isfile(os.path.join(oldPath, entry)):
            # print("Removing file {}".format(os.path.join(oldPath, entry)))  # DEBUGGING
            os.remove(os.path.join(oldPath, entry))
            print(".", end = "")
            sys.stdout.flush()
        else:
            print("X]")
            sys.stdout.flush()
            raise OSError("Entry {} is not a file or directory".format(os.path.join(oldPath, entry)))
    print("]")
    sys.stdout.flush()

    # DONE
    return retVal


def remove_a_dir(oldPath):
    '''
        PURPOSE - Empty an old directory of all files and directories
        INPUT
            oldPath - Directory to empty
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTE
            This function is recursive.
            It is also recursive.
    '''
    # LOCAL VARIABLES
    retVal = True

    # INPUT VALIDATION
    if not isinstance(oldPath, str):
        raise TypeError('Old path is of type "{}" instead of string'.format(type(oldPath)))
    elif len(oldPath) <= 0:
        raise ValueError("Invalid path length")
    elif not os.path.exists(oldPath):
        raise OSError("Path does not exist")
    elif not os.path.isdir(oldPath):
        raise OSError("Path is not a path")
    else:
        # REMOVE DIRECTORY
        shutil.rmtree(oldPath)

    # DONE
    return retVal


def copy_a_file(srcFile, dstFile):
    '''
        PURPOSE - Copy srcFile to dstFile
        INPUT
            srcFile - Relative or absolute filename original file
            dstFile - Relative or absolute filename of the copy
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
    '''
    # LOCAL VARIABLES
    retVal = False
    
    # INPUT VALIDATION
    if not isinstance(srcFile, str):
        raise TypeError('Source file is of type "{}" instead of string'.format(type(srcFile)))
    elif len(srcFile) <= 0:
        raise ValueError("Invalid source file name length")
    elif not isinstance(dstFile, str):
        raise TypeError('Source file is of type "{}" instead of string'.format(type(dstFile)))
    elif len(dstFile) <= 0:
        raise ValueError("Invalid destination file name length")
    elif srcFile == dstFile:
        raise ValueError("Source and destination can not be the same")
    elif os.path.exists(srcFile) is False:
        raise OSError("Source file does not exist")
    elif os.path.isfile(srcFile) is False:
        raise OSError("Source file is not a file")
    elif os.path.exists(dstFile) is True:
        raise OSError("Destination file already exists")
    
    # COPY
    try:
        shutil.copy2(srcFile, dstFile)
    except Exception as err:
        print("shutil.copy2() raised an exception")  # DEBUGGING
        print(repr(err))  # DEBUGGING
        retVal = False
    else:
        retVal = True
    
    # DONE
    return retVal


def backup_a_file(srcFile, dstDir, newFileExt):
    '''
        PURPOSE - Copy a file to a new destination directory while also modifying its file extension
        INPUT
            srcFile - Relative or absolute filename original file
            dstDir - Relative or absolute directory to copy the file into
            newFileExt - New file extension to replace the old file extension
        OUTPUT
            On success, True
            on failure, False
            on error, Exception
    '''
    # LOCAL VARIABLES
    retVal = False
    splitFile = ()    # Split the srcFile here
    curFileExt = ""   # Store the current srcFile file extension, if any, here
    dstFilename = ""  # Construct the destination file name, complete with new file extension, here
    
    # INPUT VALIDATION
    if not isinstance(srcFile, str):
        raise TypeError('Source file is of type "{}" instead of string'.format(type(srcFile)))
    elif len(srcFile) <= 0:
        raise ValueError("Invalid source file name length")
    elif not isinstance(dstDir, str):
        raise TypeError('Source file is of type "{}" instead of string'.format(type(dstDir)))
    elif len(dstDir) <= 0:
        raise ValueError("Invalid destination file name length")
    elif not isinstance(newFileExt, str):
        raise TypeError('File extension is of type "{}" instead of string'.format(type(dstDir)))
    elif len(newFileExt) <= 0:
        raise ValueError("Invalid file extension length")
    elif os.path.exists(srcFile) is False:
        raise OSError("Source file does not exist")
    elif os.path.isfile(srcFile) is False:
        raise OSError("Source file is not a file")

    # MANAGE BACKUP DIRECTORY
    # If it exists, verify it's a directory
    if os.path.exists(dstDir) is True:
        if os.path.isdir(dstDir) is False:
            raise OSError("Destination directory is not a directory")
    else:
        os.mkdir(dstDir)
    
    # DETERMINE FILE EXTENSION
    splitFile = os.path.splitext(srcFile)
    curFileExt = splitFile[len(splitFile) - 1]
    
    # JOIN DESTINATION FILENAME
    dstFilename = os.path.basename(srcFile)
    if 0 < len(curFileExt):
        dstFilename = dstFilename + newFileExt
    else:
        dstFilename = dstFilename.replace(curFileExt, newFileExt)
        
    # COPY
    try:
        retVal = copy_a_file(srcFile, os.path.join(dstDir, dstFilename))
    except Exception as err:
        print("copy_a_file() raised an exception")  # DEBUGGING
        print(repr(err))  # DEBUGGING
        retVal = False
    else:
        if retVal is False:
            print("copy_a_file() failed")  # DEBUGGING
            pass        
    
    # DONE
    return retVal

