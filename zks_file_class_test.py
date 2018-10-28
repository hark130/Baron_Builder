from baron_builder import TOP_DIR as TOP_DIR          # Store everything in there
from baron_builder import ARCHIVE_DIR as ARCHIVE_DIR  # Move archived save files here
from baron_builder import BACKUP_DIR as BACKUP_DIR    # Backup save files here
from baron_builder import WORKING_DIR as WORKING_DIR  # Use this directory to unarchive and modify save games
from shutil import copyfile
from zks_file_class import ZksFile
import os


def main():
    # START
    print("")
    funcTestSuccess = True
    # Is this save file missing key elements because it's too early in the game?
    # testFilename = "ZksFile_Test_Smallest_Save_Game.zks"
    # testFilename = "ZksFile_Test_Medium_Save_Game.zks"
    testFilename = "ZksFile_Test_Recent_Save_Game.zks"
    testAbsFilename = os.path.join(os.getcwd(), "Test_Files", testFilename)

    # 0. Backup File
    if funcTestSuccess:
        # A. Remove any existing back up of the file
        try:
            os.remove(testAbsFilename + ".bak")
        except Exception as err:
            pass  # It's ok if it's not there

        # B. Rename the original to back up
        try:
            copyfile(testAbsFilename, testAbsFilename + ".bak")
        except Exception as err:
            print("[ ] Failed to backup {}".format(testAbsFilename))
            print("\n{}".format(repr(err)))
            funcTestSuccess = False
        else:
            print("[X] Backed up {} to {}".format(testAbsFilename, testFilename + ".bak"))

    # 1. Open File
    if funcTestSuccess:
        try:
            testObj = ZksFile(testAbsFilename)
        except Exception as err:
            print("[ ] Failed to open {}".format(testAbsFilename))
            print("\n{}".format(repr(err)))
            funcTestSuccess = False
        else:
            if testObj.zSuccess:
                print("[X] Opened {}".format(testAbsFilename))
            else:
                print("[ ] Failed to open {}".format(testAbsFilename))
                funcTestSuccess = False

    # 2. Unpack File
    if funcTestSuccess:
        try:
            if testObj.unpack_file(os.path.join(TOP_DIR, WORKING_DIR)):
                print("[X] Unpacked {}".format(testFilename))
            else:
                print("[ ] Failed to unpack {}".format(testFilename))
                funcTestSuccess = False
        except Exception as err:
            print("[ ] Failed to unpack {}".format(testFilename))
            print("\n{}".format(repr(err)))
            funcTestSuccess = False
        else:
            if funcTestSuccess and testObj.zSuccess is False:
                print("[ ] Failed to unpack {}\n... in a buggy way".format(testFilename))
                funcTestSuccess = False

    # 3. Load Data
    if funcTestSuccess:
        try:
            if testObj.load_data():
                print("[X] Data loaded")
            else:
                print("[ ] Failed to load data")
                funcTestSuccess = False
        except Exception as err:
            print("[ ] Failed to load data")
            print("\n{}".format(repr(err)))
            funcTestSuccess = False
        else:
            if funcTestSuccess and testObj.zSuccess is False:
                print("[ ] Failed to load data... in a buggy way")
                funcTestSuccess = False

    # 4. Read Actual Data
    if funcTestSuccess:
        key0 = "Kingdom"
        key1 = "Money"
        val0 = None
        val1 = None

        try:
            val0 = testObj.zPlayFile.get_data(key0)
            val1 = testObj.zPlayFile.get_data(key1)
        except Exception as err:
            print("[ ] Failed to read game data")
            print("\n{}".format(repr(err)))
            funcTestSuccess = False
        else:
            if testObj.zSuccess and testObj.zPlayFile.jSuccess:
                print("[X] Game data read")
                if val1 is not None:
                    print("\tYou appear to have {} gold".format(val1))
                if isinstance(val0, dict):
                    print("\tYour unrest level is:\t{}".format(val0["Unrest"]))
                else:
                    print("\nThis is not a dict.  It's a {}.".format(type(val0)))

    # 5. Modify Actual Data
    if funcTestSuccess:
        kingKey = "Kingdom"
        kingDict = {}
        newKingDict = {}
        moneyKey = "Money"
        moneyVal = 0
        newMoneyVal = 0

        try:
            # "Kingdom"
            kingDict = testObj.zPlayFile.get_data(kingKey)
            kingDict["Unrest"] = "Worried"
            testObj.zPlayFile.mod_data(kingKey, kingDict)
            # "Money"
            moneyVal = testObj.zPlayFile.get_data(moneyKey)
            moneyVal = moneyVal * 2
            testObj.zPlayFile.mod_data(moneyKey, moneyVal)
        except Exception as err:
            print("[ ] Failed to write game data")
            print("\n{}".format(repr(err)))
            funcTestSuccess = False
        else:
            if testObj.zSuccess and testObj.zPlayFile.jSuccess:
                newKingDict = testObj.zPlayFile.get_data(kingKey)
                newMoneyVal = testObj.zPlayFile.get_data(moneyKey)
                if newKingDict["Unrest"] == kingDict["Unrest"] and newMoneyVal == moneyVal:
                    print("[X] Game data modified")
                    print("\tYou NOW have {} gold".format(newMoneyVal))
                    print("\tYour unrest level is NOW:\t{}".format(newKingDict["Unrest"]))
                else:
                    print("[ ] Failed to write game data")
                    funcTestSuccess = False

    # 6. Save New Game Data
    if funcTestSuccess:
        try:
            if testObj.save_json_files() is not True:
                print("[ ] Game data failed to save")
            else:
                print("[X] Game data saved")
        except Exception as err:
            print("[ ] Failed to save game data")
            print("\n{}".format(repr(err)))
            funcTestSuccess = False

    # 7. Update Old Save Game With New Data
    if funcTestSuccess:
        try:
            if testObj.update_zks() is not True:
                print("[ ] Failed to create new save game")
            else:
                print('[X] New save game "{}" created'.format(testFilename))
        except Exception as err:
            print("[ ] Failed to create new save game")
            print("\n{}".format(repr(err)))
            funcTestSuccess = False

    # X. Close ZksFile Object
    # Accomplish this step last regardless of funcTestSuccess
    try:
        if testObj is not None and testObj.close_zks() is not True:
            print("[ ] Failed to close")
        else:
            print("[X] Successfully closed")
    except Exception as err:
        print("[ ] Failed to close")
        print("\n{}".format(repr(err)))
        funcTestSuccess = False

    # FINISH
    print("")

if __name__ == "__main__":
    main()
