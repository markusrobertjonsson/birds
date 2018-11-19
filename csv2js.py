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

group_tropik = ['Näktergal', 'Blåhake', 'Rödstjärt', 'Buskskvätta', 'Stenskvätta', 'Gräshoppsångare', 'Sävsångare', 'Kärrsångare',
'Rörsångare', 'Härmsångare', 'Höksångare', 'Ärtsångare', 'Törnsångare', 'Trädgårdssångare', 'Svarthätta', 'Grönsångare', 'Lövsångare',
'Grå flugsnappare', 'Mindre flugsnappare', 'Svartvit flugsnappare', 'Törnskata', 'Rosenfink', 'Göktyta']
group_medelkort = ['Svart rödstjärt', 'Koltrast', 'Rödvingetrast', 'Gransångare', 'Bofink', 'Bergfink', 'Gulsparv', 'Sävsparv',
'Steglits', 'Gärdsmyg', 'Järnsparv', 'Rödhake', 'Björktrast', 'Kungsfågel', 'Blåmes', 'Talgoxe', 'Grönfink', 'Grönsiska', 'Gråsiska']

tropik_average = dict()
tropik_count = dict()
medelkort_average = dict()
medelkort_count = dict()

for key in ybd:
    year = key[0]
    bird = key[1]
    val = ybd[key]
    if val is None:
        continue
    if bird in group_tropik:
        if year in tropik_average:
            tropik_average[year] += val
            tropik_count[year] += 1
        else:
            tropik_average[year] = val
            tropik_count[year] = 1
    if bird in group_medelkort:
        if year in medelkort_average:
            medelkort_average[year] += val
            medelkort_count[year] += 1
        else:
            medelkort_average[year] = val
            medelkort_count[year] = 1

# print(tropik_average)
# print(tropik_count)
# print(medelkort_average)
# print(medelkort_count)

for year in tropik_average:
    tropik_average[year] /= tropik_count[year]
    ybd[(year, 'tropik')] = tropik_average[year]
for year in medelkort_average:
    medelkort_average[year] /= medelkort_count[year]
    ybd[(year, 'medelkort')] = medelkort_average[year]

out_matrix = list()

sorted_years = sorted(years)
sorted_birds = sorted(birds)
sorted_birds.append('tropik')
sorted_birds.append('medelkort')

for i, year in enumerate(sorted_years):
    out_matrix.append(list())
    for bird in sorted_birds:
        key = (year, bird)
        if key in ybd:
            val = ybd[key]
        else:
            val = 'null'
        out_matrix[i].append(val)

out = "var all_birds_with_data = [\n"
column_headers = list(sorted_birds)
column_headers.insert(0, 'Year')
out += str(column_headers) + ',\n'
for i, year in enumerate(sorted_years):
    row = list(out_matrix[i])
    # row.insert(0, '"' + str(year) + '"')
    row.insert(0, "new Date(" + str(year) + ", 1, 1)")
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
