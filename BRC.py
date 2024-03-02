import numpy;
import time;

lines = []

compare = "]"
city = {"name": "none", "min": 0.0 ,"max": 0.0, "mean": 0.0, "count": 0.0, "total": 0.0}
earth = []
count = 0
countlines = 0


earth.append(city)

def GroupByStation(string):
    global compare, city, earth, count, countlines
    stringsplit = string.split(";")
    if any(d.get("name") == stringsplit[0] for d in earth) == False:
            earth.append({"name": "none", "min": 99999.0 ,"max": 0.0, "mean": 0.0, "count": 1.0, "total": 0.0,})
            earth[count]["name"] = stringsplit[0]
            earth[count]["min"] = float(stringsplit[1])
            earth[count]["max"] = float(stringsplit[1])
            earth[count]["mean"] = float(stringsplit[1])
            earth[count]["total"] = float(stringsplit[1])
            count = count + 1
    else:
        ContainedName =  [d for d in earth if stringsplit[0] in d.get("name", "")]

        ContainedName[0]["count"] = float(ContainedName[0]["count"]) + 1

        ContainedName[0]["total"] = float(ContainedName[0]["total"]) + float(stringsplit[1])
        if ContainedName[0]["max"] < float(stringsplit[1]):
            ContainedName[0]["max"] = float(stringsplit[1])

        if ContainedName[0]["min"] > float(stringsplit[1]):
            ContainedName[0]["min"] = float(stringsplit[1])


    countlines = countlines + 1
    return earth


with open("measurements.txt", "r") as file:
    for line in file:
        lines.append(line)

for linenum in lines:
    GroupByStation(linenum)


for i in range(0, len(earth)):
    print(earth[i]["total"], earth[i]["count"])
    earth[i]["mean"] = earth[i]["total"] / earth[i]["count"]

sorted_cities = sorted(earth, key=lambda x: x['name'])

for i in range(0, len(earth)):
    print(f"{sorted_cities[i].get('name')}={sorted_cities[i].get('min')}/{round(sorted_cities[i].get('mean'), 1)}/{sorted_cities[i].get('max')}", end=", ")
        