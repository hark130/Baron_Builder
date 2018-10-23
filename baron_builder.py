#################################################
#################### IMPORTS ####################
#################################################

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
minMajNum = 3  # Minimum Python version major number
minMinNum = 5  # Minimum Python version minor number
minMicNum = 2  # Minimum Python version micro number

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


def main():
    # LOCAL VARIABLES
    retVal = True         # Indicates flow control success
    operSys = OS_UNKNOWS  # Operating system macro
    saveGamePath = ""     # Absolute path to save games

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
        pass

    # Parse Save Games
    if retVal:
        pass

    # Print Menu
    if retVal:
        pass


if __name__ == "__main__":
    main()
