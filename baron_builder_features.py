'''
    PURPOSE - Organize all of the features implemented for Baron Builder
    NOTES
        Each feature should have its own dedicated sub-menu defined here that follows
            the following general naming convention:
                bbf<num>_<SHORT DESCR>_sub_menu(saveGameObj)
        Each function will be named after the feature it directly supports
            e.g., The Baron Builder Feature 6 (change gold) function to change the gold should be named
            bbf06_GOLD_sub_menu()
'''



#################################################
#################### IMPORTS ####################
#################################################

from collections import OrderedDict
from zks_file_class import ZksFile

#################################################
#################### MACROS #####################
#################################################
MAX_GOLD = 1000000                              # Upper end limit for modifying gold
MAX_BPS = 25000                                 # Upper end limit for modifying build points

#################################################
#################### GLOBALS ####################
#################################################

#################################################
################### FEATURES ####################
#################################################


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
        tempOrdDict = saveGameObj.zPlayFile.get_data("Kingdom")
        retVal = tempOrdDict["BP"]
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
        if saveGameObj.zPlayFile.key_present("Kingdom") is True:
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


############### F02 - STABILITY #################


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
    curGold = 0  # Current amount of gold
    newGold = 0  # New amount of gold input by user
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

                    # Take input
                    newGold = input("Enter the amount of gold you want up to a maximum of {} [{}]?  ".format(MAX_GOLD, curGold * 2))

                    # Modify input
                    if len(newGold) == 0:
                        newGold = curGold * 2
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
        # print("player.json JsonFile success:\t{}".format(saveGameObj.zPlayFile.jSuccess))  # DEBUGGING
        retVal = saveGameObj.zPlayFile.get_data("Money")
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
        if saveGameObj.zPlayFile.key_present("Money") is True:
            retVal = saveGameObj.zPlayFile.mod_data("Money", newGoldAmnt)
    except KeyError as err:
        print(repr(err))  # DEBUGGING
        retVal = False

    # DONE
    return retVal
