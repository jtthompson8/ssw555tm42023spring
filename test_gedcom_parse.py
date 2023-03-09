import unittest
from datetime import datetime
import pymongo
from gedcom_parse import readGEDCOM, printIndividuals, printFamilies, checkBirthBeforeDeath, checkMarriageBeforeDivorce, checkMarriageAfterDeath, checkDivorceAfterDeath, checkBirthBeforeMarriage, checkDatesBeforeCurrent


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

    def test_marriage_after_death(self):
        self.maxDiff = None
        """tests to see if right triangle is correctly outputted"""
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ["Error @F1@:Marriage date of Carlos /Salamanca/ (@I2@) occurs after his death date.",
               "Error @F1@:Marriage date of Miriam /MartÃ­nez/ (@I1@) occurs after her death date."]
        self.assertEqual(checkMarriageAfterDeath(mydb), res,
                         'result does not match expected result for date check of marriage after death')

    def test_divorce_after_death(self):
        self.maxDiff = None
        """tests to see if right triangle is correctly outputted"""
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @F4@:Divorce date of Francesca /Liddy/ (@I15@) occurs after her death date."]
        self.assertEqual(checkDivorceAfterDeath(mydb), res,
                         'result does not match expected result for date check of divorce after death')

def test_birth_before_marriage(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @F5@: Birth date of Marie /Schrader/ occurs before the current date."]
        self.assertEqual(checkBirthBeforeMarriage(mydb), res,
                         'result does not match expected result for checking date against the current date')

def test_date_before_current_date(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @F2@: Birth date of Skylar /White/ occurs before their marriage date."]
        self.assertEqual(checkDatesBeforeCurrent(mydb), res,
                         'result does not match expected result for date check of birth marriage')


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
