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

from zks_file_class import ZksFile

#################################################
#################### MACROS #####################
#################################################
MAX_GOLD = 1000000                              # Upper end limit for modifying gold

#################################################
#################### GLOBALS ####################
#################################################

#################################################
################### FEATURES ####################
#################################################


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
                    newGold = input("Enter the amount of gold you want [{}]?  ".format(curGold * 2))

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
        PURPOSE - Baron Builder Feature 
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
        PURPOSE - Change the amount of gold for this save game
        INPUT
            saveGameObj - ZksFile object for a selected save game
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
