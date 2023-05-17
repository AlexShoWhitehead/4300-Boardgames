import csv

'''
combine multiple CSVs (1000 games each) into one larger file
'''
SHEET_PREFIX = 'datasets\sheet_'
NUM_SHEETS = 21


sheets = [str(SHEET_PREFIX + str(i).zfill(2) + '.csv') for i in range(NUM_SHEETS)]
sheets.append('datasets\sheet_missed.csv')
all_rows = []

with open(sheets[0], newline='', encoding='UTF-8') as c:
    read = csv.reader(c, delimiter=',')
    headers = next(read)


print(type(headers))

for sheet in sheets:
    print('opening sheet ' + sheet)
    with open(sheet, newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            all_rows.append(row)
        csvfile.close()
    print('parsed sheet ' + sheet)

print(len(all_rows))

with open('datasets/master_database.csv', 'w', newline='', encoding='UTF-8') as master_csv:
    writer = csv.writer(master_csv, delimiter=';')
    writer.writerow(headers)
    for row in all_rows:
        writer.writerow(row)
