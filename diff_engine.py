from collections import OrderedDict
from json_file_class import JsonFile
import hashlib
import os

BLOCKSIZE = 65536


def hash_it(filename):
    '''
        PURPOSE - Hash a file
        INPUT
            filename - File name of an existing file
        OUTPUT
            On success, hexdigest
            On failure/error, Exception
    '''
    # LOCAL VARIABLES
    retVal = ""

    # INPUT VALIDATION
    if not isinstance(filename, str):
        raise TypeError("Filename is not a string")
    elif 0 >= len(filename):
        raise ValueError("Filename is empty")
    elif os.path.exists(filename) is False:
        raise OSError("Filename does not exist")
    elif os.path.isfile(filename) is False:
        raise OSError("Filename is not a file")

    # HASH IT
    hasher = hashlib.md5()
    with open(filename, 'rb') as inFile:
        buf = inFile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = inFile.read(BLOCKSIZE)
    retVal = hasher.hexdigest()

    # DONE
    return retVal


def m_EntityData_parser(medValue):
    '''
        PURPOSE - Parse/investigate/dig into m_EntityData entries outside of main()
        INPUT
            medValue - Value associated with a m_EntityData key
        OUTPUT
            On error, Exception
    '''
    # LOCAL VARIABLES
    typeList = []  # Store the different types here before printing them

    # PARSE IT
    # 1. Type - List
    print("\t\tThis value is of type:\t{}".format(type(medValue)))

    # 2. Entries types - OrderedDicts
    for entry in medValue:
        if type(entry) not in typeList:
            typeList.append(type(entry))

    print("\t\tThis value has the following types:\t{}".format(typeList))

    # 3. First entry in each OrderedDict
    for entry in medValue:
        if 0 < len(entry):
            try:
                print("\t\t{}".format(entry["$id"]))
            except KeyError as err:
                print("\t\tNo $id")

    # DONE
    return


def compare_ordered_dicts(dict1, dict2):
    '''
        PURPOSE - Return a list of ordered dict items that do no match
        INPUT
            dict1 - Ordered Dict
            dict2 - Ordered Dict
        OUTPUT
            On success, a list (empty or not) of tuples of mismatched items
        NOTE
            This function is recursive
            It is also recursive
    '''
    # LOCAL VARIABLES
    retVal = []
    tempRetVal = []

    # INPUT VALIDATION
    if not isinstance(dict1, dict):
        raise TypeError("Dict1 is not a dictionary")
    elif not isinstance(dict2, dict):
        raise TypeError("Dict2 is not a dictionary")

    # COMPARE
    if dict1 != dict2:
        for thing in dict1.keys():
            if thing not in dict2.keys():
                # retVal.append(tuple((thing, None)))
                retVal.append(tuple(({thing:dict1[thing]}, None)))
        for thing in dict2.keys():
            if thing not in dict1.keys():
                # retVal.append(tuple((None, thing)))
                retVal.append(tuple((None, {thing:dict2[thing]})))
        for thing in dict1.keys():
            if isinstance(dict1[thing], OrderedDict) and isinstance(dict2[thing], OrderedDict):
                # print("Going recursive with {}".format(thing))  # DEBUGGING
                tempRetVal = compare_ordered_dicts(dict1[thing], dict2[thing])
                if 0 < len(tempRetVal):
                    # print("retVal before:\t{}".format(retVal))  # DEBUGGING
                    retVal += tempRetVal
                    # print("retVal after:\t{}".format(retVal))  # DEBUGGING



    # DONE
    return retVal


def main():
    rootDir = os.path.join(os.getcwd(), "Test_Files", "Linux", "Case_Study")
    beforeDir = os.path.join(rootDir, "Before")
    afterDir = os.path.join(rootDir, "After")
    beforeHash = ""
    afterHash = ""
    changedFileList = []
    beforeJsonFileObj = None
    afterJsonFileObj = None
    tempRetVal = []  # List of differences returned by compare_ordered_dicts()
    skipTheseRedHerrings = [
        # Money
        "player.json",
        # App status, game history log
        "statistic.json",
        # Diff based on version update
        "0eed7a8820af0c549a7eee0a6bd1feb9CapitalSquareVillage_Mechanic_AlignmentCN.json",
        # Save game garbage 
        "header.json",
    ]

    print("\n\nCHANGED FILES:")
    for thing in os.listdir(beforeDir):
        beforeHash = hash_it(os.path.join(beforeDir, thing))
        afterHash = hash_it(os.path.join(afterDir, thing))
        if beforeHash != afterHash:
            print("{}".format(thing))  # DEBUGGING
            if thing.endswith(".json") and thing not in skipTheseRedHerrings:
                changedFileList.append(thing)

    print("\n\nLOADING JSON FILES")
    for entry in changedFileList:
        print("\n{}".format(entry))
        # Instantiate objects
        beforeJsonFileObj = JsonFile(os.path.join(beforeDir, entry))
        afterJsonFileObj = JsonFile(os.path.join(afterDir, entry))
        # Read file contents
        beforeJsonFileObj.read_json_file()
        afterJsonFileObj.read_json_file()
        # Parse files
        beforeJsonFileObj.parse_json_contents()
        afterJsonFileObj.parse_json_contents()
        # Compare dicts
        for key in beforeJsonFileObj.jDict.keys():
            if beforeJsonFileObj.jDict[key] != afterJsonFileObj.jDict[key]:
                print("\tKey '{}' mismatch".format(key))
                if "m_EntityData" == key:
                    # print("\t\tOld Value:\t{}".format(beforeJsonFileObj.jDict[key]))
                    # print("\t\tNew Value:\t{}".format(afterJsonFileObj.jDict[key]))
                    m_EntityData_parser(beforeJsonFileObj.jDict[key])
                    for index in range(0, len(beforeJsonFileObj.jDict[key])):
                        if beforeJsonFileObj.jDict[key][index] != afterJsonFileObj.jDict[key][index]:
                            # print("\t\t\tOld Value:\t{}".format(beforeJsonFileObj.jDict[key][index]))
                            # print("\t\t\tNew Value:\t{}".format(afterJsonFileObj.jDict[key][index]))
                            tempRetVal = compare_ordered_dicts(beforeJsonFileObj.jDict[key][index], afterJsonFileObj.jDict[key][index])
                            for difference in tempRetVal:
                                print("\t\t\tOld Value:\t{}".format(difference[0]))
                                print("\t\t\tNew Value:\t{}".format(difference[1]))

if __name__ == "__main__":
    main()
