import csv


regions = {}
with open('MyTarget_regions.csv', 'r') as data:
    data_reader = csv.DictReader(data)
    for line in data_reader:
        regions[line['id']] = line['name']

print(regions)
