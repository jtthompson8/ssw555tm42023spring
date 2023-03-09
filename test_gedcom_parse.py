import unittest
from datetime import datetime
import pymongo
from gedcom_parse import readGEDCOM, printIndividuals, printFamilies, checkBirthBeforeDeath, checkMarriageBeforeDivorce, checkMarriageBeforeDeath, checkDivorceBeforeDeath


class TestGEDCOMParse(unittest.TestCase):
    """class to test gedcom_parse.py"""

    myclient = pymongo.MongoClient(
        "mongodb://localhost:27017")
    mydb = myclient["db"]
    for x in readGEDCOM('Christian_Huang_Tree.ged', mydb):
        print(x)
    for x in printIndividuals(mydb):
        print(x)
    for x in printFamilies(mydb):
        print(x)

    def test_marriage_after_divorce(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @F1@: Birth date of Miriam /MartÃ­nez/ occurs after their death date."]
        self.assertEqual(checkBirthBeforeDeath(mydb), res,
                         'result does not match expected result for date check of birth death')

    def test_marriage_after_divorce(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ["Error @F1@: Marriage date of Miriam /MartÃ­nez/ and Carlos /Salamanca/ occurs after their divorce date."]
        self.assertEqual(checkMarriageBeforeDivorce(mydb), res,
                         'result does not match expected result for date check of marriage after divorce')


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
