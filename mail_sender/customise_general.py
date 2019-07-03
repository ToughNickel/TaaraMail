import xlrd
from TaaraMail.settings import MEDIA_ROOT
from .conditionTester import conditionTester


def customise_general(access_token, filename, parameter_dict, subject, body):
    location = MEDIA_ROOT + filename
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)

    number_of_rows = sheet.nrows
    number_of_cols = sheet.ncols

    parameter_col_dict = {}

    for k in parameter_dict:
        for i in range(0, number_of_cols):
            if sheet.cell_value(1, i).lower() == k.lower():
                parameter_col_dict[k] = i
                break

    for i in range(2, number_of_rows):
        if conditionTester(filename=filename, parameter_dict=parameter_dict, parameter_col_dict=parameter_col_dict,
                           i=i):
            print("Send Email --> {}".format(sheet.cell_value(i, 1)))
