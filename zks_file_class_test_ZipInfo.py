import zipfile


def compare_two_things(thing1, thing2):
    # LOCAL VARIABLES
    retVal = True

    # Type
    if type(thing1) != type(thing2):
        print("\tType Mismatch")
        print("\tFirst is type  {}".format(type(thing1)))
        print("\tSecond is type {}".format(type(thing2)))
        retVal = False
    # Value
    else:
        if thing1 != thing2:
            print("\tValue Mismatch")
            print("\tFirst is value  {}".format(thing1))
            print("\tSecond is value {}".format(thing2))
            retVal = False

    return retVal


def same_ZipInfo_objs(obj1, obj2):
    '''
        PURPOSE - Compare two ZipInfo objects
        OUTPUT
            True if they're the same
            False if they're different
    '''
    # LOCAL VARIABLES
    retVal = True

    # INPUT VALIDATION
    if not isinstance(obj1, zipfile.ZipInfo):
        raise TypeError("Bad type")
    elif not isinstance(obj2, zipfile.ZipInfo):
        raise TypeError("Bad type")

    # COMPARE
    if not compare_two_things(obj1.CRC, obj2.CRC):
        retVal = False
        print("CRC\n")
    # if not compare_two_things(obj1.FileHeader, obj2.FileHeader):
    #     retVal = False
    #     print("FileHeader\n")
    # if not compare_two_things(obj1.__class__, obj2.__class__):
    #     retVal = False
    #     print("__class__\n")
    # if not compare_two_things(obj1.__delattr__, obj2.__delattr__):
    #     retVal = False
    #     print("__delattr__\n")
    # if not compare_two_things(obj1.__dir__, obj2.__dir__):
    #     retVal = False
    #     print("__dir__\n")
    # if not compare_two_things(obj1.__doc__, obj2.__doc__):
    #     retVal = False
    #     print("__doc__\n")
    # if not compare_two_things(obj1.__eq__, obj2.__eq__):
    #     retVal = False
    #     print("__eq__\n")
    # if not compare_two_things(obj1.__format__, obj2.__format__):
    #     retVal = False
    #     print("__format__\n")
    # if not compare_two_things(obj1.__ge__, obj2.__ge__):
    #     retVal = False
    #     print("__ge__\n")
    # if not compare_two_things(obj1.__getattribute__, obj2.__getattribute__):
    #     retVal = False
    #     print("__getattribute__\n")
    # if not compare_two_things(obj1.__gt__, obj2.__gt__):
    #     retVal = False
    #     print("__gt__\n")
    # if not compare_two_things(obj1.__hash__, obj2.__hash__):
    #     retVal = False
    #     print("__hash__\n")
    # if not compare_two_things(obj1.__init__, obj2.__init__):
    #     retVal = False
    #     print("__init__\n")
    # if not compare_two_things(obj1.__le__, obj2.__le__):
    #     retVal = False
    #     print("__le__\n")
    # if not compare_two_things(obj1.__lt__, obj2.__lt__):
    #     retVal = False
    #     print("__lt__\n")
    # if not compare_two_things(obj1.__module__, obj2.__module__):
    #     retVal = False
    #     print("__module__\n")
    # if not compare_two_things(obj1.__ne__, obj2.__ne__):
    #     retVal = False
    #     print("__ne__\n")
    # if not compare_two_things(obj1.__new__, obj2.__new__):
    #     retVal = False
    #     print("__new__\n")
    # if not compare_two_things(obj1.__reduce__, obj2.__reduce__):
    #     retVal = False
    #     print("__reduce__\n")
    # if not compare_two_things(obj1.__reduce_ex__, obj2.__reduce_ex__):
    #     retVal = False
    #     print("__reduce_ex__\n")
    # if not compare_two_things(obj1.__repr__, obj2.__repr__):
    #     retVal = False
    #     print("__repr__\n")
    # if not compare_two_things(obj1.__setattr__, obj2.__setattr__):
    #     retVal = False
    #     print("__setattr__\n")
    # if not compare_two_things(obj1.__sizeof__, obj2.__sizeof__):
    #     retVal = False
    #     print("__sizeof__\n")
    if not compare_two_things(obj1.__slots__, obj2.__slots__):
        retVal = False
        print("__slots__\n")
    # if not compare_two_things(obj1.__str__, obj2.__str__):
    #     retVal = False
    #     print("__str__\n")
    if not compare_two_things(obj1.__subclasshook__, obj2.__subclasshook__):
        retVal = False
        print("__subclasshook__\n")
    # if not compare_two_things(obj1._decodeExtra, obj2._decodeExtra):
    #     retVal = False
    #     print("_decodeExtra\n")
    # if not compare_two_things(obj1._encodeFilenameFlags, obj2._encodeFilenameFlags):
    #     retVal = False
    #     print("_encodeFilenameFlags\n")

    # VALID BUT NOISY #
    # if not compare_two_things(obj1._raw_time, obj2._raw_time):
    #     retVal = False
    #     print("_raw_time\n")
    # VALID BUT NOISY #

    if not compare_two_things(obj1.comment, obj2.comment):
        retVal = False
        print("comment\n")
    if not compare_two_things(obj1.compress_size, obj2.compress_size):
        retVal = False
        print("compress_size\n")
    if not compare_two_things(obj1.compress_type, obj2.compress_type):
        retVal = False
        print("compress_type\n")
    if not compare_two_things(obj1.create_system, obj2.create_system):
        retVal = False
        print("create_system\n")
    if not compare_two_things(obj1.create_version, obj2.create_version):
        retVal = False
        print("create_version\n")

    # VALID BUT NOISY #
    # if not compare_two_things(obj1.date_time, obj2.date_time):
    #     retVal = False
    #     print("date_time\n")
    # VALID BUT NOISY #

    if not compare_two_things(obj1.external_attr, obj2.external_attr):
        retVal = False
        print("external_attr\n")
    if not compare_two_things(obj1.extra, obj2.extra):
        retVal = False
        print("extra\n")
    if not compare_two_things(obj1.extract_version, obj2.extract_version):
        retVal = False
        print("extract_version\n")
    if not compare_two_things(obj1.file_size, obj2.file_size):
        retVal = False
        print("file_size\n")
    if not compare_two_things(obj1.filename, obj2.filename):
        retVal = False
        print("filename\n")
    if not compare_two_things(obj1.flag_bits, obj2.flag_bits):
        retVal = False
        print("flag_bits\n")

    # VALID BUT NOISY #
    # if not compare_two_things(obj1.header_offset, obj2.header_offset):
    #     retVal = False
    #     print("header_offset\n")
    # VALID BUT NOISY #
    
    if not compare_two_things(obj1.internal_attr, obj2.internal_attr):
        retVal = False
        print("internal_attr\n")
    if not compare_two_things(obj1.orig_filename, obj2.orig_filename):
        retVal = False
        print("orig_filename\n")
    if not compare_two_things(obj1.reserved, obj2.reserved):
        retVal = False
        print("reserved\n")
    if not compare_two_things(obj1.volume, obj2.volume):
        retVal = False
        print("volume\n")

    # DONE
    return retVal


def main():
    # firstZipFile = "/home/joe/Documents/Personal/Programming/Baron_Builder/Test_Files/ZksFile_Test_Recent_Save_Game.zks.bak"
    firstZipFile = "/home/joe/.config/unity3d/Owlcat Games/Pathfinder Kingmaker/Saved Games/Manual_475_Wilderness_Encounter___10_Arodus__VIII__4711___01_04_26.zks"
    # secondZipFile = "/home/joe/Documents/Personal/Programming/Baron_Builder/Test_Files/ZksFile_Test_Recent_Save_Game.zks"
    # secondZipFile = "/home/joe/.config/unity3d/Owlcat Games/Pathfinder Kingmaker/Saved Games/Baron_Builder/Archive/Manual_475_Wilderness_Encounter___10_Arodus__VIII__4711___01_04_26.bba"
    secondZipFile = "/home/joe/.config/unity3d/Owlcat Games/Pathfinder Kingmaker/Saved Games/Backup/Manual_475_Wilderness_Encounter___10_Arodus__VIII__4711___01_04_26.zks"

    firstZipObj = zipfile.ZipFile(firstZipFile, "r")
    secondZipObj = zipfile.ZipFile(secondZipFile, "r")

    firstZipInfoList = firstZipObj.infolist()
    secondZipInfoList = secondZipObj.infolist()

    if len(firstZipInfoList) == len(secondZipInfoList):
        for index in range(len(firstZipInfoList)):
            print("{}".format(firstZipInfoList[index].filename))
            same_ZipInfo_objs(firstZipInfoList[index], secondZipInfoList[index])
    else:
        raise RuntimeError("Mismatch in list length")



if __name__ == "__main__":
    main()


'''
CRC
FileHeader
__class__
__delattr__
__dir__
__doc__
__eq__
__format__
__ge__
__getattribute__
__gt__
__hash__
__init__
__le__
__lt__
__module__
__ne__
__new__
__reduce__
__reduce_ex__
__repr__
__setattr__
__sizeof__
__slots__
__str__
__subclasshook__
_decodeExtra
_encodeFilenameFlags
_raw_time
comment
compress_size
compress_type
create_system
create_version
date_time
external_attr
extra
extract_version
file_size
filename
flag_bits
header_offset
internal_attr
orig_filename
reserved
volume

'''