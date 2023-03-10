import unittest
from datetime import datetime
import pymongo
from gedcom_parse import readGEDCOM, printIndividuals, printFamilies, checkBirthBeforeDeath, checkMarriageBeforeDivorce, checkMarriageBeforeDeath, checkDivorceBeforeDeath, checkOver150, checkDatesBeforeCurrent, checkBirthBeforeMarriageAfterDivorce, checkBirthBeforeMarriage


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

    def test_checkBirthBeforeDeath(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ["Error @F1@: Birth date of Miriam /MartÃ­nez/@I1@ occurs after their death date."]
        self.assertEqual(checkBirthBeforeDeath(mydb), res,
                         'result does not match expected result for date check of birth death')

    def test_checkMarriageBeforeDivorce(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ["Error @F1@: Marriage date of Miriam /MartÃ­nez/ and Carlos /Salamanca/ occurs after their divorce date."]
        self.assertEqual(checkMarriageBeforeDivorce(mydb), res,
                         'result does not match expected result for date check of marriage after divorce')

    def test_checkMarriageBeforeDeath(self):
        self.maxDiff = None
        """tests to see if right triangle is correctly outputted"""
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ["Error @F1@:Marriage date of Carlos /Salamanca/ (@I2@) occurs after his death date.",
               "Error @F1@:Marriage date of Miriam /MartÃ­nez/ (@I1@) occurs after her death date."]
        self.assertEqual(checkMarriageBeforeDeath(mydb), res,
                         'result does not match expected result for date check of marriage after death')

    def test_checkDivorceBeforeDeath(self):
        self.maxDiff = None
        """tests to see if right triangle is correctly outputted"""
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @F4@:Divorce date of Francesca /Liddy/ (@I15@) occurs after her death date."]
        self.assertEqual(checkDivorceBeforeDeath(mydb), res,
                         'result does not match expected result for date check of divorce after death')

    def test_birth_before_marriage(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @F5@:Marriage date of Marie /Schrader/ (@I8@) occurs before her birth."]
        self.assertEqual(checkBirthBeforeMarriage(mydb), res,
                         'result does not match expected result for date check of birth before marriage')

    def test_date_before_current_date(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @I8@: Birth date of Marie /Schrader/ occurs after the current date."]
        self.assertEqual(checkDatesBeforeCurrent(mydb), res,
                         'result does not match expected result for checking date against the current date')


    def test_checkOver150(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomaly @F1@: Death date of Carlos /Salamanca/@I2@ occurs  150 (or more) years after their birth date']
        self.assertEqual(checkOver150(mydb), res,
                         'result does not match expected result for date check of birth death')
        
    def test_checkBirthBeforeMarriageAfterDivorce(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Anomaly @F1@: Hector /Salamanca/@I3@ was born before the marriage of marriage of their parents',
            'Anomaly @F1@: Eduardo /Salamanca/@I5@ was born before the marriage of marriage of their parents',
            'Anomaly @F1@: Marco /Salamanca/@I7@ was born before the marriage of marriage of their parents',
            'Anomaly @F5@: Lalo /Salamanca/@I11@ was born before the marriage of marriage of their parents',
            'Anomaly @F3@: Gretchen /Salamanca/@I12@ was born before the marriage of marriage of their parents',
            'Anomaly @F4@: Leonel /Salamanca/@I16@ was born 9 months after the divorce of his parents'
            ]
        self.assertEqual(checkBirthBeforeMarriageAfterDivorce(mydb), res,
                         'result does not match expected result for date check of birth death')
        
        
if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
