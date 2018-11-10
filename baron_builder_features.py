'''
    PURPOSE - Organize all of the features implemented for Baron Builder
    NOTES
        Each feature should have its own dedicated sub-menu defined here that follows
            the following general naming convention:
                bbf<num>_<SHORT DESCR>_sub_menu(saveGameObj)
        Each feature should also have a function dedicated to determining availability:
            bbf<num>_<SHORT_DESCR>_available(saveGameObj)
        Each function will be named after the feature it directly supports
            e.g., The Baron Builder Feature 6 (change gold) function to change the gold should be named
            bbf06_GOLD_sub_menu()
'''


#################################################
#################### IMPORTS ####################
#################################################

from baron_builder_imports import supportedOSGlobal
from baron_builder_imports import MAX_ERRS
from baron_builder_utilities import clear_screen, are_you_sure
from collections import OrderedDict
from zks_file_class import ZksFile


#################################################
#################### MACROS #####################
#################################################

MAX_GOLD = 9999999                              # Upper end limit for modifying gold
MAX_BPS = 25000                                 # Upper end limit for modifying build points


#################################################
#################### GLOBALS ####################
#################################################

# KINGDOM UNREST LEVELS
fullStabListGlobal = [ "Serene", "Stable", "Worried", "Troubled", "Rioting", "Crumbling" ]


#################################################
################### FEATURES ####################
#################################################


def user_feature_menu(operSys, saveGameObj, curNumBadAns):
    '''
        PURPOSE - Allow a user to decide how to edit a given save game
        INPUT
            operSys - See OPERATAING SYSTEM macros
            saveGameObj - ZksFile object for a selected save game
            curNumBadAns - Current number of incorrect answers to track error tolerance
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
    numBadAnswers = curNumBadAns  # Current number of bad answers

    # INPUT VALIDATION
    if not isinstance(operSys, int):
        raise TypeError('Operating system is of type "{}" instead of integer'.format(type(operSys)))
    elif operSys not in supportedOS:
        raise ValueError("Operating system value is unknown")
    elif not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))
    elif not isinstance(curNumBadAns, int):
        raise TypeError('Current number of bad answers is of type "{}" instead of integer'.format(type(curNumBadAns)))
    elif curNumBadAns > MAX_ERRS:
        raise RuntimeError("Exceeded maximum bad answers")
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

    # PRINT MENU
    while retVal and numBadAnswers <= MAX_ERRS:
        print("")  # Blank line
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
            if are_you_sure(numBadAnswers, "close the file without saving") is True:
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
    if numBadAnswers > MAX_ERRS:
        raise RuntimeError("Exceeded maximum bad answers")
    return retVal


############## F01 - BUILD POINTS ###############


def bbf01_BP_sub_menu(saveGameObj, curNumBadAns, maxNumBadAns):
    '''
        PURPOSE - Baron Builder Feature 01: Modify build points
            This function serves as the sub-menu to modify build points
        INPUT
            saveGameObj - ZksFile object for a selected save game
            curNumBadAns - Current number of incorrect answers to track error tolerance
            maxNumBadAns - Maximum number of incorrect answers before giving up
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTES
            This function makes no changes but calls functions that do
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = True
    curBP = 0  # Current amount of gold
    newBP = 0  # New amount of gold input by user
    numBadAnswers = curNumBadAns  # Number of bad answers given here

    # INPUT VALIDATION
    if not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))
    elif not isinstance(curNumBadAns, int):
        raise TypeError('Current number of bad answers is of type "{}" instead of integer'.format(type(curNumBadAns)))
    elif not isinstance(maxNumBadAns, int):
        raise TypeError('Maximum number of bad answers is of type "{}" instead of integer'.format(type(maxNumBadAns)))
    elif curNumBadAns > maxNumBadAns:
        retVal = False

    # FEATURE 01 - BP
    if retVal:
        try:
            # PRINT MENU
            print("")  # Blank line
            curBP = bbf01_BP_get_bps(saveGameObj)
        except Exception as err:
            print("\nUnable to determine current build points")
            print(repr(err))
            retVal = False
        else:
            if -1 == curBP:
                print("\nUnable to determine current build points")
            else:
                while numBadAnswers <= maxNumBadAns:

                    # Print options
                    print("You currently have {} build points.".format(curBP))

                    # Take input
                    print("Enter the amount of build points you want up to a maximum of {}".format(MAX_BPS))
                    print("-or-")
                    print('Type "exit" to return to the previous menu')
                    newBP = input("Enter your selection [{}]:  ".format(curBP * 2))

                    # Modify input
                    if len(newBP) == 0:
                        newBP = curBP * 2
                    else:
                        newBP = newBP.lower()

                    if "exit" == newBP:
                        retVal = True
                        break
                    else:
                        try:
                            newBP = int(newBP)
                        except Exception as err:
                            print("Invalid selection.")
                            numBadAnswers += 1
                            if numBadAnswers <= maxNumBadAns:
                                print("Try again.")
                        else:
                            numBadAnswers = 0
                            # Execute selection
                            retVal = bbf01_BP_set_bps(saveGameObj, newBP)
                            break

    # DONE
    return retVal


def bbf01_BP_get_bps(saveGameObj):
    '''
        PURPOSE - Baron Builder Feature 01: Modify build points
            Determine how many build points exist in this save game
        INPUT
            saveGameObj - ZksFile object for a selected save game
        OUTPUT
            On success, Integer value representing the number of build points
            On failure, -1
            On error, Exception
        NOTES
            This function makes no changes
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = -1
    tempOrdDict = OrderedDict()  # Temporary return value from JsonFile.get_data("Kingdom")

    # DETERMINE BUILD POINTS
    try:
        if bbf01_BP_available(saveGameObj) is True:
            tempOrdDict = saveGameObj.zPlayFile.get_data("Kingdom")
            retVal = tempOrdDict["BP"]
        else:
            retVal = -1
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = -1

    # VALIDATE DATA
    if not isinstance(retVal, int):
        retVal = -1
    elif -1 > retVal:
        retVal = -1

    # DONE
    return retVal


def bbf01_BP_set_bps(saveGameObj, newBPAmnt):
    '''
        PURPOSE - Baron Builder Feature 01: Modify build points
            Change the amount of build points for this save game
        INPUT
            saveGameObj - ZksFile object for a selected save game
            newBPAmnt - Integer representation for the new amount of build points
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTES
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = False
    tempOrdDict = OrderedDict()  # Temporary return value from JsonFile.get_data("Kingdom")
    oldBPAmnt = 0  # Old amount of BP

    # INPUT VALIDATION
    if not isinstance(newBPAmnt, int):
        raise TypeError('New build point amount is of type "{}" instead of integer'.format(type(newBPAmnt)))
    elif 0 > newBPAmnt:
        raise ValueError("Invalid amount of build points")
    elif MAX_BPS < newBPAmnt:
        raise ValueError("Amount of new build points exceeds arbitrary maximum of {}".format(MAX_BPS))

    # DETERMINE AMOUNT OF GOLD
    try:
        if bbf01_BP_available(saveGameObj) is True:
            # 1. Get the Kingdom dictionary
            tempOrdDict = saveGameObj.zPlayFile.get_data("Kingdom")
            oldBPAmnt = tempOrdDict["BP"]
            # 2. Modify the Kingdom dictionary
            tempOrdDict["BP"] = newBPAmnt
            tempOrdDict["BPOnLastRavenVisit"] = newBPAmnt - oldBPAmnt + tempOrdDict["BPOnLastRavenVisit"]
            # 3. Replace the Kingdom dictionary
            retVal = saveGameObj.zPlayFile.mod_data("Kingdom", tempOrdDict)
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = False

    # DONE
    return retVal


def bbf01_BP_available(saveGameObj):
    '''
        PURPOSE - Baron Builder Feature 01: Modify build points
            Determine if this save game is 'mature' enough to support this feature
        INPUT
            saveGameObj - ZksFile object for a selected save game
        OUTPUT
            If available, True
            If not, False
            On error, Exception
        NOTES
            This function makes no changes
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = False
    tempOrdDict = OrderedDict()  # Temporary return value from JsonFile.get_data("Kingdom")

    # INPUT VALIDATION
    if not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))

    # DETERMINE AVAILABILITY
    try:
        if saveGameObj.zPlayFile.key_present("Kingdom") is True:
            # 1. Get the Kingdom dictionary
            tempOrdDict = saveGameObj.zPlayFile.get_data("Kingdom")
            if "BP" in tempOrdDict.keys():
                retVal = True
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = False

    # DONE
    return retVal


############### F02 - STABILITY #################


def bbf02_STAB_sub_menu(saveGameObj, curNumBadAns, maxNumBadAns):
    '''
        PURPOSE - Baron Builder Feature 02: Modify kingdom stability
            This function serves as the sub-menu to modify the kingdom's stability
        INPUT
            saveGameObj - ZksFile object for a selected save game
            curNumBadAns - Current number of incorrect answers to track error tolerance
            maxNumBadAns - Maximum number of incorrect answers before giving up
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTES
            This function makes no changes but calls functions that do
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = True
    curStab = ""  # Current stability
    newStab = ""  # New stability
    newStabChoice = 0  # New stability user selection
    numBadAnswers = curNumBadAns  # Number of bad answers given here
    fullStabList = fullStabListGlobal  # Full list of stability strings
    suppStabList = [ "Stable", "Worried", "Troubled", "Rioting", "Crumbling" ]  # Supported stabilities

    # INPUT VALIDATION
    if not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))
    elif not isinstance(curNumBadAns, int):
        raise TypeError('Current number of bad answers is of type "{}" instead of integer'.format(type(curNumBadAns)))
    elif not isinstance(maxNumBadAns, int):
        raise TypeError('Maximum number of bad answers is of type "{}" instead of integer'.format(type(maxNumBadAns)))
    elif curNumBadAns > maxNumBadAns:
        retVal = False

    # FEATURE 02 - STABILITY
    if retVal:
        try:
            # PRINT MENU
            print("")  # Blank line
            curStab = bbf02_STAB_get_stability(saveGameObj)
        except Exception as err:
            print("\nUnable to determine kingdom's current stability")
            print(repr(err))
            retVal = False
        else:
            if -1 == curStab:
                print("\nUnable to determine kingdom's current stability")
            else:
                while numBadAnswers <= maxNumBadAns:

                    # Print options
                    print('Your kingdom is currently "{}"'.format(curStab))
                    print("\nKingdom Stability Choices:")
                    for stab in fullStabList:
                        print("{}. {}".format(fullStabList.index(stab) + 1, stab))

                    # Take input
                    print("\nEnter the number of the new stability level")
                    print("-or-")
                    print('Type "exit" to return to the previous menu')
                    newStabChoice = input("Enter your selection [{}]:  ".format(fullStabList.index("Stable") + 1))

                    # Modify input
                    if 0 == len(newStabChoice):
                        newStabChoice = fullStabList.index("Stable") + 1
                        print("Settting default response to {}".format(fullStabList.index("Stable") + 1))
                    else:
                        newStabChoice = newStabChoice.lower()

                    # Execute selection
                    if "exit" == newStabChoice:
                        retVal = True
                        break
                    else:
                        try:
                            newStabChoice = int(newStabChoice)
                            newStab = fullStabList[newStabChoice - 1]
                            if newStab in suppStabList:
                                retVal = bbf02_STAB_set_stability(saveGameObj, newStab)
                                numBadAnswers = 0
                                break
                            else:
                                print('"{}" is not currently supported.'.format(fullStabList[newStabChoice - 1]))
                                print('"{}" is currently the highest supported kingdom stability'.format(suppStabList[0]))
                                numBadAnswers += 1
                                if numBadAnswers <= maxNumBadAns:
                                    print("Try again.")
                        except Exception as err:
                            print("Invalid selection.")
                            numBadAnswers += 1
                            if numBadAnswers <= maxNumBadAns:
                                print("Try again.")
                        else:
                            pass

    # DONE
    return retVal


def bbf02_STAB_get_stability(saveGameObj):
    '''
        PURPOSE - Baron Builder Feature 02: Modify kingdom stability
            Determine the kingdom's stability in this save game
        INPUT
            saveGameObj - ZksFile object for a selected save game
        OUTPUT
            On success, String representing kingdom's current unrest level
            On failure, Empty string
            On error, Exception
        NOTES
            This function makes no changes
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = -1
    tempOrdDict = OrderedDict()  # Temporary return value from JsonFile.get_data("Kingdom")

    # DETERMINE BUILD POINTS
    try:
        if bbf02_STAB_available(saveGameObj) is True:
            tempOrdDict = saveGameObj.zPlayFile.get_data("Kingdom")
            retVal = tempOrdDict["Unrest"]
        else:
            retVal = ""
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = ""

    # VALIDATE DATA
    if not isinstance(retVal, str):
        retVal = ""
    elif retVal not in fullStabListGlobal:
        retVal = ""

    # DONE
    return retVal


def bbf02_STAB_set_stability(saveGameObj, newStabStr):
    '''
        PURPOSE - Baron Builder Feature 02: Modify kingdom stability
            Change the kingdom's stability for this save game
        INPUT
            saveGameObj - ZksFile object for a selected save game
            newStabStr - String representation for the new kingdom unrest level
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTES
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = False
    tempOrdDict = OrderedDict()  # Temporary return value from JsonFile.get_data("Kingdom")

    # INPUT VALIDATION
    if not isinstance(newStabStr, str):
        raise TypeError('New build point amount is of type "{}" instead of string'.format(type(newStabStr)))
    elif 1 > len(newStabStr):
        raise ValueError("New stability string is empty")
    elif newStabStr not in fullStabListGlobal:
        raise ValueError("Invalid kingdom stability")

    # DETERMINE AMOUNT OF GOLD
    try:
        if bbf02_STAB_available(saveGameObj) is True:
            # 1. Get the Kingdom dictionary
            tempOrdDict = saveGameObj.zPlayFile.get_data("Kingdom")
            # 2. Modify the Kingdom dictionary
            tempOrdDict["Unrest"] = newStabStr
            tempOrdDict["UnrestOnLastRavenVisit"] = newStabStr
            # 3. Replace the Kingdom dictionary
            retVal = saveGameObj.zPlayFile.mod_data("Kingdom", tempOrdDict)
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = False

    # DONE
    return retVal


def bbf02_STAB_available(saveGameObj):
    '''
        PURPOSE - Baron Builder Feature 02: Modify kingdom stability
            Determine if this save game is 'mature' enough to support this feature
        INPUT
            saveGameObj - ZksFile object for a selected save game
        OUTPUT
            If available, True
            If not, False
            On error, Exception
        NOTES
            This function makes no changes
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = False
    tempOrdDict = OrderedDict()  # Temporary return value from JsonFile.get_data("Kingdom")

    # INPUT VALIDATION
    if not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))

    # DETERMINE AVAILABILITY
    try:
        if saveGameObj.zPlayFile.key_present("Kingdom") is True:
            # 1. Get the Kingdom dictionary
            tempOrdDict = saveGameObj.zPlayFile.get_data("Kingdom")
            if "Unrest" in tempOrdDict.keys():
                retVal = True
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = False

    # DONE
    return retVal


################## F06 - GOLD ###################


def bbf06_GOLD_sub_menu(saveGameObj, curNumBadAns, maxNumBadAns):
    '''
        PURPOSE - Baron Builder Feature 06: Modify gold
            This function serves as the sub-menu to modify gold
        INPUT
            saveGameObj - ZksFile object for a selected save game
            curNumBadAns - Current number of incorrect answers to track error tolerance
            maxNumBadAns - Maximum number of incorrect answers before giving up
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTES
            This function makes no changes but calls functions that do
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = True
    curGold = 0                   # Current amount of gold
    newGold = 0                   # New amount of gold input by user
    numBadAnswers = curNumBadAns  # Number of bad answers given here
    defaultGold = 0               # Default amount of gold to set

    # INPUT VALIDATION
    if not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))
    elif not isinstance(curNumBadAns, int):
        raise TypeError('Current number of bad answers is of type "{}" instead of integer'.format(type(curNumBadAns)))
    elif not isinstance(maxNumBadAns, int):
        raise TypeError('Maximum number of bad answers is of type "{}" instead of integer'.format(type(maxNumBadAns)))
    elif curNumBadAns > maxNumBadAns:
        retVal = False

    # FEATURE 06 - GOLD
    if retVal:
        try:
            # PRINT MENU
            print("")  # Blank line
            curGold = bbf06_GOLD_get_gold(saveGameObj)
        except Exception as err:
            print("\nUnable to determine current gold amount")
            print(repr(err))
            retVal = False
        else:
            if -1 == curGold:
                print("\nUnable to determine current gold amount")
            else:
                while numBadAnswers <= maxNumBadAns:

                    # Print options
                    print("You currently have {} gold.".format(curGold))
                    
                    # Determine max gold
                    if curGold * 2 > MAX_GOLD:
                        defaultGold = MAX_GOLD
                    else:
                        defaultGold = curGold * 2

                    # Take input
                    newGold = input("Enter the amount of gold you want up to a maximum of {} [{}]?  ".format(MAX_GOLD, defaultGold))

                    # Modify input
                    if len(newGold) == 0:
                        newGold = defaultGold
                        numBadAnswers = 0
                    else:
                        try:
                            newGold = int(newGold)
                        except Exception as err:
                            print("Invalid selection.")
                            numBadAnswers += 1
                            if numBadAnswers <= maxNumBadAns:
                                print("Try again.")
                        else:
                            numBadAnswers = 0

                    # Execute selection
                    retVal = bbf06_GOLD_set_gold(saveGameObj, newGold)
                    break

    # DONE
    return retVal


def bbf06_GOLD_get_gold(saveGameObj):
    '''
        PURPOSE - Baron Builder Feature 06: Modify gold
            Determine how much gold exists in this save game
        INPUT
            saveGameObj - ZksFile object for a selected save game
        OUTPUT
            On success, Integer value representing the amount of gold
            On failure, -1
            On error, Exception
        NOTES
            This function makes no changes
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = -1

    # DETERMINE AMOUNT OF GOLD
    try:
        if bbf06_GOLD_available(saveGameObj) is True:
            retVal = saveGameObj.zPlayFile.get_data("Money")
        else:
            retVal = -1
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = -1

    # DONE
    return retVal


def bbf06_GOLD_set_gold(saveGameObj, newGoldAmnt):
    '''
        PURPOSE - Baron Builder Feature 06: Modify gold
            Change the amount of gold for this save game
        INPUT
            saveGameObj - ZksFile object for a selected save game
            newGoldAmnt - Integer representation for the new amount of gold
        OUTPUT
            On success, True
            On failure, False
            On error, Exception
        NOTES
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = False

    # INPUT VALIDATION
    if not isinstance(newGoldAmnt, int):
        raise TypeError('New gold amount is of type "{}" instead of integer'.format(type(newGoldAmnt)))
    elif 0 > newGoldAmnt:
        raise ValueError("Invalid amount of new gold")
    elif MAX_GOLD < newGoldAmnt:
        raise ValueError("Amount of new gold exceeds arbitrary maximum of {}".format(MAX_GOLD))

    # DETERMINE AMOUNT OF GOLD
    try:
        if bbf06_GOLD_available(saveGameObj) is True:
            retVal = saveGameObj.zPlayFile.mod_data("Money", newGoldAmnt)
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = False

    # DONE
    return retVal


def bbf06_GOLD_available(saveGameObj):
    '''
        PURPOSE - Baron Builder Feature 06: Modify gold
            Determine if this save game is 'mature' enough to support this feature
        INPUT
            saveGameObj - ZksFile object for a selected save game
        OUTPUT
            If available, True
            If not, False
            On error, Exception
        NOTES
            This function makes no changes
            This function will not close anything
    '''
    # LOCAL VARIABLES
    retVal = False
    tempOrdDict = OrderedDict()

    # INPUT VALIDATION
    if not isinstance(saveGameObj, ZksFile):
        raise TypeError('Save game object is of type "{}" instead of ZksFile'.format(type(saveGameObj)))

    # DETERMINE AVAILABILITY
    try:
        retVal = saveGameObj.zPlayFile.key_present("Money")
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = False

    # DONE
    return retVal
