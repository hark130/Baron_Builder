'''
    PURPOSE - Organize all of the utility functionality implemented for Baron Builder
'''


#################################################
#################### IMPORTS ####################
#################################################

from baron_builder_imports import supportedOSGlobal
from baron_builder_imports import OS_UNKNOWS, OS_LINUX, OS_WINDOWS, OS_APPLE
from baron_builder_imports import MAX_ERRS
import os
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


def are_you_sure(curNumBadAns, actionStr=""):
    '''
        PURPOSE - Verify the user knows what they're doing
        INPUT
            curNumBadAns - Current number of incorrect answers to track error tolerance
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
    numBadAnswers = curNumBadAns  # Current number of bad answers

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

