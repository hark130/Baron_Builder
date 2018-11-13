'''
    PURPOSE - Organize all of the file management functionality implemented for Baron Builder
'''


#################################################
#################### IMPORTS ####################
#################################################

from baron_builder_imports import MAX_ERRS
from baron_builder_imports import nixSaveGamePath, winSaveGamePath, macSaveGamePath
from baron_builder_imports import saveGameJson, backGameJson, archGameJson
from baron_builder_imports import OS_UNKNOWS, OS_LINUX, OS_WINDOWS, OS_APPLE
from baron_builder_imports import TOP_DIR, ARCHIVE_DIR, BACKUP_DIR, WORKING_DIR
from baron_builder_imports import ARCHIVE_EXT, BACKUP_EXT, MISC_BACKUP_EXT, SAVE_GAME_EXT
from baron_builder_imports import supportedOSGlobal
from baron_builder_utilities import clear_screen
from collections import OrderedDict
# from copy import deepcopy
from json_file_class import JsonFile
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


def user_file_menu(operSys, saveGamePath, oldSaveGameFileList, curNumBadAns):
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
    fileNum = None                          # Index of the user-selected file
    numBadAnswers = curNumBadAns            # Current number of bad answers
    selection = 0                           # User menu selection
    tempRetVal = 0                          # File index to backup/archive
    backupZksFile = None                    # ZksFile object to backup/archive
    workDirExists = None                    # Set this to true if a working directory already existed
    zksWorkDir = ""                         # Store the path of the full working directory here before ZksFile.close_zks()
    userQuit = False                        # Set this to True if the user wants to quit
    saveGameFileList = oldSaveGameFileList  # Current list of save games in directory - Update on deletes
    backGameFileList = []                   # Current list of backed up save games - Update on deletes
    saveGamesChanged = False                # Set this to True if list of save games on disk ever change
    backGamesChanged = False                # Set this to True if list of backed up save games on disk ever change
    gameJsonFile = ""                       # Full path to the PKM save game list json file
    backJsonFile = ""                       # Full path to the Baron Builder backup save game list json file
    archJsonFile = ""                       # Full path to the Baron Builder archive save game list json file
    backupGamePath = ""                     # Full path to the Baron Builder backup directory


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
        gameJsonFile = os.path.join(saveGamePath, "..", saveGameJson)
        backJsonFile = os.path.join(saveGamePath, TOP_DIR, BACKUP_DIR, backGameJson)
        archJsonFile = os.path.join(saveGamePath, TOP_DIR, ARCHIVE_DIR, archGameJson)
        backupGamePath = os.path.join(saveGamePath, TOP_DIR, BACKUP_DIR)

    # CLEAR SCREEN
    clear_screen(operSys)

    # PREPARE BACKUP DIRECTORY
    start_storage_dir(backupGamePath, backGameJson)

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
            userQuit = True
        elif "a" == selection:
            try:
                fileNum = user_file_selection_menu(operSys, saveGamePath, saveGameFileList, numBadAnswers)
            except RuntimeError as err:
                if str(err) == "Quit":
                    userQuit = True
            except Exception as err:
                print('user_file_selection_menu() raised "{}" exception'.format(str(err)))  # DEBUGGING
                retVal = False
            else:
                retVal = fileNum
                break
        elif "b" == selection:
            numBadAnswers = 0
            # Choose file to backup
            try:
                fileNum = user_file_selection_menu(operSys, saveGamePath, saveGameFileList, numBadAnswers)
            except RuntimeError as err:
                if str(err) == "Quit":
                    userQuit = True
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
                    clear_screen(operSys)
                    print("\nBacking up file:\t{}".format(saveGameFileList[fileNum]))
                    numBadAnswers = 0

            # Backup file
            try:
                retVal = backup_a_file(os.path.join(saveGamePath, saveGameFileList[fileNum]),
                                       backupGamePath, BACKUP_EXT, srcJson=gameJsonFile, dstJson=backJsonFile)
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
            numBadAnswers = 0
            # Choose file to archive
            try:
                fileNum = user_file_selection_menu(operSys, saveGamePath, saveGameFileList, numBadAnswers)
            except RuntimeError as err:
                if str(err) == "Quit":
                    userQuit = True
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
                    clear_screen(operSys)
                    print("\nArchiving file:\t{}".format(saveGameFileList[fileNum]))
                    numBadAnswers = 0
                    # Archive file
                    try:
                        retVal = archive_a_file(saveGamePath,
                                                os.path.join(saveGamePath, saveGameFileList[fileNum]),
                                                os.path.join(saveGamePath, TOP_DIR, ARCHIVE_DIR),
                                                srcJson=gameJsonFile, dstJson=archJsonFile)
                    except Exception as err:
                        print('archive_a_file() raised "{}" exception'.format(str(err)))  # DEBUGGING
                        retVal = False
                        break
                    else:
                        if retVal is False:
                            print("archive_a_file() failed to archive the file")  # DEBUGGING
                            break
                        else:
                            print("Successfully archived file")
                            saveGamesChanged = True
        elif "d" == selection:
            numBadAnswers = 0
            try:
                user_restore_menu(operSys, saveGamePath, numBadAnswers)
            except RuntimeError as err:
                if "Quit" == str(err):
                    userQuit = True
                elif "Exit" == str(err):
                    clear_screen(operSys)
                    continue
                else:
                    raise err
            except Exception as err:
                print('user_file_selection_menu() raised "{}" exception'.format(str(err)))  # DEBUGGING
                retVal = False
                break
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

        if userQuit is True:
            raise RuntimeError("Quit")

        if saveGamesChanged is True:
            # Update save game file list in case save games were deleted
            saveGameFileList = list_save_games(operSys, saveGamePath)
            saveGamesChanged = False

        if backGamesChanged is True:
            # Update save game file list in case save games were deleted
            backGameFileList = list_save_games(operSys, backupGamePath, fileExt=BACKUP_EXT)
            backGamesChanged = False

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


def user_restore_menu(operSys, saveGamePath, curNumBadAns):
    '''
        PURPOSE - Extricate restore functionality into a restore sub-menu
        INPUT
            operSys - See OPERATAING SYSTEM macros
            saveGamePath - Relative or absolute path to check for save games
            curNumBadAns - Current number of incorrect answers to track error tolerance
        OUTPUT
            On error, Exception
        EXCEPTIONS
            Runtime("Exit") - User selected exit from menu
            Runtime("Quit") - User selected quit from menu
    '''
    # LOCAL VARIABLES
    numBadAnswers = curNumBadAns  # Current number of bad answers
    selection = ""                # User selection from "RESTORE" menu
    userExit = False              # Set this to True if the user wants to return to the previous menu
    userQuit = False              # Set this to True if the user wants to quit
    readFiles = False             # Set this to True if it's time to select files
    typeFile = ""                 # Dynamic string to aid in user feedback (e.g., backup, archive)
    gameJsonFile = ""             # Full path to the PKM save game list json file
    backJsonFile = ""             # Full path to the Baron Builder backup save game list json file
    archJsonFile = ""             # Full path to the Baron Builder archive save game list json file
    archGamePath = ""             # Path to the archived save games
    backGamePath = ""             # Path to the backed up save games
    workGamePath = ""             # Path to the Baron Builder working directory
    archZksFileObj = None         # ZksFile object of archived save game
    # Dynamic Variables
    # These variables could be updated each while loop
    fileNum = None                # Index of the user-selected file
    restoreGamePath = ""          # Path to backed up or archived save games
    restoreGameList = []          # List of save games found in restoreGamePath
    restoreJsonFile = ""          # Full path to the Baron Builder save game list json file to restore from
    archGameList = []             # List of available archived games to restore
    backGameList = []             # List of available backed up games to restore
    numArchGames = 0              # Number of available archive games
    numBackGames = 0              # Number of available backed up games
    copiedList = []               # Return value from copy_save_game_from_list()

    # INPUT VALIDATION
    # Save Game List Json Files
    archJsonFile = os.path.join(saveGamePath, TOP_DIR, ARCHIVE_DIR, archGameJson)
    backJsonFile = os.path.join(saveGamePath, TOP_DIR, BACKUP_DIR, backGameJson)
    gameJsonFile = os.path.join(saveGamePath, "..", saveGameJson)
    # Baron Builder Save Game Directories
    archGamePath = os.path.join(saveGamePath, TOP_DIR, ARCHIVE_DIR)
    backGamePath = os.path.join(saveGamePath, TOP_DIR, BACKUP_DIR)
    workGamePath = os.path.join(saveGamePath, TOP_DIR, WORKING_DIR)

    # CLEAR SCREEN
    clear_screen(operSys)

    while numBadAnswers <= MAX_ERRS:
        # UPDATE DYNAMIC VARIABLES
        try:
            archGameList = list_save_games(operSys, archGamePath, fileExt=ARCHIVE_EXT)
        except OSError:
            archGameList = []
        try:
            backGameList = list_save_games(operSys, backGamePath, fileExt=BACKUP_EXT)
        except OSError:
            backGameList = []
        numArchGames = len(archGameList)
        numBackGames = len(backGameList)

        # PRINT MENU
        print("")  # Blank line

        # Print options
        print("RESTORE SAVE GAME SELECTION")
        print("What type of save game do you want to restore?")
        print("(a) Backup [{} files]".format(numBackGames))
        print("(b) Archive [{} files]".format(numArchGames))
        print("-or-")
        print('Type "clear" to clear the screen')
        print('Type "exit" to return to the previous menu')
        print('Type "quit" to exit this program')

        # Take input
        selection = input("Make your selection [Backup]:  ")

        # Modify input
        if len(selection) == 0:
            selection = "a"
        else:
            selection = selection.lower()

            # Translate human answers into scantron answers
            if "backup" == selection:
                selection = "a"
            elif "archive" == selection:
                selection = "b"

        # Execute selection
        if "clear" == selection:
            numBadAnswers = 0
            clear_screen(operSys)
            readFiles = False
        elif "exit" == selection:
            numBadAnswers = 0
            userExit = True
            readFiles = False
        elif "quit" == selection:
            numBadAnswers = 0
            userQuit = True
            readFiles = False
        elif "a" == selection:
            numBadAnswers = 0
            restoreGamePath = backGamePath
            restoreGameList = backGameList
            restoreJsonFile = backJsonFile
            typeFile = "backup"
            readFiles = True
        elif "b" == selection:
            numBadAnswers = 0
            restoreGamePath = archGamePath
            restoreGameList = archGameList
            restoreJsonFile = archJsonFile
            typeFile = "archive"
            readFiles = True
        else:
            print("\nInvalid selection.")
            numBadAnswers += 1
            if numBadAnswers <= MAX_ERRS:
                print("Try again.")

        if readFiles is True and userExit is False and userQuit is False:
            # Validate selection
            if 0 >= len(restoreGameList):
                print("\nThere are no {} files to restore.".format(typeFile))
                numBadAnswers += 1
                if numBadAnswers <= MAX_ERRS:
                    print("Try again.")
                continue

            # Allow user to choose a save game to restore
            try:
                fileNum = user_file_selection_menu(operSys, restoreGamePath, restoreGameList, numBadAnswers)
            except RuntimeError as err:
                if "Quit" == str(err):
                    userQuit = True
                elif "Exit" == str(err):
                    clear_screen(operSys)
                    continue
                else:
                    raise err
            except Exception as err:
                print('user_file_selection_menu() raised "{}" exception'.format(str(err)))  # DEBUGGING
                break
            else:
                if 0 > fileNum or fileNum >= len(restoreGameList):
                    print("user_file_selection_menu() failed to return a proper file index")  # DEBUGGING
                    break
                else:
                    # Restore the backed up file
                    clear_screen(operSys)
                    print("\nRestoring {} file:\t{}".format(typeFile, restoreGameList[fileNum]))
                    numBadAnswers = 0
                    if backup_a_file(gameJsonFile, backGamePath, MISC_BACKUP_EXT, overwrite=True) is False:
                        print("backup_a_file() failed to backup {}".format(backJsonFile))  # DEBUGGING
                        pass
                    # Restore file
                    # Backup
                    if "a" == selection:
                        try:
                            retVal = backup_a_file(os.path.join(restoreGamePath, restoreGameList[fileNum]),
                                                   saveGamePath, SAVE_GAME_EXT, srcJson=restoreJsonFile, dstJson=gameJsonFile,
                                                   overwrite=True)
                        except Exception as err:
                            print('backup_a_file() raised "{}" exception'.format(str(err)))  # DEBUGGING
                            retVal = False
                            break
                        else:
                            if retVal is False:
                                print("backup_a_file() failed to restore the {} file".format(typeFile))  # DEBUGGING
                                break
                            else:
                                print("Successfully restored {} file".format(typeFile))
                    elif "b" == selection:
                        try:
                            archZksFileObj = ZksFile(os.path.join(restoreGamePath, restoreGameList[fileNum]))
                            if archZksFileObj.unpack_file(workGamePath) is not True:
                                print("ZksFile.unpack_file() failed on the {} file".format(typeFile))  # DEBUGGING
                                retVal = False
                                break
                            if archZksFileObj.unarchive_file(saveGamePath) is not True:
                                print("ZksFile.unarchive_file() failed on the {} file".format(typeFile))  # DEBUGGING
                                retVal = False
                                break
                            if archZksFileObj.close_zks() is not True:
                                print("ZksFile.close_zks() failed")  # DEBUGGING
                                retVal = False
                                break
                        except Exception as err:
                            print('ZksFile object raised "{}" exception'.format(str(err)))  # DEBUGGING
                            retVal = False
                            break
                        else:
                            # GET ITEM FROM OLD JSON FILE
                            try:
                                copiedList = copy_save_game_from_list(archJsonFile, os.path.basename(restoreGameList[fileNum]))
                            except Exception as err:
                                print("copy_save_game_from_list() failed to copy {} from {}".format(os.path.basename(restoreGameList[fileNum]), archJsonFile))  # DEBUGGING
                                print(repr(err))
                                retVal = False
                                break
                            else:
                                # print("Copied List:\t{}".format(copiedList))  # DEBUGGING
                                pass

                            # ADD TO NEW JSON FILE
                            if isinstance(copiedList, list) and 0 < len(copiedList):
                                try:
                                    add_save_game_to_list(gameJsonFile, copiedList)
                                except Exception as err:
                                    print("add_save_game_to_list() failed to add {} to {}".format(copiedList, os.path.basename(gameJsonFile)))  # DEBUGGING
                                    print(repr(err))
                                    retVal = False
                                    break

                            print("Successfully restored {} file".format(typeFile))

        if userExit is True:
            raise RuntimeError("Exit")

        if userQuit is True:
            raise RuntimeError("Quit")

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
    retVal = []      # List of file names sorted by modification time, descending
    supportedOS = supportedOSGlobal
    rawTupList = []  # Unsorted list of tuples
    sortBy = None    # Set this to ST_MTIME for *nix and ST_CTIME for Windows

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
        raise OSError('Directory "{}" does not exist'.format(saveGamePath))

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
        PURPOSE - Empty an old directory of all files and directories and remove it
        INPUT
            oldPath - Directory to empty and remove
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


def copy_a_file(srcFile, dstFile, overwrite=False):
    '''
        PURPOSE - Copy srcFile to dstFile
        INPUT
            srcFile - Relative or absolute filename original file
            dstFile - Relative or absolute filename of the copy
            overwrite - Will delete destination file if it exists
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
    elif os.path.exists(dstFile) is True and overwrite is False:
        raise OSError("Destination file already exists")
    elif not isinstance(overwrite, bool):
        raise TypeError('Overwrite is of type "{}" instead of bool'.format(type(overwrite)))
    
    # DELETE?
    if overwrite is True and os.path.exists(dstFile):
        try:
            # File
            if os.path.isfile(dstFile):
                os.remove(dstFile)
            # Directory
            elif os.path.isdir(dstFile):
                remove_a_dir(dstFile)
        except Exception as err:
            print("Deleting existing destination file failed")  # DEBUGGING
            print(repr(err))  # DEBUGGING
            retVal = False

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


def backup_a_file(srcFile, dstDir, newFileExt, srcJson=None, dstJson=None, overwrite=False):
    '''
        PURPOSE - Copy a file to a new destination directory while also modifying its file extension
        INPUT
            srcFile - Relative or absolute filename original file
            dstDir - Relative or absolute directory to copy the file into
            newFileExt - New file extension to replace the old file extension
            srcJson - Source save game list json file to remove the entry from
            dstJson - Destination save game list json file to add the entry to
            overwrite - Will delete destination file if it exists
        OUTPUT
            On success, True
            on failure, False
            on error, Exception
    '''
    # LOCAL VARIABLES
    retVal = False
    splitFile = ()        # Split the srcFile here
    curFileExt = ""       # Store the current srcFile file extension, if any, here
    dstFilename = ""      # Construct the destination file name, complete with new file extension, here
    destinationJson = ""  # os.path.basename(dstJson) or backGameJson... whichever is not None first
    copiedList = []       # List of copied entries; Return value from copy_save_game_from_list()
    
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
    elif not isinstance(overwrite, bool):
        raise TypeError('Overwrite is of type "{}" instead of bool'.format(type(overwrite)))
    else:
        if dstJson is None:
            destinationJson = backGameJson
        else:
            destinationJson = os.path.basename(dstJson)
    
    # DETERMINE FILE EXTENSION
    splitFile = os.path.splitext(srcFile)
    curFileExt = splitFile[len(splitFile) - 1]
    # print("Current file extension for {}:\t{}".format(srcFile, curFileExt))  # DEBUGGING
    
    # JOIN DESTINATION FILENAME
    dstFilename = os.path.basename(srcFile)
    if 0 >= len(curFileExt):
        dstFilename = dstFilename + newFileExt
    else:
        dstFilename = dstFilename.replace(curFileExt, newFileExt)
        
    # COPY
    try:
        retVal = copy_a_file(srcFile, os.path.join(dstDir, dstFilename), overwrite)
    except Exception as err:
        print("copy_a_file() raised an exception")  # DEBUGGING
        print(repr(err))  # DEBUGGING
        retVal = False
    else:
        if retVal is False:
            print("copy_a_file() failed")  # DEBUGGING
            pass

    # GET ITEM FROM OLD JSON FILE
    if retVal is True and srcJson is not None:
        try:
            copiedList = copy_save_game_from_list(srcJson, os.path.basename(srcFile))
        except Exception as err:
            print("copy_save_game_from_list() failed to copy {} from {}".format(os.path.basename(srcFile), srcJson))  # DEBUGGING
            print(repr(err))
            retVal = False
        else:
            # print("Copied List:\t{}".format(copiedList))  # DEBUGGING
            pass

    # ADD TO NEW JSON FILE
    if retVal is True and dstJson is not None and isinstance(copiedList, list) and 0 < len(copiedList):
        try:
            add_save_game_to_list(dstJson, copiedList)
        except Exception as err:
            print("add_save_game_to_list() failed to add {} to {}".format(copiedList, os.path.basename(dstJson)))  # DEBUGGING
            print(repr(err))
            retVal = False

    # DONE
    return retVal


def archive_a_file(saveGamePath, srcFile, dstDir, srcJson=None, dstJson=None):
    '''
        PURPOSE - Archive a file to a new destination directory while also modifying its file extension
            and deleting the original
        INPUT
            saveGamePath - Relative or absolute path to check for save games
            srcFile - Relative or absolute filename original file
            dstDir - Relative or absolute directory to archive the file into
            srcJson - Source save game list json file to remove the entry from
            dstJson - Destination save game list json file to add the entry to
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTES
            The orginal steam-saves-release.json will be backed up, changing .json to .bak.  Any
                existing backed up copies will be overwritten.
    '''
    # LOCAL VARIABLES
    retVal = True          # Set this to False if anything fails
    tempRetVal = False     # Check return values
    splitFile = ()         # Split the srcFile here
    archiveZksFile = None  # ZksFile object to archive remove archived save game from
    saveGameJsonPath = os.path.join(saveGamePath, "..", saveGameJson)
    workDir = os.path.join(saveGamePath, TOP_DIR, WORKING_DIR)
    backDir = os.path.join(saveGamePath, TOP_DIR, BACKUP_DIR)
    archDir = os.path.join(saveGamePath, TOP_DIR, ARCHIVE_DIR)
    archGameJsonPath = os.path.join(archDir, archGameJson)
    thisWorkDir = None     # Store the source file's full working directory here
    workDirExists = False  # Determine if the working directory existed before ZksFile.unpack_file()
    removedList = []       # List of removed entries; Return value from remove_save_game_from_list()

    # INPUT VALIDATION
    if not isinstance(srcFile, str):
        raise TypeError('Source file is of type "{}" instead of string'.format(type(srcFile)))
    elif len(srcFile) <= 0:
        raise ValueError("Invalid source file name length")
    elif not isinstance(dstDir, str):
        raise TypeError('Source file is of type "{}" instead of string'.format(type(dstDir)))
    elif len(dstDir) <= 0:
        raise ValueError("Invalid destination file name length")
    elif os.path.exists(srcFile) is False:
        raise OSError("Source file does not exist")
    elif os.path.isfile(srcFile) is False:
        raise OSError("Source file is not a file")

    # MANAGE BACKUP DIRECTORY
    start_storage_dir(archDir, archGameJson)

    # ARCHIVE FILE
    try:
        # 1. OPEN SAVE GAME AS ZksFile object
        archiveZksFile = ZksFile(srcFile)
        thisWorkDir = os.path.join(TOP_DIR, WORKING_DIR, archiveZksFile.zModDir)
        # 2. DETERMINE WORKING DIRECTORY STATUS
        if os.path.exists(thisWorkDir) is True:
            if os.path.isdir(thisWorkDir) is True:
                workDirExists = True
            else:
                raise OSError("Working directory is actually a file?!")
        # 3. REPACK THE FILE
        tempRetVal = archiveZksFile.unpack_file(os.path.join(saveGamePath, TOP_DIR, WORKING_DIR))
        if tempRetVal:
            tempRetVal = archiveZksFile.archive_file(dstDir)
            if tempRetVal is False:
                raise OSError("ZksFile object failed to archive the source file")
            else:
                archiveZksFile.close_zks()
        else:
            raise OSError("ZksFile object failed to unpack file being archived")
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    try:
        # 4. REMOVE FROM SAVE GAME LIST
        # Backup save game file
        tempRetVal = backup_a_file(saveGameJsonPath, backDir, MISC_BACKUP_EXT, overwrite=True)
        if tempRetVal is False:
            raise OSError("Failed to backup {}".format(saveGameJson))
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # 4. GET ITEM FROM OLD JSON FILE
    if retVal is True and srcJson is not None:
        try:
            removedList = remove_save_game_from_list(srcJson, os.path.basename(srcFile))
        except Exception as err:
            print("remove_save_game_from_list() failed to copy {} from {}".format(os.path.basename(srcFile), srcJson))  # DEBUGGING
            print(repr(err))
            retVal = False
        else:
            print("Removed List:\t{}".format(removedList))  # DEBUGGING
            pass

    # 5. ADD TO NEW JSON FILE
    if retVal is True and dstJson is not None and isinstance(removedList, list) is True and 0 < len(removedList):
        try:
            add_save_game_to_list(dstJson, removedList)
        except Exception as err:
            print("add_save_game_to_list() failed to add {} to {}".format(removedList, os.path.basename(dstJson)))  # DEBUGGING
            print(repr(err))
            retVal = False

    # 6. DELETE THE ORIGINAL
    try:
        os.remove(srcFile)
    except Exception as err:
        print("Failed to remove original save game file:\t{}".format(srcFile))  # DEBUGGING
        print(repr(err))  # DEBUGGING
        raise err

    # 7. DELETE WORKING DIRECTORY?
    if workDirExists:
        try:
            print("ABOUT TO EMPTY {}".format(thisWorkDir))  # DEBUGGING
            # empty_a_dir(thisWorkDir)
            print("ABOUT TO DELETE {}".format(thisWorkDir))  # DEBUGGING
            # remove_a_dir(thisWorkDir)
        except Exception as err:
            print("Failed to remove original save game file:\t{}".format(srcFile))  # DEBUGGING
            print(repr(err))  # DEBUGGING
            raise err

    # DONE
    return retVal


def add_save_game_to_list(absSaveGameList, newSaveGame):
    '''
        PURPOSE - Add one save game, or list of save games, to the stored list of save games
        INPUT
            absSaveGameList - Relative or absolute path to the json file storing the list of save games
            newSaveGame - OrderedDict, or list of OrderedDicts, of save game(s) to add to the list
        OUTPUT
            On failure or error, Exception
    '''
    # LOCAL VARIABLES
    saveGameList = []                          # List of save games to add to existing list
    newGameFilenameList = []                   # List of new filenames parse from saveGameList
    existFilenameList = []                     # List of existing filenames parsed from absSaveGameList
    sgjJsonFileObj = None                      # Store the JsonFile object here
    mandatoryKeys = [ "Filename", "Version" ]  # Mandatory keys for each save game list entry
    sgjJsonDict = OrderedDict()                # Store the sgjJsonFileObj.jDict["Files"] here to modify
    asglVersion = 0                            # Version of the absSaveGameList
    highVersion = 0                            # Highest version from the newSaveGames

    # INPUT VALIDATION
    # absSaveGameList
    if not isinstance(absSaveGameList, str):
        raise TypeError('Save game list name is of type "{}" instead of string'.format(type(absSaveGameList)))
    elif 0 >= len(absSaveGameList):
        raise ValueError("Invalid save game list name length")
    elif os.path.exists(absSaveGameList) is False:
        raise OSError("Save game list json file does not exist")
    elif os.path.isfile(absSaveGameList) is False:
        raise OSError("Save game list json file is not a file")

    # newSaveGame
    if isinstance(newSaveGame, OrderedDict):
        saveGameList.append(newSaveGame)
    elif isinstance(newSaveGame, list):
        saveGameList = newSaveGame
    else:
        raise TypeError('Save game name is of type "{}" instead of OrderedDict or list'.format(type(newSaveGame)))

    # saveGameName entries
    for oDict in saveGameList:
        if not isinstance(oDict, OrderedDict):
            print("oDict is :\t{}".format(oDict))  # DEBUGGING
            print("oDict is type:\t{}".format(type(oDict)))  # DEBUGGING
            raise TypeError("Save game list contains non-OrderedDict")
        elif 2 != len(oDict):
            raise ValueError("Save game list contains an OrderedDict of improper length")
        else:
            for entry in oDict.keys():
                if not isinstance(entry, str):
                    raise TypeError("Save game list contains an OrderedDict with a non-string key")
                else:
                    if entry == "Filename":
                        if not isinstance(oDict[entry], str):
                            raise TypeError("Save game list contains an OrderedDict with a non-string filename")
                        elif 0 >= len(oDict[entry]):
                            raise ValueError("Save game list contains an OrderedDict with an empty filename")
                        else:
                            if oDict[entry] != os.path.basename(oDict[entry]):
                                raise ValueError("Save game list contains an OrderedDict with a path/filename")
                            else:
                                newGameFilenameList.append(oDict[entry])
                    elif entry == "Version":
                        if not isinstance(oDict[entry], int):
                            raise TypeError("Save game list contains an OrderedDict with a non-int version")
                        else:
                            if oDict[entry] > highVersion:
                                highVersion = oDict[entry]
                    else:
                        raise TypeError("Save game list contains an OrderedDict with an errant/unexpected key:\t{}".format(entry))

    # PARSE JSON FILE
    # Load json file
    try:
        sgjJsonFileObj = JsonFile(absSaveGameList)
        if sgjJsonFileObj.jSuccess:
            if sgjJsonFileObj.read_json_file() is False:
                raise RuntimeError("Failed to read json file")
            if sgjJsonFileObj.parse_json_contents() is False:
                raise RuntimeError("Failed to parse json file contents")
        else:
            raise RuntimeError("Failed to instantiate JsonFile object")
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # Add save games
    try:
        # Get existing list of OrderedDicts
        sgjJsonDict = sgjJsonFileObj.get_data("Files")
        # Parse list of OrderedDicts into list of filenames
        for entry in sgjJsonDict:
            existFilenameList.append(entry["Filename"])
        # Update existing entries
        for index, entry in enumerate(sgjJsonDict):
            if entry["Filename"] in newGameFilenameList:
                for newEntry in saveGameList:
                    if entry["Filename"] == newEntry["Filename"]:
                        # print("Updating:\t{} with {}".format(entry, newEntry))  # DEBUGGING
                        sgjJsonDict[index]["Version"] = newEntry["Version"]
                        # print("Updated:\t{}".format(sgjJsonDict[index]))  # DEBUGGING
                        break
        # Add new entries
        for entry in saveGameList:
            if entry["Filename"] not in existFilenameList:
                # print("Adding:\t{}".format(entry))  # DEBUGGING
                sgjJsonDict.append(entry)
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err
    else:
        sgjJsonFileObj.mod_data("Files", sgjJsonDict)

    # Update version
    try:
        asglVersion = sgjJsonFileObj.get_data("Version")
        if highVersion > asglVersion:
            sgjJsonFileObj.mod_data("Version", highVersion)
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # Save changes
    try:
        sgjJsonFileObj.write_json_file()
        sgjJsonFileObj.close_json_file()
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    return


def copy_save_game_from_list(absSaveGameList, saveGameName):
    '''
        PURPOSE - Copy details about one save game (or a list) from the stored list of save games
        INPUT
            absSaveGameList - Relative or absolute path to the json file storing the list of save games
            saveGameName - Name, or list of names, of save game(s) to remove from the list
        OUTPUT
            On success, return the list of entries removed
            On failure or error, Exception
    '''
    # LOCAL VARIABLES
    retVal = []            # List of entries removed
    saveGameList = []      # List of save games to remove from
    sgjJsonFileObj = None  # Store the JsonFile object here
    sgjJsonFiles = None    # sgjJsonFileObj.jDict["Files"]

    # INPUT VALIDATION
    # absSaveGameList
    if not isinstance(absSaveGameList, str):
        raise TypeError('Save game list name is of type "{}" instead of string'.format(type(absSaveGameList)))
    elif 0 >= len(absSaveGameList):
        raise ValueError("Invalid save game list name length")
    elif os.path.exists(absSaveGameList) is False:
        raise OSError("Save game list json file does not exist")
    elif os.path.isfile(absSaveGameList) is False:
        raise OSError("Save game list json file is not a file")

    # saveGameName
    if isinstance(saveGameName, str):
        saveGameList.append(saveGameName)
    elif isinstance(saveGameName, list):
        saveGameList = saveGameName
    else:
        raise TypeError('Save game name is of type "{}" instead of string or list'.format(type(saveGameName)))

    # saveGameName entries
    for filename in saveGameList:
        if not isinstance(filename, str):
            raise TypeError("Save game list contains non-string")
        elif 0 >= len(filename):
            raise ValueError("Save game list contains empty string")
        elif filename != os.path.basename(filename):
            raise ValueError("Detected a save game list entry that contains a path")

    # PARSE JSON FILE
    # Load json file
    try:
        sgjJsonFileObj = JsonFile(absSaveGameList)
        if sgjJsonFileObj.jSuccess:
            if sgjJsonFileObj.read_json_file() is False:
                raise RuntimeError("Failed to read json file")
            if sgjJsonFileObj.parse_json_contents() is False:
                raise RuntimeError("Failed to parse json file contents")
        else:
            raise RuntimeError("Failed to instantiate JsonFile object")
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # Copy save games
    # print("saveGameList:\t{}".format(saveGameList))  # DEBUGGING
    try:
        sgjJsonFiles = sgjJsonFileObj.get_data("Files")
        # sgjJsonFiles = deepcopy(sgjJsonFileObj.get_data("Files"))
        for entry in sgjJsonFiles:
            # print(entry["Filename"])  # DEBUGGING
            # if entry["Filename"] in saveGameList:
            if check_filename_no_ext(entry["Filename"], saveGameList) is True:
                # print("Copying:\t{}".format(entry))  # DEBUGGING
                retVal.append(entry)
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # Close JsonFile object
    try:
        sgjJsonFileObj.close_json_file()
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # DONE
    return retVal


def remove_save_game_from_list(absSaveGameList, saveGameName):
    '''
        PURPOSE - Remove one save game from the stored list of save games
        INPUT
            absSaveGameList - Relative or absolute path to the json file storing the list of save games
            saveGameName - Name, or list of names, of save game(s) to remove from the list
        OUTPUT
            On success, return the list of entries removed
            On failure or error, Exception
    '''
    # LOCAL VARIABLES
    retVal = []            # List of entries removed
    saveGameList = []      # List of save games to remove from
    sgjJsonFileObj = None  # Store the JsonFile object here
    sgjJsonFiles = None    # sgjJsonFileObj.jDict["Files"]

    # INPUT VALIDATION
    # absSaveGameList
    if not isinstance(absSaveGameList, str):
        raise TypeError('Save game list name is of type "{}" instead of string'.format(type(absSaveGameList)))
    elif 0 >= len(absSaveGameList):
        raise ValueError("Invalid save game list name length")
    elif os.path.exists(absSaveGameList) is False:
        raise OSError("Save game list json file does not exist")
    elif os.path.isfile(absSaveGameList) is False:
        raise OSError("Save game list json file is not a file")

    # saveGameName
    if isinstance(saveGameName, str):
        saveGameList.append(saveGameName)
    elif isinstance(saveGameName, list):
        saveGameList = saveGameName
    else:
        raise TypeError('Save game name is of type "{}" instead of string or list'.format(type(saveGameName)))

    # saveGameName entries
    for filename in saveGameList:
        if not isinstance(filename, str):
            raise TypeError("Save game list contains non-string")
        elif 0 >= len(filename):
            raise ValueError("Save game list contains empty string")
        elif filename != os.path.basename(filename):
            raise ValueError("Detected a save game list entry that contains a path")

    # PARSE JSON FILE
    # Load json file
    try:
        sgjJsonFileObj = JsonFile(absSaveGameList)
        if sgjJsonFileObj.jSuccess:
            if sgjJsonFileObj.read_json_file() is False:
                raise RuntimeError("Failed to read json file")
            if sgjJsonFileObj.parse_json_contents() is False:
                raise RuntimeError("Failed to parse json file contents")
        else:
            raise RuntimeError("Failed to instantiate JsonFile object")
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # Remove save games
    try:
        sgjJsonFiles = sgjJsonFileObj.get_data("Files")
        # for entry in sgjJsonFileObj.jDict["Files"]:
        for entry in sgjJsonFiles:
            if entry["Filename"] in saveGameList:
                # print("Removing:\t{}".format(entry))  # DEBUGGING
                # sgjJsonFileObj.jDict["Files"].remove(entry)
                retVal.append(entry)
                sgjJsonFiles.remove(entry)
                # retVal.append(sgjJsonFiles.remove(entry))
                # print("remove_save_game_from_list() retVal is currently:\t{}".format(retVal))  # DEBUGGING
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # Save changes
    try:
        sgjJsonFileObj.mod_data("Files", sgjJsonFiles)
        sgjJsonFileObj.write_json_file()
        sgjJsonFileObj.close_json_file()
    except Exception as err:
        print(repr(err))  # DEBUGGING
        raise err

    # DONE
    return retVal


def start_storage_dir(dstDir, bbJsonFile):
    '''
        PURPOSE - This function will attempt to create the backup directory from scratch
        INPUT
            dstDir - Absolute or relative path to the directory to start
            bbJsonFile - Base filename of the baron builder json file to start there
        OUTPUT
            OSError - Destination directory is not a directory
            OSError - Baron Builder save game json file exists as a directory
        NOTES
            This function will work for both the backup and archive baron builder directories
            If the directory doesn't exist, it will attempt to make it
            If the baron builder save game json doesn't exist, it will create an empty one
    '''
    # LOCAL VARIABLES
    absBBJsonFile = os.path.join(dstDir, bbJsonFile)  # Combined path of the dir and filename
    defContents = '{"Version":1,"Files":[]}'          # Default contents to start a new file
    bbJsonFileObj = None                              # Instantiate the JsonFile object here

    # INPUT VALIDATION
    # If it exists, verify it's a directory
    if os.path.exists(dstDir) is True:
        if os.path.isdir(dstDir) is False:
            raise OSError("Destination directory is not a directory")
    else:
        os.mkdir(dstDir)

    # CHECK BARON BUILDER JSON
    if os.path.exists(absBBJsonFile) is True:
        if os.path.isfile(absBBJsonFile) is True:
            pass
        else:
            raise OSError("Baron Builder save game json file exists as a directory")
    else:
        with open(absBBJsonFile, "w") as outFile:
            outFile.write(defContents)

    # DONE
    return


def verify_storage_dir(dstDir, bbJsonFile, fixIt=False):
    '''
        PURPOSE - Verify the integrity of a Baron Builder save game json
        INPUT
            dstDir - Absolute or relative path to the directory to start
            bbJsonFile - Base filename of the baron builder json file to start there
            fixIt - If broken, fix it
        OUTPUT
            True if the Baron Builder save game json is good
            False if it's bad
            Exception on error
        NOTE
            'Fix It' functionality not yet implemented
            This function assumes that bbJsonFile exists as a file
    '''
    # LOCAL VARIABLES
    retVal = True                                     # Set this to False if anything fails
    absBBJsonFile = os.path.join(dstDir, bbJsonFile)  # Combined path of the dir and filename
    mandatoryKeys = ["Version", "Files"]              # Mandatory keys
    mandatoryFilesKeys = ["Filename", "Version"]      # Mandatory "Files" keys
    bbJsonFileList = []                               # List of "Files" filenames from bbJsonFile
    bbJsonFileObj = None                              # Instantiate the JsonFile object here
    bbJsonDict = OrderedDict()                        # Copy of the JsonFile.jDict
    currentVersion = 0                                # "Version" of the save game list json file

    # INPUT VALIDATION

    # PARSE JSON
    try:
        bbJsonFileObj = JsonFile(absBBJsonFile)
        bbJsonFileObj.read_json_file()
        bbJsonFileObj.parse_json_contents()
    except Exception as err:
        print(repr(err))  # DEBUGGING
        retVal = False
    else:
        bbJsonDict = bbJsonFileObj.jDict
        bbJsonFileObj.close_json_file()

    # VERIFICATION
    # 1. Mandatory keys
    if retVal is True:
        for key in mandatoryKeys:
            if key not in bbJsonDict.keys():
                print("{} is missing mandatory key {}".format(bbJsonFile, key))  # DEBUGGING
                retVal = False
                break

    # 2. Extraneous keys
    if retVal is True:
        for key in bbJsonDict.keys():
            if key not in mandatoryKeys:
                print("{} has extraneous key {}".format(bbJsonFile, key))  # DEBUGGING
                retVal = False
                break

    # 3. Data types for those keys
    if retVal is True:
        # Version
        if not isinstance(bbJsonDict["Version"], int):
            print("{} has a non-integer version".format(bbJsonFile))  # DEBUGGING
            retVal = False
        # Files
        elif not isinstance(bbJsonDict["Files"], list):
            print("{} has a non-list of files".format(bbJsonFile))  # DEBUGGING
            retVal = False
        else:
            currentVersion = bbJsonDict["Version"]

    # 4. Content for those keys
    if retVal is True:
        # Version
        if 1 > bbJsonDict["Version"]:
            print("{} has an invalid version of {}".format(bbJsonFile, bbJsonDict["Version"]))  # DEBUGGING
            retVal = False
        # Files
        else:
            for entry in bbJsonDict["Files"]:
                if retVal is False:
                    break
                if 2 != len(entry):
                    print("{} has a 'Files' entry of invalid length".format(bbJsonFile))  # DEBUGGING
                    retVal = False
                    break
                else:
                    for subEntry in entry:
                        if retVal is False:
                            break
                        # Mandatory sub-entries
                        for subKey in mandatoryFilesKeys:
                            if subKey not in subEntry:
                                print("{} has a 'Files' entry missing a mandatory 'Files' key of {}".format(bbJsonFile, subKey))  # DEBUGGING
                                retVal = False
                                break
                        # Extraneous sub-entries
                        for subKey in subEntry:
                            if subKey not in mandatoryFilesKeys:
                                print("{} has a 'Files' entry has an extraneous key of {}".format(bbJsonFile, subKey))  # DEBUGGING
                                retVal = False
                                break
                        # Filename
                        if not isinstance(subEntry["Filename"], str):
                            print("{} has a 'Files' entry with a non-string filename".format(bbJsonFile))  # DEBUGGING
                            retVal = False
                            break
                        elif not isinstance(subEntry["Version"], int):
                            print("{} has a 'Files' entry with a non-integer version".format(bbJsonFile))  # DEBUGGING
                            retVal = False
                            break
                        elif currentVersion < subEntry["Version"]:
                            print("{} has a 'Files' entry with a version ({}) higher than the save game json ({})".format(
                                bbJsonFile, subEntry["Version"], currentVersion))  # DEBUGGING
                            retVal = False
                            break

    # 5. Verify Save Game Json Contains All Existing Files
    if retVal is True:
        for sgFile in bbJsonDict["Files"]:
            if os.path.exists(os.path.join(dstDir, sgFile)) is False:
                print("{} file {} does not exist".format(bbJsonFile, sgFile))
                retVal = False
                break
            elif os.path.isfile(os.path.join(dstDir, sgFile)) is False:
                print("{} file {} is not a file".format(bbJsonFile, sgFile))
                retVal = False
                break

    # 6. Verify All Existing Files Exist In The Save Game Json
    if retVal is True:
        # Get list of all bbJson filenames
        for entry in bbJsonDict["Files"]:
            bbJsonFileList.append(entry["Filename"])
        # Parse all existing filenames
        for sgFile in os.listdir(dstDir):
            if os.path.isfile(sgFile) is True:
                if os.path.basename(sgFile) not in bbJsonFileList:
                    print("{} file not listed in {}".format(os.path.basename(sgFile), bbJsonFile))  # DEBUGGING
                    retVal = False
                    break

    # FIX IT
    if retVal is False and fixIt is True:
        print("SAVE GAME JSON REPAIR NOT YET IMPLEMENTED")  # DEBUGGING
        pass

    # DONE
    return retVal


def check_filename_no_ext(needleFilename, haystackFile):
    '''
        PURPOSE - Determine if a filename matches another filename, or a list of filenames, without
            concern for file extensions
        INPUT
            needleFilename - String representation of a relative or absolute filename, with or
                without a file extension
            haystackFile - String, or list of strings, representation of a relative or absolute
                filename, with or without a file extension
        OUTPUT
            True if needleFilename matches something in haystackFile
            False if there's no match for needleFilename in haystackFile
            Exception on error
        NOTE
            The catalyst for this function is that I've begun comparing .zks file lists to .bbb
                file lists, etc.  I don't want to have to worry about file extensions but that
                means that needleFile in haystackList doesn't work easily as an inline one-liner.
            Examples:
                True == check_filename_no_ext(some_file.bak, some_file.orig)
                True == check_filename_no_ext(some_file.bak, [some_file.orig, nunya.txt])
                True == check_filename_no_ext(a_file.bak, [some_file.orig, nunya.txt, a_file])
                True == check_filename_no_ext(../some_file.bak, ../../some_file.orig)
                True == check_filename_no_ext(/root/some_file.bak, [/home/user/some_file.orig, nunya.txt])
                True == check_filename_no_ext(a_file.bak, [some_file.orig, nunya.txt, ../a_file])
                True == check_filename_no_ext(/root/a_file.bak, [some_file.orig, nunya.txt, a_file])
    '''
    # LOCAL VARIABLES
    retVal = False
    tempList = []    # Translate haystackFile here based on dynamic typing
    hsFileList = []  # Build this from haystackFile
    nFile = ""       # Build this from needleFilename

    # INPUT VALIDATION
    # needleFilename
    if not isinstance(needleFilename, str):
        raise TypeError("Needle is not a string")
    elif 0 >= len(needleFilename):
        raise ValueError("Needle is empty")
    # haystackFile
    if isinstance(haystackFile, str):
        tempList.append(haystackFile)
    elif isinstance(haystackFile, list):
        tempList = haystackFile
    else:
        raise TypeError("Haystack is not a string or list")
    # tempList
    for entry in tempList:
        if not isinstance(entry, str):
            raise TypeError("Haystack contained a non-string")

    # PREPARATION
    for entry in tempList:
        hsFileList.append(os.path.splitext(os.path.basename(entry))[0])

    nFile = os.path.splitext(os.path.basename(needleFilename))[0]

    # COMPARISON
    if nFile in hsFileList:
        retVal = True

    # DONE
    return retVal
