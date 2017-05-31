import json
import csv

def cal(pp1, pp2, pp3):
  p1 = [pp1[0]/2, pp1[1]]
  p2 = [pp2[0]/2, pp2[1]]
  p3 = [pp3[0]/2, pp3[1]]

  x1 = p1[0]
  y1 = p1[1]
  x2 = p2[0]
  y2 = p2[1]
  x3 = p3[0]
  y3 = p3[1]

  t = -((x2 - x3)*(y2 - y1) + (y3 - y2)*(x2 - x1)) / ((y2 - y1) ** 2 + (x2 - x1) ** 2)

  p = [x3 + (y1 - y2) * t, y3 + (x2 - x1) * t]

  return (((y1 - y2) * t) ** 2 + ((x2 - x1) * t) ** 2) ** 0.5,\
         (p[0] - p2[0]) * (p[0] - p1[0]) < 0 and (p[1] - p2[1]) * (p[1] - p1[1]) < 0

if __name__ == '__main__':
  with open('boundary-ward.geojson') as file:
    feature = json.load(file)['features']

  distMap = {}
  outputfile = 'crime-w.csv'

  distance = [0.001, 0.0005, 0.0001, 0.00005]
  boundTitle = list(map(lambda x: 'bound-%.5f' % x, distance))

  for f in feature:
    distMap[f['properties']['ward']] = f['geometry']['coordinates']

  with open('crime.csv') as csvfile:
    r = csv.reader(csvfile)
    for row in r:
      if row[12] == 'Ward': # 11 District 12 Ward
        with open(outputfile, 'a') as csv_file:
          w = csv.writer(csv_file)
          w.writerow(row + boundTitle)
        continue

      # 11: dict 12: ward 19: lat 20: lng
      b = []
      try:
        disarr = []

        for subdist in distMap[str(int(row[12]))][0]:
          for i in range(len(subdist) - 1):
            d, inline = cal(subdist[i], subdist[i+1], (float(row[20]), float(row[19])))
            disarr.append({
              'dis': d,
              'inline': inline,
            })

        for d in distance:
          bound = False
          for dis in disarr:
            if dis['dis'] < d and dis['inline']:
              bound = True
              break
          b.append(bound)
      except Exception as e:
        pass

      with open(outputfile, 'a') as csv_file:
        w = csv.writer(csv_file)
        w.writerow(row + b)
