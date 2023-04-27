import unittest
from datetime import datetime
import pymongo
from gedcom_parse import readGEDCOM, printIndividuals, printFamilies, checkBirthBeforeDeath, checkMarriageBeforeDivorce, checkMarriageBeforeDeath, checkDivorceBeforeDeath, checkOver150, checkDatesBeforeCurrent, checkBirthBeforeMarriageAfterDivorce, checkBirthBeforeMarriage, checkBirthBeforeDeathOfParents, checkMarriageAfterFourteen, checkSiblingsBornSame, checkSiblingSpacing, checkFifteenSiblings, checkMaleLastNames, checkCorrectGenderRole, checkUniqueIds, check_UniqueName_and_BirthDate, check_UniqueFamily_and_MarriageDate, check_aunt_uncle_nephew_niece, check_first_cousins_marriage, checkMarriageDescendants, checkMarriageSibling, listMultipleBirths, listOrphans, checkAgeGap, checkRecentBirths, checkLivingMarried, checkLivingSingle


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
    for x in checkBirthBeforeDeath(mydb):
        print(x)
    for x in checkMarriageBeforeDivorce(mydb):
        print(x) 
    for x in checkMarriageBeforeDeath(mydb):
        print(x)
    for x in checkDivorceBeforeDeath(mydb):
        print(x)
    for x in checkOver150(mydb):
        print(x)
    for x in checkDatesBeforeCurrent(mydb):
        print(x)
    for x in checkBirthBeforeMarriageAfterDivorce(mydb):
        print(x)
    for x in checkBirthBeforeMarriage(mydb):
        print(x)
    for x in checkBirthBeforeDeathOfParents(mydb):
        print(x)
    for x in checkMarriageAfterFourteen(mydb):
        print(x)
    for x in checkSiblingsBornSame(mydb):
        print(x)
    for x in checkSiblingSpacing(mydb):
        print(x)
    for x in checkFifteenSiblings(mydb):
        print(x)
    for x in checkMaleLastNames(mydb):
        print(x)
    for x in checkCorrectGenderRole(mydb):
        print(x)
    for x in checkUniqueIds(mydb):
        print(x)
    for x in check_UniqueName_and_BirthDate(mydb):
        print(x)
    for x in check_UniqueFamily_and_MarriageDate(mydb):
        print(x)
    for x in check_aunt_uncle_nephew_niece(mydb):
        print(x)
    for x in check_first_cousins_marriage(mydb):
        print(x)
    for x in checkMarriageDescendants(mydb):
        print(x)
    for x in checkMarriageSibling(mydb):
        print(x)
    for x in listMultipleBirths(mydb):
        print(x)
    for x in listOrphans(mydb):
        print(x)

    def test_checkBirthBeforeDeath(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            "Error @F1@: Birth date of Miriam /MartÃ­nez/@I1@ occurs after their death date."]
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
        res = [
            'Anomaly @F1@: Death date of Carlos /Salamanca/@I2@ occurs  150 (or more) years after their birth date']
        self.assertEqual(checkOver150(mydb), res,
                         'result does not match expected result for date check of birth death')

    def test_checkBirthBeforeMarriageAfterDivorce(self):
        self.maxDiff = None
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomaly @F1@: Hector /Salamanca/@I3@ was born before the marriage of marriage of their parents', 'Anomaly @F1@: Eduardo /Salamanca/@I5@ was born before the marriage of marriage of their parents', 'Anomaly @F1@: Marco /Salamanca/@I7@ was born before the marriage of marriage of their parents', 'Anomaly @F5@: Lalo /Salamanca/@I11@ was born before the marriage of marriage of their parents', 'Anomaly @F3@: Gretchen /Salamanca/@I12@ was born before the marriage of marriage of their parents', 'Anomaly @F4@: Leonel /Salamanca/@I16@ was born 9 months after the divorce of his parents',
               'Anomaly @F4@: Lennie /Salamanca/@I17@ was born 9 months after the divorce of his parents', 'Anomaly @F4@: Bill /Salamanca/@I18@ was born 9 months after the divorce of his parents', 'Anomaly @F4@: Dan /Salamanca/@I19@ was born 9 months after the divorce of his parents', 'Anomaly @F4@: Amit /Salamanca/@I20@ was born 9 months after the divorce of his parents', 'Anomaly @F4@: Brendan /Salamanca/@I21@ was born 9 months after the divorce of his parents', 'Anomaly @F8@: Dave /White/@I38@ was born before the marriage of marriage of their parents', 'Anomaly @F8@: Stacy /White/@I38@ was born before the marriage of marriage of their parents']
        self.assertEqual(checkBirthBeforeMarriageAfterDivorce(mydb), res,
                         'result does not match expected result for date check of birth death')

    def test_checkBirthBeforeDeathOfParents(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Error @I3@: Death of Miriam /MartÃ­nez/@I1@ occurs before her child was born.',
            'Error @I5@: Death of Miriam /MartÃ­nez/@I1@ occurs before her child was born.',
            'Error @I7@: Death of Miriam /MartÃ­nez/@I1@ occurs before her child was born.'
        ]
        self.assertEqual(checkBirthBeforeDeathOfParents(mydb), res,
                         'result does not match expected result for checking being born before parents die')

    def test_checkMarriageAfterFourteen(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Error @F4@: Eduardo /Salamanca/ married before turning 14'
        ]
        self.assertEqual(checkMarriageAfterFourteen(mydb), res,
                         'result does not match expected result for checking marriage before 14')

    def test_checkSiblingsBornSame(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomaly in @F4@ there are 6 children with the birthday of 5 JUL 1961']
        self.assertEqual(checkSiblingsBornSame(mydb), res,
                         'result does not match expected result for checking more than 5 siblings having the same birthdate')

    def test_checkSiblingSpacing(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomaly in @F4@ child @I16@ and child @I22@ have birthdays within 92 days', 'Anomaly in @F4@ child @I17@ and child @I22@ have birthdays within 92 days', 'Anomaly in @F4@ child @I18@ and child @I22@ have birthdays within 92 days',
               'Anomaly in @F4@ child @I19@ and child @I22@ have birthdays within 92 days', 'Anomaly in @F4@ child @I20@ and child @I22@ have birthdays within 92 days', 'Anomaly in @F4@ child @I21@ and child @I22@ have birthdays within 92 days']
        self.assertEqual(checkSiblingSpacing(mydb), res,
                         'result does not match expected result for checking sibling spacing')

    def test_checkFifteenSiblings(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomaly @F7@: Family has 15 or more siblings']
        self.assertEqual(checkFifteenSiblings(mydb), res,
                         'result does not match expected result for check of fifteens siblings')

    def test_checkMaleLastNames(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Error @F7@: Child9 /Smith/ @I31@ has a different last name than his father Walter /White/ @I13@. All male members of a family should have the same last name.']
        print(checkMaleLastNames(mydb))
        self.assertEqual(checkMaleLastNames(mydb), res,
                         'result does not match expected result for date check of male last names')

    def test_checkCorrectGenderRole(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomaly in family @F1@: Husband is not a male (@I2@)', 'Anomaly in family @F1@: Wife is not a female (@I1@)',
               'Anomaly in family @F8@: Wife is not a female (@I38@)', 'Anomaly in family @F8@: Wife is not a female (@I38@)']
        self.assertEqual(checkCorrectGenderRole(mydb), res,
                         'result does not match expected result for gender check of families')

    def test_checkUniqueIds(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Anomaly: @F8@ is repeated (not unique)', 'Anomaly: @I38@ is repeated (not unique)']
        self.assertEqual(checkUniqueIds(mydb), res,
                         'result does not match expected result for id uniqueness check of individuals and families')

    def test_check_UniqueName_and_BirthDate(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Anomaly: Dave /White/ with a birth date of 11 JAN 1990 appears more than once.']
        print(check_UniqueName_and_BirthDate(mydb))
        self.assertEqual(check_UniqueName_and_BirthDate(mydb), res,
                         'result does not match expected result for unique names and birth dates check')

    def test_check_UniqueFamily_and_MarriageDate(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomaly: Family with the spouses Dave /White/ and Dave /White/ with a marriage date of 6 AUG 2012 appears more than once.']
        print(check_UniqueFamily_and_MarriageDate(mydb))
        self.assertEqual(check_UniqueFamily_and_MarriageDate(mydb), res,
                         'result does not match expected result for unique spouses and marriage dates check')

    def test_check_first_cousins_marriage(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Anomaly Marco /Salamanca/ is married to first cousin Gretchen /Salamanca/']
        print(check_first_cousins_marriage(mydb))
        self.assertEqual(check_UniqueFamily_and_MarriageDate(mydb), res,
                         'result does not match expected result for first cousin marriage check')

    def test_check_aunt_uncle_nephew_niece(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Anomaly Carlos /Salamanca/ is married to their nephew/niece Gretchen /Salamanca/']
        print(check_first_cousins_marriage(mydb))
        self.assertEqual(check_UniqueFamily_and_MarriageDate(mydb), res,
                         'result does not match expected result for aunt/uncle nephew/niece marriage check')
        
    def testcheckMarriageSibling(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            'Error: Carlos /Salamanca/ is married to Miriam /MartÃ\xadnez/ and they are siblings',
            'Error: Dave /White/ is married to Dave /White/ and they are siblings',
            'Error: Dave /White/ is married to Dave /White/ and they are siblings'
        ]
        self.assertEqual(checkMarriageSibling(mydb), res,
                         'result does not match expected result for sibling marriage check')

    def testcheckMarriageDescendant(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = [
            
        ]
        self.assertEqual(checkMarriageDescendants(mydb), res,
                         'result does not match expected result for descendant marriage check')
        
    def testlistMultipleBirths(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomoly: in family @F4@ there are 6 births on 5 JUL 1961', 'Anomoly: in family @F8@ there are 2 births on 11 JAN 1990']
        self.assertEqual(listMultipleBirths(mydb), res,
                         'result does not match expected result for list multiple births')
        
    def testlistOrphans(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = ['Anomoly: in family @F7@, @I37@ is an orphan']
        self.assertEqual(listOrphans(mydb), res,
                         'result does not match expected result for list oprhans')
        

    def test_checkAgeGap(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = "Couples where the older spouse was more than twice the age of the younger spouse: ['@F5@']"
        self.assertEqual(checkAgeGap(mydb), res,
                            'result does not match expected result for age gap list')
        
    def test_checkRecentBirths(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = "People born in the last 30 days: []"
        self.assertEqual(checkRecentBirths(mydb), res,
                            'result does not match expected result for recent births list')
        
    def test_checkLivingMarried(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = "Living married people: ['@I3@', '@I4@', '@I5@', '@I6@', '@I7@', '@I8@']"
        self.assertEqual(checkLivingMarried(mydb), res,
                            'result does not match expected result for living married people list')
        
    def test_checkLivingSingle(self):
        myclient = pymongo.MongoClient(
            "mongodb://localhost:27017")
        mydb = myclient["db"]
        res = "Living single people over 30: ['@I9@', '@I10@', '@I11@', '@I16@', '@I17@', '@I18@', '@I19@', '@I20@', '@I21@', '@I22@', '@I23@', '@I24@', '@I38@', '@I40@', '@I38@']"
        self.assertEqual(checkLivingSingle(mydb), res,
                            'result does not match expected result for living single people list')



if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
