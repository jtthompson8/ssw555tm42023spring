import unittest
from datetime import datetime
import pymongo
from gedcom_parse import readGEDCOM, printIndividuals, printFamilies, checkMarriageAfterDeath, checkDivorceAfterDeath


class TestGEDCOMParse(unittest.TestCase):
    """class to test gedcom_parse.py"""

    myclient = pymongo.MongoClient(
        "mongodb+srv://Christian:6TYXxCt9Sp9GDO20@cluster0.iilq4vg.mongodb.net/?retryWrites=true&w=majority")
    mydb = myclient["db"]
    for x in readGEDCOM('Christian_Huang_Tree.ged', mydb):
        print(x)
    for x in printIndividuals(mydb):
        print(x)
    for x in printFamilies(mydb):
        print(x)

    def test_marriage_after_death(self):
        self.maxDiff = None
        """tests to see if right triangle is correctly outputted"""
        myclient = pymongo.MongoClient(
            "mongodb+srv://Christian:6TYXxCt9Sp9GDO20@cluster0.iilq4vg.mongodb.net/?retryWrites=true&w=majority")
        mydb = myclient["db"]
        res = ["Error @F1@:Marriage date of Carlos /Salamanca/ (@I2@) occurs after his death date.",
               "Error @F1@:Marriage date of Miriam /MartÃ­nez/ (@I1@) occurs after her death date."]
        self.assertEqual(checkMarriageAfterDeath(mydb), res,
                         'result does not match expected result for date check of marriage after death')

    def test_divorce_after_death(self):
        self.maxDiff = None
        """tests to see if right triangle is correctly outputted"""
        myclient = pymongo.MongoClient(
            "mongodb+srv://Christian:6TYXxCt9Sp9GDO20@cluster0.iilq4vg.mongodb.net/?retryWrites=true&w=majority")
        mydb = myclient["db"]
        res = [
            "Error @F4@:Divorce date of Francesca /Liddy/ (@I15@) occurs after her death date."]
        self.assertEqual(checkDivorceAfterDeath(mydb), res,
                         'result does not match expected result for date check of divorce after death')


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
