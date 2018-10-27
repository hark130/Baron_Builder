from json_file_class import JsonFile
import os
import unittest


class Json_File_Class_Tests(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        self.fileList = []
        self.contentList = []
        self.defFileContent = ""
        with open(os.path.join("Test_Files", "header.json"), "r") as inFile:
            self.defFileContent = inFile.read()
        super().__init__(*args, **kwargs)


    def create_file(self, filename, contents):
        # INPUT VALIDATION
        # filename
        if isinstance(filename, list):
            self.fileList = filename
        elif isinstance(filename, str):
            self.fileList.append(filename)
        else:
            raise TypeError("filename is the wrong data type")
        # contents
        if isinstance(contents, list):
            self.contentList = contents
        elif isinstance(contents, str):
            self.contentList.append(contents)
        else:
            raise TypeError("contents is the wrong data type")
        # Number of files
        if len(self.fileList) <= 0:
            raise ValueError("Empty file list")
        # Number of contents
        if len(self.contentList) <= 0:
            raise ValueError("Empty content list")

        # MAKE FILES
        for fName in self.fileList:
            for fContent in self.contentList:
                with open(fName, "w") as outFile:
                    outFile.write(fContent)


    def __del__(self):
        if isinstance(self.fileList, list):
            if len(self.fileList) > 0:
                for fName in self.fileList:
                    if os.path.isfile(fName):
                        os.remove(fName)


class Json_File_Class_Test_Normal(Json_File_Class_Tests):


    def test_Normal_01_Read(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Normal01.json")
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)


    def test_Normal_02_Parse(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Normal02.json")
        expectResults = {"$id":"1","Name":"Barony's Capital - 30 Erastus (VII) 4711 - 13:54:43","Description":"The barony teeters on the edge. Where will its destiny lead — salvation, or damnation? The baron's last hope is to identify the source of the troubles in his lands over the last few months and put an end to the horrible events that could well lead the country to its final fall.","GameName":"Yuhra Thorne","Type":"Manual","IsAutoLevelupSave":False,"QuickSaveNumber":0,"LoadedTimes":0,"Area":"173c1547502bb7243ad94ef8eec980d0"}
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)
        for key in expectResults.keys():
            try:
                self.assertTrue(test.fDict[key] == expectResults[key])
            except KeyError as err:
                self.fail()
            except Exception as err:
                print(repr(err))


    def test_Normal_03_Mod(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Normal03.json")
        expectResults = {"$id":"2","Name":"Barony's Capital - 30 Erastus (VII) 4711 - 13:54:43","Description":"Yuhra is awesome!","GameName":"Yuhra Thorne","Type":"Manual","IsAutoLevelupSave":True,"QuickSaveNumber":1,"LoadedTimes":0,"Area":"173c1547502bb7243ad94ef8eec980d0"}
        changes = {"$id":"2", "Description":"Yuhra is awesome!", "IsAutoLevelupSave":True, "QuickSaveNumber":1}
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())
        # Modify existing data
        for key in changes.keys():
            test.changed = False
            try:
                self.assertTrue(test.mod_data(key, changes[key]))
            except Except as err:
                print(repr(err))
                raise(err)
            else:
                self.assertTrue(test.changed)
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)
        for key in expectResults.keys():
            try:
                self.assertTrue(test.fDict[key] == expectResults[key])
            except KeyError as err:
                self.fail()
            except Exception as err:
                print(repr(err))


    def test_Normal_04_Add(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Normal04.json")
        expectResults = {"String" : "To string",
                         "Tuple" : ("To", "Tuple"),
                         "List" : ["To", "a", "list", 1, 2, 3, 4],
                         "Dictionary" : {"to":"a","dict":"ionary"},
                         "Bool1" : True,
                         "Bool2" : False,
                         "Integer" : 1337 }
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())
        # Modify existing data
        for key in expectResults.keys():
            test.changed = False
            try:
                self.assertTrue(test.add_data(key, expectResults[key]))
            except Except as err:
                print(repr(err))
                raise(err)
            else:
                self.assertTrue(test.changed)
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)
        for key in expectResults.keys():
            try:
                self.assertTrue(test.fDict[key] == expectResults[key])
            except KeyError as err:
                self.fail()
            except Exception as err:
                print(repr(err))


    def test_Normal_05_Del(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Normal05.json")
        expectResults = {"$id":"1","Name":"Barony's Capital - 30 Erastus (VII) 4711 - 13:54:43","Description":"The barony teeters on the edge. Where will its destiny lead — salvation, or damnation? The baron's last hope is to identify the source of the troubles in his lands over the last few months and put an end to the horrible events that could well lead the country to its final fall.","GameName":"Yuhra Thorne","Type":"Manual","IsAutoLevelupSave":False,"QuickSaveNumber":0,"LoadedTimes":0,"Area":"173c1547502bb7243ad94ef8eec980d0"}
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())
        # Modify existing data
        for key in expectResults.keys():
            test.changed = False
            try:
                self.assertTrue(test.del_data(key))
            except Except as err:
                print(repr(err))
                raise(err)
            else:
                self.assertTrue(test.changed)
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)
        for key in expectResults.keys():
            try:
                self.assertTrue(key not in test.fDict.keys())
            except KeyError as err:
                self.fail()
            except Exception as err:
                print(repr(err))


    def test_Normal_06_Write(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Normal05.json")
        expectResults = {"$id":"1","Name":"Barony's Capital - 30 Erastus (VII) 4711 - 13:54:43","Description":"The barony teeters on the edge. Where will its destiny lead — salvation, or damnation? The baron's last hope is to identify the source of the troubles in his lands over the last few months and put an end to the horrible events that could well lead the country to its final fall.","GameName":"Yuhra Thorne","Type":"Manual","IsAutoLevelupSave":False,"QuickSaveNumber":0,"LoadedTimes":0,"Area":"173c1547502bb7243ad94ef8eec980d0"}
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())
        # Modify existing data
        for key in expectResults.keys():
            test.changed = False
            try:
                self.assertTrue(test.del_data(key))
            except Except as err:
                print(repr(err))
                raise(err)
            else:
                self.assertTrue(test.changed)
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)
        for key in expectResults.keys():
            try:
                self.assertTrue(key not in test.fDict.keys())
            except KeyError as err:
                self.fail()
            except Exception as err:
                print(repr(err))
        # Write the file
        self.assertTrue(test.write_json_file())
        results = JsonFile(inFilename)
        self.assertTrue(results.read_json_file())
        self.assertTrue(results.parse_json_contents())
        # Verify data is missing
        for key in expectResults.keys():
            self.assertFalse(results.changed)
            self.assertFalse(results.key_present(key))
            self.assertFalse(results.changed)


class Json_File_Class_Test_Error(Json_File_Class_Tests):


    def test_Error_01_Read(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Error01.json")
        test = JsonFile(inFilename)
        self.assertFalse(test.read_json_file())
        self.assertFalse(test.fCont)


    def test_Error_02_Parse(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Error02.json")
        self.create_file(inFilename, "This is not a JSON formatted file")
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        try:
            self.assertFalse(test.parse_json_contents())
        except JSONDecodeError as err:
            self.assertTrue(True)  # More fidelilty
        except Exception as err:
            self.fail("Raised wrong exception")
        self.assertFalse(test.fDict)


    def test_Error_03_Mod(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Error03.json")
        expectResults = {"$id":"1","Name":"Barony's Capital - 30 Erastus (VII) 4711 - 13:54:43","Description":"The barony teeters on the edge. Where will its destiny lead — salvation, or damnation? The baron's last hope is to identify the source of the troubles in his lands over the last few months and put an end to the horrible events that could well lead the country to its final fall.","GameName":"Yuhra Thorne","Type":"Manual","IsAutoLevelupSave":False,"QuickSaveNumber":0,"LoadedTimes":0,"Area":"173c1547502bb7243ad94ef8eec980d0"}
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())
        # Attempt to modify nonexistent data
        self.assertFalse(test.mod_data("$id ", "2"))
        self.assertFalse(test.mod_data("description", "Yuhra is awesome!"))
        self.assertFalse(test.mod_data("Is4utoLevelupSave", True))
        self.assertFalse(test.mod_data("Quick_Save_Number", 1))
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)
        for key in expectResults.keys():
            try:
                self.assertTrue(test.fDict[key] == expectResults[key])
            except KeyError as err:
                self.fail()
            except Exception as err:
                print(repr(err))


    def test_Error_04_Add(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Error04.json")
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())

        # Attempt to add existing data
        self.assertFalse(test.add_data("$id", "2"))
        self.assertFalse(test.add_data("Description", "Yuhra is awesome!"))
        self.assertFalse(test.add_data("IsAutoLevelupSave", True))
        self.assertFalse(test.add_data("QuickSaveNumber", 1))

        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)


    def test_Error_05_Del(self):
        inFilename = os.path.join("Test_Files", "Json_File_Class_Test_Error05.json")
        expectResults = {"delete":"this", "This key":["does", "not", "exist"], "key here":False, "How many keys named this?":0}
        self.create_file(inFilename, self.defFileContent)
        test = JsonFile(inFilename)
        self.assertTrue(test.read_json_file())
        self.assertTrue(test.parse_json_contents())
        # Modify existing data
        for key in expectResults.keys():
            test.changed = False
            try:
                self.assertFalse(test.del_data(key))
            except Except as err:
                print(repr(err))
                raise(err)
            else:
                self.assertFalse(test.changed)
        # Use .find() to avoid BOM headers
        self.assertTrue(self.defFileContent.find(test.fCont) >= 0)


class Json_File_Class_Test_Boundary(Json_File_Class_Tests):


    def test_Boundary_01(self):
        self.assertTrue(True)


class Json_File_Class_Test_Special(Json_File_Class_Tests):


    def test_Special_01(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main(verbosity = 2, exit = False)
