from collections import OrderedDict
import codecs
import io
import json
import re
import sys


def strip_first_dict(strDict):
    # LOCAL VARIABLES
    retVal = ""
    curPos = 0
    numStartDelims = 0
    numStopDelims = 0
    startPos = None
    stopPos = None

    # INPUT VALIDATION
    if not isinstance(strDict, str):
        raise TypeError("Not a string")
    elif 0 == len(strDict):
        raise ValueError("Empty string")
    elif strDict.count("{") > 0 and strDict.count("}") > 0 and strDict.find("{") < strDict.find("}"):
        # FIND A DICTIONARY
        retVal = strDict

        for char in retVal:
            if char == "{":
                numStartDelims += 1
                # print("Num start == {}".format(numStartDelims))  # DEBUGGING
                if startPos is None:
                    startPos = curPos
                    # print("Start Pos == {}".format(startPos))  # DEBUGGING
            elif char == "}":
                numStopDelims += 1
                # print("Num stop == {}".format(numStopDelims))  # DEBUGGING

            if numStartDelims == numStopDelims and 0 < numStopDelims:
                stopPos = curPos
                # print("Stop Pos == {}".format(stopPos))  # DEBUGGING
                # print("start == {}".format(numStartDelims))  # DEBUGGING
                # print("stop == {}".format(numStopDelims))  # DEBUGGING
                retVal = retVal[startPos:stopPos + 1]
                # print(retVal)  # DEBUGGING
                break
            else:
                curPos += 1

    return retVal


def strip_inner_dict(strDict):
    # LOCAL VARIABLES
    retVal = ""
    tmpStr = ""

    # INPUT VALIDATION
    if not isinstance(strDict, str):
        raise TypeError("Not a string")
    elif 0 == len(strDict):
        raise ValueError("Empty string")
    elif strDict.count("{") > 0 and strDict.count("}") > 0:
        # FIND A DICTIONARY
        retVal = strip_first_dict(strDict)
        tmpStr = retVal
        # Strip off dictionary delimiters
        while True:
            tmpStr = tmpStr[1:]
            tmpStr = tmpStr[:len(tmpStr) - 1]
            tmpStr = strip_inner_dict(tmpStr)
            if 0 == len(tmpStr):
                break
            else:
                retVal = tmpStr
    
    return retVal


def main():
    # LOCAL VARIABLES
    tempString = ""
    origFileName = "/home/joe/Documents/Personal/Programming/Baron_Builder/Test_Files/Case_Study/player(original).json"
    brknFileName = "/home/joe/Documents/Personal/Programming/Baron_Builder/Test_Files/Case_Study/player(broken8).json"
    origContent = ""
    brknContent = ""
    origUTF8Content = ""
    brknUTF8Content = ""
    origStrList = []
    brknStrList = []
    remOrigContent = ","
    remBrknContent = ","
    origDict = {}
    brknDict = {}
    origOrdDict = {}
    brnkOrdDict = {}

    # READ FILES
    with open(origFileName, "r") as origFile:
        origContent = origFile.read()

    with open(brknFileName, "r") as brknFile:
        brknContent = brknFile.read()

    # REMOVE SIMILARITIES
    # Attempt #1 - Didn't remove enough
    # origStrList = origContent.split()
    # brknStrList = brknContent.split()
    # for brknEntry in brknStrList:
    #     if brknEntry in origStrList:
    #         while True:
    #             try:
    #                 origStrList.remove(brknEntry)
    #                 brknStrList.remove(brknEntry)
    #                 print("Removed:\t{}".format(brknEntry))
    #             except Exception as err:
    #                 break
    # remOrigContent = remOrigContent.join(origStrList)
    # remBrknContent = remBrknContent.join(brknStrList)

    # Attempt #2 - Didn't remove enough
    # origStrList = re.split("{|}", origContent)
    # brknStrList = re.split("{|}", brknContent)
    # for brknEntry in brknStrList:
    #     if brknEntry in origStrList:
    #         while True:
    #             try:
    #                 origStrList.remove(brknEntry)
    #                 brknStrList.remove(brknEntry)
    #                 print("Removed:\t{}".format(brknEntry))
    #             except Exception as err:
    #                 break
    # remOrigContent = remOrigContent.join(origStrList)
    # remBrknContent = remBrknContent.join(brknStrList)

    # Attempt #3
    # remOrigContent = origContent
    # remBrknContent = brknContent
    # print("REMOVING BROKEN CONTENT FROM ORIGINAL")
    # print("Original Size:\t{}".format(len(remOrigContent)))
    # print("Broken Size:\t  {}".format(len(remBrknContent)))

    # print("[", end = "")
    # sys.stdout.flush()

    # while True:
    #     print(".", end = "")
    #     sys.stdout.flush()
    #     # Find inner-most dict
    #     try:
    #         tempString = strip_inner_dict(remBrknContent)
    #         # print(tempString)
    #         # break
    #     except Exception as err:
    #         break  # No more dictionaries?
    #     else:
    #         if 0 < len(tempString):
    #             try:
    #                 remOrigContent = remOrigContent.replace(tempString, "")
    #             except Exception as err:
    #                 pass

    #             try:
    #                 remBrknContent = remBrknContent.replace(tempString, "")
    #             except Exception as err:
    #                 print(repr(err))
    #                 break
    #         else:
    #             break

    # print("]\n")
    # sys.stdout.flush()

    # # PRINT REMAINDER
    # print("\nORIGINAL:\n{}\n".format(remOrigContent))
    # print("\nBROKEN:\n{}\n".format(remBrknContent))
    # print("Original Size: {}".format(len(remOrigContent)))
    # print("Broken Size:   {}".format(len(remBrknContent)))

    # Attempt #4
    # remOrigContent = origContent
    # remBrknContent = brknContent
    # print("REMOVING ORIGINAL CONTENT FROM BROKEN")
    # print("Original Size:\t{}".format(len(remOrigContent)))
    # print("Broken Size:\t  {}".format(len(remBrknContent)))

    # print("[", end = "")
    # sys.stdout.flush()

    # while True:
    #     print(".", end = "")
    #     sys.stdout.flush()
    #     # Find inner-most dict
    #     try:
    #         tempString = strip_inner_dict(remOrigContent)
    #         # print(tempString)
    #         # break
    #     except Exception as err:
    #         break  # No more dictionaries?
    #     else:
    #         if 0 < len(tempString):
    #             try:
    #                 remOrigContent = remOrigContent.replace(tempString, "")
    #             except Exception as err:
    #                 pass

    #             try:
    #                 remBrknContent = remBrknContent.replace(tempString, "")
    #             except Exception as err:
    #                 print(repr(err))
    #                 break
    #         else:
    #             break

    # print("]\n")
    # sys.stdout.flush()

    # Attempt #5 - Ordering
    newOrigFileName = origFileName.replace(".json", "_new.json")
    newBrknFileName = brknFileName.replace(".json", "_new.json")

    with codecs.open(origFileName, "r", "utf-8-sig") as origUTF8File:
        origUTF8Content = origUTF8File.read()

    with codecs.open(brknFileName, "r", "utf-8-sig") as brknUTF8File:
        brknUTF8Content = brknUTF8File.read()

    origDict = json.loads(origUTF8Content)
    brknDict = json.loads(brknUTF8Content)
    origOrdDict = json.loads(origUTF8Content, object_pairs_hook = OrderedDict)
    brknOrdDict = json.loads(brknUTF8Content, object_pairs_hook = OrderedDict)

    print("origDict is of type {}".format(type(origDict)))
    print("brknDict is of type {}".format(type(brknDict)))
    print("origOrdDict is of type {}".format(type(origOrdDict)))
    print("brknOrdDict is of type {}".format(type(brknOrdDict)))

    # for key in origOrdDict.keys():
    #     print(key)
    # print("")
    # for key in brknOrdDict.keys():
    #     print(key)

    with io.open(newOrigFileName, "w", encoding="utf-8-sig") as outFile:
        json.dump(origOrdDict, outFile, separators=(',', ':'))

    with io.open(newBrknFileName, "w", encoding="utf-8-sig") as outFile:
        json.dump(brknOrdDict, outFile, separators=(',', ':'))

    # # PRINT REMAINDER
    # print("\nORIGINAL:\n{}\n".format(remOrigContent))
    # print("\nBROKEN:\n{}\n".format(remBrknContent))
    # print("Original Size: {}".format(len(remOrigContent)))
    # print("Broken Size:   {}".format(len(remBrknContent)))

    # BONUS ROUND
    # test1 = '"$id":"3466"'
    # test2 = '"$id":"3467"'
    # test3 = '"$id":"3468"'
    # test4 = '"$id":"3469"'
    # test5 = '"$id":"3470"'

    # if test1 in origContent and test1 not in brknContent:
    #     print("Broken content is missing:\t{}".format(test1))
    # if test2 in origContent and test2 not in brknContent:
    #     print("Broken content is missing:\t{}".format(test2))
    # if test3 in origContent and test3 not in brknContent:
    #     print("Broken content is missing:\t{}".format(test3))
    # if test4 in origContent and test4 not in brknContent:
    #     print("Broken content is missing:\t{}".format(test4))
    # if test5 in origContent and test5 not in brknContent:
    #     print("Broken content is missing:\t{}".format(test5))


if __name__ == "__main__":
    main()