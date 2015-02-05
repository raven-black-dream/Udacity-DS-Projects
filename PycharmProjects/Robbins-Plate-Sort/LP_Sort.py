__author__ = 'Evan Harley'

# License Plate Sorting Script for Robbins Parking
import xlrd
from datetime import date, datetime as dt
from collections import Counter
import os

# "Main" method


def process_lp_spreadsheet():
    current_date = date.today()
    file_path = os.path.normpath('C:/Users/Evan/My Documents/Robbins - License Place Sort/')
#    file_path = os.path.normpath("C:/users/patroller1/desktop/airport/Mo's Reports Data/")
    file_name = "\Airport_" + str(current_date.year) + ".xlsx"
    filename = file_path + file_name
    workbook = xlrd.open_workbook(filename)
    sheet_names = workbook.sheet_names()
    given_date = sheet_names[len(sheet_names) - 1]
    sorted_data = lp_prepare(workbook, given_date)
    keys = sorted(sorted_data.keys())
    processed_data = lp_process(sorted_data)
    dates = (keys[0], keys[len(keys) - 1])
    lp_write(processed_data, dates, file_path, file_name)


def lp_prepare(workbook, given_date):  # Prepares the data to be processed
    i = 0
    sheet_names = workbook.sheet_names()
    given_date_as_dt = dt.strptime(given_date, "%b %d %Y")
    sort_method = False
    for blah in range(len(sheet_names)):
        sheet_names[blah] = dt.strptime(sheet_names[blah], "%b %d %Y")
    if len(sheet_names) <= 7:
        sort_method = True
    for day in range(len(sheet_names)):
        if given_date_as_dt == sheet_names[day]:
            i = day
            break
    if sort_method:
        data = lp_sort(workbook, sheet_names, (i, -1, -1))
    else:
        data = lp_sort(workbook, sheet_names, (i, i - 8, -1))

    return data


def lp_sort(workbook, sheet_names, rng):  # sorts each sheet in the worksheet into a dictionary by date
    inc = 0
    data = {}

    for tab in range(rng[0], rng[1], rng[2]):
        plates = []
        sheet = workbook.sheet_by_index(tab)
        for row in range(sheet.nrows):
            if sheet.cell_value(row, 0) == "LP":
                continue
            elif len(str(sheet.cell_value(row, 0))) <= 5 or len(str(sheet.cell_value(row, 0))) > 7:
                continue
            else:
                plates.append(str(sheet.cell_value(row, 0)))
        data[sheet_names[inc]] = sorted(plates)
        inc += 1
    return data

# Counts each instance of a licence plate number and divides them by the scan number they were last seen in


def lp_process(data):
    final_data = {}
    keys = sorted(data.keys())
    count = Counter(data[keys[len(keys) - 1]])
    plates_count = {}
    for plate in count:
        plates_count[plate] = {'count': count[plate]}
        plates_count[plate]['scans'] = []
        if 1 not in plates_count[plate]['scans']:
            plates_count[plate]['scans'].append(1)
    scan_num = 2
    for i in range(len(keys) - 2, -1, -1):
        temp_count = Counter(data[keys[i]])

        for plate in temp_count:
            if plate in plates_count:
                plates_count[plate]['count'] += 1
                if scan_num not in plates_count[plate]['scans']:
                    plates_count[plate]['scans'].append(scan_num)
            else:
                plates_count[plate] = {'count': 1}
                plates_count[plate]['scans'] = []
                plates_count[plate]['scans'].append(scan_num)
        scan_num += 1

    final_data['first_time'] = []
    final_data['not_present_in_1'] = []
    final_data['not_present_in_2'] = []
    final_data['not_present_in_3'] = []
    final_data['not_present_in_4'] = []
    final_data['not_present_in_5'] = []
    final_data['not_present_in_6'] = []
    final_data['not_present_in_7'] = []
    final_data['present_in_all'] = []
    for plate in plates_count:
        lst = plates_count[plate]['scans']
        if len(lst) == len(keys):
            final_data['present_in_all'].append(plate)
        elif len(lst) == 1 and 1 in lst:
            final_data['first_time'].append(plate)
        elif 2 in lst and sorted(lst).index(2) == 0:
            final_data['not_present_in_1'].append(plate)
        elif 3 in lst and sorted(lst).index(3) == 0:
            final_data['not_present_in_2'].append(plate)
        elif 4 in lst and sorted(lst).index(4) == 0:
            final_data['not_present_in_3'].append(plate)
        elif 5 in lst and sorted(lst).index(5) == 0:
            final_data['not_present_in_4'].append(plate)
        elif 6 in lst and sorted(lst).index(6) == 0:
            final_data['not_present_in_5'].append(plate)
        elif 7 in lst and sorted(lst).index(7) == 0:
            final_data['not_present_in_6'].append(plate)
        elif 8 in lst and sorted(lst).index(8) == 0:
            final_data['not_present_in_7'].append(plate)
    for datum in final_data:
        final_data[datum] = sorted(final_data[datum])
    return final_data


def lp_write(data, dates, path, name):
    usable_name = name.partition('.')
    filename = path + usable_name[0] + "-" + date.strftime(dates[0], "%d%b%y")\
        + "-" + date.strftime(dates[1], "%d%b%Y") + ".txt"
    with open(filename, 'w') as f:
        if len(data['present_in_all']) != 0:
            f.write("----Present in all scans----\n")
            for i in range(0, len(data['present_in_all']), 1):
                if (i + 1) % 5 == 0 or i == (len(data['present_in_all']) - 1):
                    f.write(data['present_in_all'][i] + " | \n")
                else:
                    f.write(data['present_in_all'][i] + " | ")
        if len(data['not_present_in_1']) != 0:
            f.write("\n----Not present in most recent scan----\n")
            for i in range(0, len(data['not_present_in_1']), 1):
                if (i + 1) % 5 == 0 or i == (len(data['not_present_in_1']) - 1):
                    f.write(data['not_present_in_1'][i] + " | \n")
                else:
                    f.write(data['not_present_in_1'][i] + " | ")
        for index in range (2, 8, 1):
            if len(data['not_present_in_{0}'.format(index)]) != 0:
                f.write("\n----Not present in {0} most recent scans----\n".format(index))
                for i in range(0, len(data['not_present_in_{0}'.format(index)]), 1):
                    if (i + 1) % 5 == 0 or i == (len(data['not_present_in_{0}'.format(index)]) - 1):
                        f.write(data['not_present_in_{0}'.format(index)][i] + " | \n")
                    else:
                        f.write(data['not_present_in_{0}'.format(index)][i] + " | ")

    f.close()

process_lp_spreadsheet()