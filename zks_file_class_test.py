from baron_builder import TOP_DIR as TOP_DIR          # Store everything in there
from baron_builder import ARCHIVE_DIR as ARCHIVE_DIR  # Move archived save files here
from baron_builder import BACKUP_DIR as BACKUP_DIR    # Backup save files here
from baron_builder import WORKING_DIR as WORKING_DIR  # Use this directory to unarchive and modify save games
from zks_file_class import ZksFile
import os


def main():
    # START
    print("")
    funcTestSuccess = True

    # 1. Open File
    if funcTestSuccess:
        try:
            testFilename = "ZksFile_Test_Smallest_Save_Game.zks"
            testAbsFilename = os.path.join(os.getcwd(), "Test_Files", testFilename)
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
        except Exception as err:
            print("[ ] Failed to unpack {}".format(testFilename))
            print("\n{}".format(repr(err)))
            funcTestSuccess = False
        else:
            if not testObj.zSuccess:
                print("[ ] Failed to unpack {}".format(testFilename))
                funcTestSuccess = False


    # FINISH
    print("")

if __name__ == "__main__":
    main()
