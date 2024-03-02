import multiprocessing
from multiprocessing import Process, Manager, Pool







def GroupByStation(Chunk):
    local_dict = {}
    for i in range(len(Chunk)):
      name, value = Chunk[i].strip().split(";")
      value = float(value)
      if name not in local_dict:
        local_dict[name] = {"min": value, "max": value, "total": value, "count": 1}
      else:
          ContainedName =  local_dict[name]


          local_dict[name]["count"] = float(local_dict[name]["count"]) + 1.0

          local_dict[name]["total"] = float(local_dict[name]["total"]) + float(value)
          if local_dict[name]["max"] < float(value):
              local_dict[name]["max"] = float(value)

          if local_dict[name]["min"] > float(value):
              local_dict[name]["min"] = float(value)
    return local_dict


if __name__ == '__main__':
  numprocesses = 8
  lines = open("measurements.txt", "r").readlines()
  chunk_size = len(lines) // numprocesses
  chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

  with Pool(processes=numprocesses) as pool:
    results = pool.map(GroupByStation, chunks)


  print("{", end = "")
  final_results = {}

  for local_dict in results:
    for name, stats in local_dict.items():
      if name not in final_results:
        final_results[name] = stats
      else:
        final_results[name]["min"] = min(final_results[name]["min"], stats["min"])
        final_results[name]["max"] = max(final_results[name]["max"], stats["max"])
        final_results[name]["total"] += stats["total"]
        final_results[name]["count"] += stats["count"]

  for name, stats in sorted(final_results.items(), key = lambda item: item[0]):
    mean = round(stats["total"] / stats["count"], 1)
    print(f"{name}={stats['min']}/{mean}/{stats['max']}", end = ", ")
  print("}", end = "")

