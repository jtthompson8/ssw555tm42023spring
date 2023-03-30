from prettytable import PrettyTable
import pymongo
from datetime import datetime
import calendar
from datetime import datetime, timedelta
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
                    elif info[1] == "CHIL":
                        if "CHIL" in dic:
                            dic[info[1]].append(info[2])
                        else:
                            dic["CHIL"] = [info[2]]
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
    currtime = datetime.now().date()
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
            marriageDate_object = datetime.strptime(
                marriageDate, '%d %b %Y').date()
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

# Checks Birth Before Marriage


def checkBirthBeforeMarriage(mydb):
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
            if 'BIRTHDATE' in hubDoc:
                hubborn = hubDoc['BIRTHDATE']
                hubborn_object = datetime.strptime(hubborn, '%d %b %Y').date()
                if marDate_object < hubborn_object:
                    # print("Error " +  doc["id"] + ":Marriage date of " + hubDoc["NAME"] + " (" + hubDoc["id"] +") occurs before his birth date.")
                    ret.append("Error " + doc["id"] + ":Marriage date of " + hubDoc["NAME"] +
                               " (" + hubDoc["id"] + ") occurs before his birth.")
            if 'BIRTHDATE' in wifeDoc:
                wifborn = wifeDoc['BIRTHDATE']
                wifborn_object = datetime.strptime(wifborn, '%d %b %Y').date()
                if marDate_object < wifborn_object:
                    # print("Error " +  doc["id"] + ":Marriage date of " + wifeDoc["NAME"] + " (" + wifeDoc["id"] +") occurs before her birth date.")
                    ret.append("Error " + doc["id"] + ":Marriage date of " + wifeDoc["NAME"] +
                               " (" + wifeDoc["id"] + ") occurs before her birth.")
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
                    ret.append("Error " + doc["FAMS"] + ": Birth date of " + doc["NAME"] + doc["id"] +
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
    return ret

# checks if individual lived over 150 years


def checkOver150(mydb):
    ret = []
    mycol = mydb["Individuals"]
    cursor = mycol.find({})
    for doc in cursor:
        birthTime = datetime.strptime(doc["BIRTHDATE"], '%d %b %Y').date()
        if "DEATHDATE" in doc:
            deathTime = datetime.strptime(doc["DEATHDATE"], '%d %b %Y').date()
            delta = relativedelta(birthTime, deathTime)
            if (abs(delta.years) >= 150):
                ret.append("Anomaly " + doc["FAMS"] + ": Death date of " + doc["NAME"] +
                           doc["id"] + " occurs  150 (or more) years after their birth date")
        else:
            today = datetime.today()
            delta = relativedelta(birthTime, today)
            if (abs(delta.years) >= 150):
                ret.append("Anomaly " + doc["FAMS"] + ": "+doc["NAME"] +
                           doc["id"] + " has been alive for 150 (or more) years")
    return ret

# checks if child was born when not married


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
                marriageDate = datetime.strptime(
                    famDoc["DATE"], '%d %b %Y').date()
                if marriageDate > childBirth:
                    ret.append("Anomaly " + doc["FAMC"] + ": "+doc["NAME"] + doc["id"] +
                               " was born before the marriage of marriage of their parents")
                if "DIVDATE" in famDoc:
                    divorceDate = datetime.strptime(
                        famDoc["DIVDATE"], '%d %b %Y').date()
                    delta = relativedelta(childBirth, divorceDate)
                    if (abs(delta.months) >= 9):
                        ret.append("Anomaly " + doc["FAMC"] + ": "+doc["NAME"] +
                                   doc["id"] + " was born 9 months after the divorce of his parents")
    return ret
# checks if chilld was born before death of parents


def checkBirthBeforeDeathOfParents(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol.find({})
    for doc in cursor:
        if "FAMC" in doc:
            childBirth = datetime.strptime(doc["BIRTHDATE"], '%d %b %Y').date()
            famDoc = mycol2.find_one({'id': doc["FAMC"]})
            if "HUSB" in famDoc:
                husb = famDoc["HUSB"]
                wife = famDoc["WIFE"]
                hubDoc = mycol.find_one({'id': husb})
                wifeDoc = mycol.find_one({'id': wife})
                if 'DEATHDATE' in hubDoc:
                    hubdied = hubDoc['DEATHDATE']
                    hubdied_object = datetime.strptime(
                        hubdied, '%d %b %Y').date()
                    if childBirth > hubdied_object:
                        ret.append("Error " + doc["id"] + ": Death of " + hubDoc["NAME"] +
                                   " occurs at least 9 months before his child is born.")
                if 'DEATHDATE' in wifeDoc:
                    wifdied = wifeDoc['DEATHDATE']
                    wifdied_object = datetime.strptime(
                        wifdied, '%d %b %Y').date()
                    if childBirth > wifdied_object:
                        ret.append("Error " + doc["id"] + ": Death of " + wifeDoc["NAME"] +
                                   wifeDoc["id"] + " occurs before her child was born.")
    return ret

# checks if Marriage is after both husband and wife are 14 or older


def checkMarriageAfterFourteen(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol2.find({})
    for doc in cursor:
        if "DATE" in doc:
            marriageDate = datetime.strptime(doc["DATE"], '%d %b %Y').date()
            husb = doc["HUSB"]
            wife = doc["WIFE"]
            hubDoc = mycol.find_one({'id': husb})
            wifeDoc = mycol.find_one({'id': wife})
            if 'BIRTHDATE' in hubDoc:
                hubBorn = hubDoc['BIRTHDATE']
                hubBorn_obj = datetime.strptime(hubBorn, '%d %b %Y').date()
                delta = relativedelta(hubBorn_obj, marriageDate)
                if (abs(delta.years) <= 14):
                    ret.append(
                        "Error " + doc["id"] + ": " + hubDoc["NAME"] + " married before turning 14")
            if 'BIRTHDATE' in wifeDoc:
                wifeBorn = wifeDoc['BIRTHDATE']
                wifeBorn_obj = datetime.strptime(wifeBorn, '%d %b %Y').date()
                delta = relativedelta(wifeBorn_obj, marriageDate)
                if (abs(delta.years) <= 14):
                    ret.append(
                        "Error " + doc["id"] + ": " + hubDoc["NAME"] + " married before turning 14")
    return ret

 # checks that no more than five siblings are born at the same time


def checkSiblingsBornSame(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol2.find({})
    for doc in cursor:
        dic = {}
        if "CHIL" in doc:
            for chil in doc["CHIL"]:
                indDoc = mycol.find_one({'id': chil})
                if indDoc["BIRTHDATE"] not in dic:
                    dic[indDoc["BIRTHDATE"]] = 1
                else:
                    dic[indDoc["BIRTHDATE"]] = dic[indDoc["BIRTHDATE"]] + 1
        for x, y in dic.items():
            if y > 5:
                ret.append("Anomaly " + "in " + doc["id"] + " there are " + str(
                    y) + " children with the birthday of " + str(x))
    return ret

# checks that birth dates of siblings are more than 8 months (243 days) apart or less than 2 days apart


def checkSiblingSpacing(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol2.find({})
    for doc in cursor:
        dic = {}
        if "CHIL" in doc:
            for chil in doc["CHIL"]:
                indDoc = mycol.find_one({'id': chil})
                for x, y in dic.items():
                    if (abs(y - datetime.strptime(indDoc["BIRTHDATE"], '%d %b %Y').date()) <= timedelta(days=243) and abs(y - datetime.strptime(indDoc["BIRTHDATE"], '%d %b %Y').date()) > timedelta(days=2)):
                        ret.append("Anomaly in " + doc["id"] + " child " + x + " and child " + indDoc["id"] + " have birthdays within " + str(
                            abs(y - datetime.strptime(indDoc["BIRTHDATE"], '%d %b %Y').date()).days) + " days")
                dic[indDoc["id"]] = datetime.strptime(
                    indDoc["BIRTHDATE"], '%d %b %Y').date()
    return ret
# checks that marriage should not occur during marriage to another spouse


def noBigamy(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol.find({})
    cursor2 = mycol2.find({})

    for doc in cursor2:
        if "DATE" in doc:
            husb = doc["HUSB"]
            wife = doc["WIFE"]
            hubDoc = mycol.find_one({'id': husb})
            wifeDoc = mycol.find_one({'id': wife})
            if "DIVDATE" not in doc:
                if len(hubDoc["FAMS"]) > 1:
                    ret.append("Error " + doc["id"] + ": " + hubDoc["NAME"] +
                               " may not get married while already married")
                if len(wifeDoc["FAMS"]) > 1:
                    ret.append("Error " + doc["id"] + ": " + wifeDoc["NAME"] +
                               " may not get married while already married")


def checkParentsAge(mydb):
    ret = []
    hubborn_object = None
    wifborn_object = None
    chilborn_object = None
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol2.find({})
    for doc in cursor:
        if "DATE" in doc:
            husb = doc["HUSB"]
            wife = doc["WIFE"]
            child = doc["CHIL"]
            hubDoc = mycol.find_one({'id': husb})
            wifeDoc = mycol.find_one({'id': wife})
            chilDoc = mycol.find_one({'id': child})
            if 'BIRTHDATE' in hubDoc:
                hubborn = hubDoc["BIRHTDATE"]
                hubborn_object = datetime.strptime(hubborn, '%d %b %Y').date()
            if 'BIRTHDATE' in wifeDoc:
                wifborn = hubDoc["BIRHTDATE"]
                wifborn_object = datetime.strptime(wifborn, '%d %b %Y').date()
            if 'BIRTHDATE' in chilDoc:
                chilborn = chilDoc["BIRHTDATE"]
                chilborn_object = datetime.strptime(
                    chilborn, '%d %b %Y').date()
            hub_chil_age_diff = relativedelta(
                chilborn_object, hubborn_object).years
            wif_age_diff = relativedelta(chilborn_object, wifborn_object).years
            if hub_chil_age_diff > 80:
                ret.append("Error " + doc["id"] + ": Husband " +
                           hubDoc["NAME"] + " More than 80 years older than child")
            if wif_age_diff > 60:
                ret.append("Error " + doc["id"] + ": Husband " +
                           wifeDoc["NAME"] + " More than 60 years older than child")


def checkFifteenSiblings(mydb):
    ret = []
    mycol = mydb["Families"]
    cursor = mycol.find({})
    for doc in cursor:
        if "CHIL" in doc:
            if len(doc["CHIL"]) >= 15:
                ret.append("Anomaly "+doc["id"]+": Family has 15 or more siblings")
    return(ret)


def checkMaleLastNames(mydb):
    ret = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]
    cursor = mycol.find({})
    for doc in cursor:
        if "FAMC" in doc:
            famDoc = mycol2.find_one({'id': doc["FAMC"]})
            try:
                fatherDoc = mycol.find_one({'id': famDoc["HUSB"]})
            except:
                continue
            if (fatherDoc["SURN"] != doc["SURN"]):
                ret.append("Error "+doc["FAMC"]+": "+doc["NAME"] +" "+ doc["id"] + " has a different last name than his father "+fatherDoc["NAME"] +" "+ fatherDoc["id"] +". All male members of a family should have the same last name.")
    return ret 


# readGEDCOM('Christian_Huang_Tree.ged', mydb)
