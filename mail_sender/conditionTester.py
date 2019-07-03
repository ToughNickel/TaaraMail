import xlrd
from TaaraMail.settings import MEDIA_ROOT


def conditionTester(filename, parameter_dict, parameter_col_dict, i):
    print("\n********************************\n\n\n\n\n\n\n\nReached conditionTester")
    location = MEDIA_ROOT + filename
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)

    number_of_rows = sheet.nrows
    number_of_cols = sheet.ncols

    for k, v in parameter_col_dict.items():
        print("\t For parameter_col_dict  k = %s and v = %s \n \t ---> typeof(sheet.cell_value(%s, %s)) = %s and typeof(parameter_dict[%s]) = %s" %
              (k, v, i, v, type(sheet.cell_value(i, v)), k, type(parameter_dict[k])))
        cell_value = str(sheet.cell_value(i, v)).lower().strip()
        required_value = parameter_dict[k].lower().strip()

        if cell_value != required_value:
            print("sheet.cell_value(%s, %s) = %s whereas parameter_dict[%s] = %s \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" %
                  (i, v, sheet.cell_value(i, int(v)), k, parameter_dict[k]))
            return False

    return True
