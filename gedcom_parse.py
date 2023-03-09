from prettytable import PrettyTable
import pymongo
from datetime import datetime
import calendar



myclient = pymongo.MongoClient("mongodb+srv://Christian:6TYXxCt9Sp9GDO20@cluster0.iilq4vg.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["db"]


def readGEDCOM(file, mydb):
    res = []
    mycol = mydb["Individuals"]
    mycol2 = mydb["Families"]

    tags = ['INDI','NAME','SEX','BIRT','DEAT','FAMC','FAMS','FAM','MARR','HUSB','WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE']

    dic = {}
    first_indi = True
    famDic = {}
    first_fam = True
    birthDate = False
    deathDate = False
    divDate = False
    with open(file, 'r') as ged:
        for line in ged:
            info = line.strip().split(' ', 2)
            # print(info)
            res.append(info)
            #lvl, tag, args
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
                    res.append("<-- " + info[0] + "|" + info[1] + "|" + valid + "|" + info[2])
                else:
                    # print("<-- " + info[0] + "|" + info[1] + "|" + valid + "|" + info[2])
                    res.append("<-- " + info[0] + "|" + info[1] + "|" + valid + "|" + info[2])
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
    x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Dead", "Death", "Child", "Spouse"]
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
        x.add_row([doc["id"], doc["NAME"], doc["SEX"], doc["BIRTHDATE"], age, dead, date, children, spouse])  
    # print(x)
    ret.append(x)
    return ret

def printFamilies(mydb):
    ret = []
    mycol2 = mydb["Families"]
    y = PrettyTable()
    y.field_names = ["ID", "Married", "Divorced", "Husband ID", "Wif ID", "Children"]
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
            hubDoc = mycol.find_one({'id' : husb})
            wifeDoc = mycol.find_one({'id' : wife})
            if 'DEATHDATE' in hubDoc:
                hubdied = hubDoc['DEATHDATE']
                hubdied_object = datetime.strptime(hubdied, '%d %b %Y').date()
                if marDate_object > hubdied_object:
                    # print("Error " +  doc["id"] + ":Marriage date of " + hubDoc["NAME"] + " (" + hubDoc["id"] +") occurs after his death date.")
                    ret.append("Error " +  doc["id"] + ":Marriage date of " + hubDoc["NAME"] + " (" + hubDoc["id"] +") occurs after his death date.")
            if 'DEATHDATE' in wifeDoc:
                wifdied = wifeDoc['DEATHDATE']
                wifdied_object = datetime.strptime(wifdied, '%d %b %Y').date()
                if marDate_object > wifdied_object:
                    # print("Error " +  doc["id"] + ":Marriage date of " + wifeDoc["NAME"] + " (" + wifeDoc["id"] +") occurs after her death date.")
                    ret.append("Error " +  doc["id"] + ":Marriage date of " + wifeDoc["NAME"] + " (" + wifeDoc["id"] +") occurs after her death date.")
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
            hubDoc = mycol.find_one({'id' : husb})
            wifeDoc = mycol.find_one({'id' : wife})
            if 'DEATHDATE' in hubDoc:
                hubdied = hubDoc['DEATHDATE']
                hubdied_object = datetime.strptime(hubdied, '%d %b %Y').date()
                if divDate_object > hubdied_object:
                    # print("Error " +  doc["id"] + ":Divorce date of " + hubDoc["NAME"] + " (" + hubDoc["id"] +") occurs after his death date.")
                    ret.append("Error " +  doc["id"] + ":Divorce date of " + hubDoc["NAME"] + " (" + hubDoc["id"] +") occurs after his death date.")
            if 'DEATHDATE' in wifeDoc:
                wifdied = wifeDoc['DEATHDATE']
                wifdied_object = datetime.strptime(wifdied, '%d %b %Y').date()
                if divDate_object > wifdied_object:
                    # print("Error " +  doc["id"] + ":Divorce date of " + wifeDoc["NAME"] + " (" + wifeDoc["id"] +") occurs after her death date.")
                    ret.append("Error " +  doc["id"] + ":Divorce date of " + wifeDoc["NAME"] + " (" + wifeDoc["id"] +") occurs after her death date.")
    return ret
                    
# for x in readGEDCOM('Christian_Huang_Tree.ged', mydb):
#     print(x)
# for x in printIndividuals(mydb):
#     print(x)
# for x in printFamilies(mydb):
#     print(x)
# for x in checkMarriageBeforeDeath(mydb):
#     print(x)
# for x in checkDivorceBeforeDeath(mydb):
#     print(x)