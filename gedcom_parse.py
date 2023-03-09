from prettytable import PrettyTable
import pymongo
from datetime import datetime
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["db"]


def readGEDCOM(file, mydb):
    res = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]

    tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
            'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

    dic = {}
    first_indi = True
    first_fam = True
    birthDate = False
    deathDate = False
    divDate = False
    with open(file, 'r') as ged:
        for line in ged:
            info = line.strip().split(' ', 2)
            # print(info)
            res.append(info)
            # lvl, tag, args
            # print("--> " + line.strip())
            res.append("--> " + line.strip())
            valid = 'N'
            if info[1] in tags:
                valid = 'Y'
            if len(info) > 2:
                if info[2] == 'INDI' or info[2] == 'FAM':
                    if info[2] == 'INDI':
                        if first_indi:
                            dic = {}
                            first_indi = False
                        else:
                            mycol.insert_one(dic)
                        dic = {}
                        dic["id"] = info[1]
                    else:
                        if first_fam:
                            mycol.insert_one(dic)
                            dic = {}
                            first_fam = False
                        else:
                            mycol2.insert_one(dic)
                        dic = {}
                        dic["id"] = info[1]
                    valid = 'Y'
                    # print("<-- " + info[0] + "|" + info[1] + "|" + valid + "|" + info[2])
                    res.append("<-- " + info[0] + "|" +
                               info[1] + "|" + valid + "|" + info[2])
                else:
                    # print("<-- " + info[0] + "|" + info[1] + "|" + valid + "|" + info[2])
                    res.append("<-- " + info[0] + "|" +
                               info[1] + "|" + valid + "|" + info[2])
                    if birthDate:
                        dic["BIRTHDATE"] = info[2]
                        birthDate = False
                    elif deathDate:
                        dic["DEATHDATE"] = info[2]
                        deathDate = False
                    elif divDate:
                        dic["DIVDATE"] = info[2]
                        divDate = False
                    elif info[1] == "DEAT":
                        deathDate = True
                    else:
                        dic[info[1]] = info[2]
            else:
                if info[1] == 'TRLR':
                    mycol2.insert_one(dic)
                elif info[1] == "BIRT":
                    birthDate = True
                elif info[1] == "DIV":
                    divDate = True
                # print("<-- " + info[0] + "|" + info[1] + "|" + valid)
                res.append("<-- " + info[0] + "|" + info[1] + "|" + valid)
    return res


def printIndividuals(mydb):
    ret = []
    mycol = mydb["Individuals"]
    x = PrettyTable()
    x.field_names = ["ID", "Name", "Gender", "Birthday",
                     "Age", "Dead", "Death", "Child", "Spouse"]
    # print("Individuals")
    ret.append("Individuals")
    cursor = mycol.find({})
    for doc in cursor:
        if "DEATHDATE" in doc:
            dead = "Y"
            date = doc["DEATHDATE"]
            year = int(doc["BIRTHDATE"][-4:])
            age = int(doc["DEATHDATE"][-4:]) - year
        else:
            year = int(doc["BIRTHDATE"][-4:])
            age = 2023 - year
            dead = "N"
            date = "N/A"
        if "FAMS" in doc:
            spouse = doc["FAMS"]
        else:
            spouse = "N/A"
        if "FAMC" in doc:
            children = doc["FAMC"]
        else:
            children = "N/A"
        x.add_row([doc["id"], doc["NAME"], doc["SEX"],
                  doc["BIRTHDATE"], age, dead, date, children, spouse])
    # print(x)
    ret.append(x)
    return ret


def printFamilies(mydb):
    ret = []
    mycol2 = mydb["Families"]
    y = PrettyTable()
    y.field_names = ["ID", "Married", "Divorced",
                     "Husband ID", "Wif ID", "Children"]
    # print("Families")
    ret.append("Families")
    cursor2 = mycol2.find({})
    for doc in cursor2:
        if "DIVDATE" in doc:
            div = doc["DIVDATE"]
        else:
            div = "N/A"
        if "CHIL" in doc:
            child = doc["CHIL"]
        else:
            child = "N/A"
        if "HUSB" in doc:
            husb = doc["HUSB"]
        else:
            husb = "N/A"
        if "WIFE" in doc:
            wife = doc["WIFE"]
        else:
            wife = "N/A"
        if "DATE" in doc:
            date = doc["DATE"]
        else:
            date = "N/A"
        y.add_row([doc["id"], date, div, husb, wife, child])
    # print(y)
    ret.append(y)
    return ret

def checkDatesBeforeCurrent(mydb):
    ret = []
    mycol = mydb["Individuals"]
    cursor = mycol.find({})
    currtime = datetime.now()
    for doc in cursor:
        if 'DEATHDATE' in doc:
            deathDate = doc['DEATHDATE']
            deathDate_object = datetime.strptime(deathDate, '%d %b %Y').date()
            if deathDate_object > currtime:
                ret.append("Error " + doc["id"] + ": Death date of " + doc["NAME"] +
                  " occurs after the current date.")
        if 'BIRTHDATE' in doc:
            birthDate = doc['BIRTHDATE']
            birthDate_object = datetime.strptime(
                birthDate, '%d %b %Y').date()
            if birthDate_object > currtime:
                ret.append("Error " + doc["id"] + ": Birth date of " + doc["NAME"] +
                               " occurs after the current date.")
        if 'DATE' in doc:
            marriageDate = doc['DATE']
            marriageDate_object = datetime.strptime(marriageDate, '%d %b %Y').date()
            if marriageDate_object > currtime:
                ret.append("Error " + doc["id"] + ": Marriage date of " + doc["NAME"] +
                               " occurs after the current date.")
        if 'DIVDATE' in doc:
            divDate = doc["DIVDATE"]
            divDate_object = datetime.strptime(divDate, '%d %b %Y').date()
            if divDate_object > currtime:
                ret.append("Error " + doc["id"] + ": Divorce date of " + doc["NAME"] +
                               " occurs after the current date.")
    return ret


def checkBirthBeforeMarriage(mydb):
    ret = []
    mycol = mydb["Individuals"]
    cursor = mycol.find({})
    for doc in cursor:
        if 'DATE' in doc:
            marriageDate = doc['DATE']
            marriageDate_object = datetime.strptime(marriageDate, '%d %b %Y').date()
            if 'BIRTHDATE' in doc:
                birthDate = doc['BIRTHDATE']
                birthDate_object = datetime.strptime(
                    birthDate, '%d %b %Y').date()
                if birthDate_object > marriageDate_object:
                    ret.append("Error " + doc["id"] + ": Birth date of " + doc["NAME"] +
                               " occurs after their marriage date.")
            else:
                ret.append("Error " + doc["id"] + ": " + doc["NAME"] +
                           " cannot have their marriage date before being born")
    return ret

# Checks Birth Before Death
def checkBirthBeforeDeath(mydb):
    ret = []
    mycol = mydb["Individuals"]
    cursor = mycol.find({})
    for doc in cursor:
        if 'DEATHDATE' in doc:
            deathDate = doc['DEATHDATE']
            deathDate_object = datetime.strptime(deathDate, '%d %b %Y').date()
            if 'BIRTHDATE' in doc:
                birthDate = doc['BIRTHDATE']
                birthDate_object = datetime.strptime(
                    birthDate, '%d %b %Y').date()
                if birthDate_object > deathDate_object:
                    ret.append("Error " + doc["id"] + ": Birth date of " + doc["NAME"] +
                               " occurs after their death date.")
            else:
                ret.append("Error " + doc["id"] + ": " + doc["NAME"] +
                           " cannot have their death date before being born")
    return ret


# Checks Marriage Before Divorce
def checkMarriageBeforeDivorce(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor2 = mycol2.find({})
    for doc in cursor2:
        if "DATE" in doc:
            marDate = doc["DATE"]
            marDate_object = datetime.strptime(marDate, '%d %b %Y').date()
            husb = doc["HUSB"]
            wife = doc["WIFE"]
            husbDoc = mycol.find_one({'id': husb})
            wifeDoc = mycol.find_one({'id': wife})
            if "DIVDATE" in doc:
                divDate = doc["DIVDATE"]
                divDate_object = datetime.strptime(divDate, '%d %b %Y').date()
                if marDate_object > divDate_object:
                    ret.append("Error " + doc["id"] + ": Marriage date of " + wifeDoc["NAME"] +
                               " and " + husbDoc["NAME"] + " occurs after their divorce date.")
        if "DATE" not in doc and "DIVDATE" in doc:
            husb = doc["HUSB"]
            wife = doc["WIFE"]
            husbDoc = mycol.find_one({'id': husb})
            wifeDoc = mycol.find_one({'id': wife})
            ret.append("Error " + doc["id"] + ": Divorce of " + wifeDoc["NAME"] +
                       " and " + husbDoc["NAME"] + " cannot occur before marriage")
    return ret


# check Marriage before death
def checkMarriageBeforeDeath(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor2 = mycol2.find({})
    for doc in cursor2:
        if "DATE" in doc:
            marDate = doc["DATE"]
            marDate_object = datetime.strptime(marDate, '%d %b %Y').date()
            husb = doc["HUSB"]
            wife = doc["WIFE"]
            hubDoc = mycol.find_one({'id': husb})
            wifeDoc = mycol.find_one({'id': wife})
            if 'DEATHDATE' in hubDoc:
                hubdied = hubDoc['DEATHDATE']
                hubdied_object = datetime.strptime(hubdied, '%d %b %Y').date()
                if marDate_object > hubdied_object:
                    # print("Error " +  doc["id"] + ":Marriage date of " + hubDoc["NAME"] + " (" + hubDoc["id"] +") occurs after his death date.")
                    ret.append("Error " + doc["id"] + ":Marriage date of " + hubDoc["NAME"] +
                               " (" + hubDoc["id"] + ") occurs after his death date.")
            if 'DEATHDATE' in wifeDoc:
                wifdied = wifeDoc['DEATHDATE']
                wifdied_object = datetime.strptime(wifdied, '%d %b %Y').date()
                if marDate_object > wifdied_object:
                    # print("Error " +  doc["id"] + ":Marriage date of " + wifeDoc["NAME"] + " (" + wifeDoc["id"] +") occurs after her death date.")
                    ret.append("Error " + doc["id"] + ":Marriage date of " + wifeDoc["NAME"] +
                               " (" + wifeDoc["id"] + ") occurs after her death date.")
    return ret


# check Divorce before death
def checkDivorceBeforeDeath(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor2 = mycol2.find({})
    for doc in cursor2:
        if "DIVDATE" in doc:
            divDate = doc["DIVDATE"]
            divDate_object = datetime.strptime(divDate, '%d %b %Y').date()
            husb = doc["HUSB"]
            wife = doc["WIFE"]
            hubDoc = mycol.find_one({'id': husb})
            wifeDoc = mycol.find_one({'id': wife})
            if 'DEATHDATE' in hubDoc:
                hubdied = hubDoc['DEATHDATE']
                hubdied_object = datetime.strptime(hubdied, '%d %b %Y').date()
                if divDate_object > hubdied_object:
                    # print("Error " +  doc["id"] + ":Divorce date of " + hubDoc["NAME"] + " (" + hubDoc["id"] +") occurs after his death date.")
                    ret.append("Error " + doc["id"] + ":Divorce date of " + hubDoc["NAME"] +
                               " (" + hubDoc["id"] + ") occurs after his death date.")
            if 'DEATHDATE' in wifeDoc:
                wifdied = wifeDoc['DEATHDATE']
                wifdied_object = datetime.strptime(wifdied, '%d %b %Y').date()
                if divDate_object > wifdied_object:
                    # print("Error " +  doc["id"] + ":Divorce date of " + wifeDoc["NAME"] + " (" + wifeDoc["id"] +") occurs after her death date.")
                    ret.append("Error " + doc["id"] + ":Divorce date of " + wifeDoc["NAME"] +
                               " (" + wifeDoc["id"] + ") occurs after her death date.")
    return 

#checks if individual lived over 150 years
def checkOver150(mydb):
    ret = []
    mycol = mydb["Individuals"]
    cursor = mycol.find({})
    for doc in cursor:
        birthTime = datetime.strptime(doc["BIRTHDATE"], '%d %b %Y').date()
        if "DEATHDATE" in doc:
            deathTime = datetime.strptime(doc["DEATHDATE"], '%d %b %Y').date()
            delta = relativedelta(birthTime, deathTime)
            if (abs(delta.years) >= 150 ):
                ret.append("Anomaly " +doc["FAMS"]+ ": Death date of " + doc["NAME"] + doc["id"] +" occurs  150 (or more) years after their birth date")
        else:
            today = datetime.today()
            delta = relativedelta(birthTime, today)
            if (abs(delta.years) >= 150 ):
                ret.append("Anomaly " +doc["FAMS"]+ ": "+doc["NAME"] + doc["id"] +" has been alive for 150 (or more) years")
    print(ret)
    return ret

#checks if child was born when not married
def checkBirthBeforeMarriageAfterDivorce(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol.find({})
    for doc in cursor:
        if "FAMC" in doc:
            childBirth = datetime.strptime(doc["BIRTHDATE"], '%d %b %Y').date()
            famDoc = mycol2.find_one({'id': doc["FAMC"]})
            if "DATE" in famDoc:
                marriageDate = datetime.strptime(famDoc["DATE"], '%d %b %Y').date()
                if marriageDate > childBirth:
                    ret.append("Anomaly " +doc["FAMC"]+ ": "+doc["NAME"] + doc["id"] +" was born before the marriage of marriage of their parents")
                if "DIVDATE" in famDoc:
                    divorceDate = datetime.strptime(famDoc["DIVDATE"], '%d %b %Y').date()
                    delta = relativedelta(childBirth, divorceDate)
                    if (abs(delta.months) >= 9):
                        ret.append("Anomaly " +doc["FAMC"]+ ": "+doc["NAME"] + doc["id"] +" was born 9 months after the divorce of his parents")
    print(ret)
    return ret

for x in readGEDCOM('Christian_Huang_Tree.ged', mydb):
    print(x)
for x in printIndividuals(mydb):
    print(x)
for x in printFamilies(mydb):
    print(x)