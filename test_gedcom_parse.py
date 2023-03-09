import unittest
from datetime import datetime
import pymongo
from gedcom_parse import readGEDCOM, printIndividuals, printFamilies, checkMarriageBeforeDeath, checkDivorceBeforeDeath


class TestGEDCOMParse(unittest.TestCase):
    """class to test gedcom_parse.py"""
    
    myclient = pymongo.MongoClient("mongodb+srv://Christian:6TYXxCt9Sp9GDO20@cluster0.iilq4vg.mongodb.net/?retryWrites=true&w=majority")
    mydb = myclient["db"]
    for x in readGEDCOM('Christian_Huang_Tree.ged', mydb):
        print(x)
    for x in printIndividuals(mydb):
        print(x)
    for x in printFamilies(mydb):
        print(x)
    
    # def test_check_marriage_before_death(self):
    #     """tests to see if right triangle is correctly outputted"""
    #     myclient = pymongo.MongoClient("mongodb+srv://Christian:6TYXxCt9Sp9GDO20@cluster0.iilq4vg.mongodb.net/?retryWrites=true&w=majority")
    #     mydb = myclient["db"]
    #     res = ["Error @F1@:Marriage date of Carlos /Salamanca/ (@I2@) occurs before his death date.","Error @F1@:Marriage date of Miriam /MartÃ­nez/ (@I1@) occurs before her death date.","Error @F4@:Divorce date of Francesca /Liddy/ (@I15@) occurs before her death date."]
    #     self.assertEqual(checkMarriageBeforeDeath(mydb),res,'3,4,5 should be a Right triangle')