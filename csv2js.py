from datetime import datetime

file = open('data.csv', 'r')
data = file.read()

years = set()
birds = set()
ybd = dict()

lines = data.split('\n')
for line in lines:
    bird, _, year, date = line.split(',')
    year = int(year)
    if year not in years:
        years.add(year)
    if bird not in birds:
        birds.add(bird)

    day, month, year_again = date.split('/')
    day = int(day)
    month = int(month)
    year_again = int(year_again)
    assert(year == year_again)
    day_of_year = datetime(year, month, day).timetuple().tm_yday

    key = (year, bird)
    assert(key not in ybd)
    ybd[key] = day_of_year

out_matrix = list()

sorted_years = sorted(years)
sorted_birds = sorted(birds)
for i, year in enumerate(sorted_years):
    out_matrix.append(list())
    for bird in sorted_birds:
        key = (year, bird)
        if key in ybd:
            val = ybd[key]
        else:
            val = 'null'
        out_matrix[i].append(val)

out = "var arr = [\n"
column_headers = list(sorted_birds)
column_headers.insert(0, 'Year')
out += str(column_headers) + ',\n'
for i, year in enumerate(sorted_years):
    row = list(out_matrix[i])
    row.insert(0, year)
    out += str(row).replace("'", "") + ",\n"
out += "        ];"

# var arr = [
#           ['Year', 'Art1', 'Art2'],
#           ['2004',   null,      400],
#           ['2005',   1170,      460],
#           ['2006',   660,       1120],
#           ['2008',   1030,      540],
#           ['2009',   1030,      null],
#         ];

print(out)

file.close()
