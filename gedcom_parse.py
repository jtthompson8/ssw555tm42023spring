from prettytable import PrettyTable
from datetime import datetime
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["db"]
mycol = mydb["Individuals"]
mycol2 = mydb["Families"]

tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
        'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

dic = {}
first_indi = True
famDic = {}
first_fam = True
birthDate = False
deathDate = False
x = PrettyTable()
y = PrettyTable()
x.field_names = ["ID", "Name", "Gender", "Birthday",
                 "Age", "Alive", "Death", "Child", "Spouse"]
y.field_names = ["ID", "Married", "Divorced",
                 "Husband ID", "Wif ID", "Children"]

with open('Christian_Huang_Tree.ged', 'r') as ged:
    for line in ged:
        info = line.strip().split(' ', 2)
        # lvl, tag, args
        print("--> " + line.strip())
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
                print("<-- " + info[0] + "|" + info[1] +
                      "|" + valid + "|" + info[2])
            else:
                print("<-- " + info[0] + "|" + info[1] +
                      "|" + valid + "|" + info[2])
                if birthDate:
                    dic["BIRTHDATE"] = info[2]
                    birthDate = False
                elif deathDate:
                    dic["DEATHDATE"] = info[2]
                    deathDate = False
                elif info[1] == "DEAT":
                    deathDate = True
                else:
                    dic[info[1]] = info[2]
        else:
            if info[1] == 'TRLR':
                mycol2.insert_one(dic)
            elif info[1] == "BIRT":
                birthDate = True
            print("<-- " + info[0] + "|" + info[1] + "|" + valid)

print("Individuals")
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
print(x)

print("Families")
cursor2 = mycol2.find({})
for doc in cursor2:
    if doc["_CURRENT"] == "N":
        div = "N/A"
    else:
        div = "Y"
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
print(y)

# User Story #3


def birth_before_death(individual_id):
    individual = mycol.find_one({"id": individual_id})
    if "BIRTHDATE" in individual and "DEATHDATE" in individual:
        birth_date = datetime.strptime(individual["BIRTHDATE"], "%d %b %Y")
        death_date = datetime.strptime(individual["DEATHDATE"], "%d %b %Y")
        return birth_date < death_date
    else:
        return False

# User Story
