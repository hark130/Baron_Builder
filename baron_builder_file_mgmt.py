'''
    PURPOSE - Organize all of the file management functionality implemented for Baron Builder
'''


#################################################
#################### IMPORTS ####################
#################################################




#################################################
#################### MACROS #####################
#################################################



#################################################
#################### GLOBALS ####################
#################################################




#################################################
################### FUNCTIONS ###################
#################################################


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


