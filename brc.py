import numpy;
import time;
import multiprocessing

def filelinecount():
  with open("measurements.txt", 'r') as file:
          counted = 0
          for line in file:
              counted += 1
          return counted

n = filelinecount() 

numthreads = 1

nmin = 0
n = n / numthreads
nconst = n

threads = []
threadstartline = [0,50000000]

chunks = {"name": "0", "startnum": 0, "endnum": 2, "content": []}

chunkslist = []

count = 0

chunkslistcount = [{"content": []}]

MassiveChunk = [{"content": []}]

chunkslist.append({"name": "none", "min": 99999.0 ,"max": 0.0, "mean": 0.0, "count": 1.0, "total": 0.0,})





def GroupByStation(strings):
    global compare, city, earth, countlines, count, chunkslist
    for i in range(len(strings)):
      stringsplit = strings[i].split(";")
      if any(d.get("name") == stringsplit[0] for d in chunkslist) == False:
        chunkslist.append({"name": "none", "min": 99999.0 ,"max": 0.0, "mean": 0.0, "count": 1.0, "total": 0.0,})
        #print(len(chunkslist))
        chunkslist[count]["name"] = stringsplit[0]
        chunkslist[count]["min"] = float(stringsplit[1])
        chunkslist[count]["max"] = float(stringsplit[1])
        chunkslist[count]["mean"] = float(stringsplit[1])
        chunkslist[count]["total"] = float(stringsplit[1])
        chunkslist[count]["count"] = 1.0
        #print(len(chunkslist))
        count = count + 1
      else:
          ContainedName =  [d for d in chunkslist if stringsplit[0] in d.get("name", "")]


          ContainedName[0]["count"] = float(ContainedName[0]["count"]) + 1.0

          ContainedName[0]["total"] = float(ContainedName[0]["total"]) + float(stringsplit[1])
          if ContainedName[0]["max"] < float(stringsplit[1]):
              ContainedName[0]["max"] = float(stringsplit[1])

          if ContainedName[0]["min"] > float(stringsplit[1]):
              ContainedName[0]["min"] = float(stringsplit[1])


      countlines = countlines + 1
    print(len(chunkslist))

lines = []

compare = "]"
city = {"name": "none", "min": 0.0 ,"max": 0.0, "mean": 0.0, "count": 0.0, "total": 0.0}
earth = []
count = 0
countlines = 0

print("starting")


print("reading file")


with open("measurements.txt", "r") as file:
    for line in file:
        lines.append(line)

processes = []

print("starting threads")

for i in range(numthreads):
  MassiveChunk.append({"content": []})
  MassiveChunk[i]["content"] = lines[int(nmin):int(n)]
  n = n + nconst
  nmin = nmin + nconst
  p = multiprocessing.Process(target=GroupByStation, args=(MassiveChunk[i]["content"],))
  processes.append(p)
  p.start()




for p in processes:
  p.join()

print(len(chunkslist))

print("finding mean")

for i in range(1):
  print(len(chunkslist))

'''for i in range(0, len(MassiveChunk)):
    chunkslist[i]["mean"] = chunkslist[i]["total"] / chunkslist[i]["count"]

sorted_cities = sorted(chunkslist, key=lambda x: x['name'])

print("printing all")

for i in range(0, len(chunkslist)):
    print(f"{sorted_cities[i].get('name')}={sorted_cities[i].get('min')}/{(round(sorted_cities[i].get('mean'),1))}/{sorted_cities[i].get('max')}", end=", ")
#print("\n\n", len(chunkslist), "new cities out of", countlines, "lines. \nThe city name of city 0 is", chunkslist[0]["name"] )
#print("\n\n", len(chunkslist), "new cities out of", countlines, "lines. \nThe city name of city 1 is", chunkslist[1]["name"] )

print(len(MassiveChunk[0]))'''
        
