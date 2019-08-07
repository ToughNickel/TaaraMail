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
        print("\t For parameter_col_dict  k = %s and v = %s \n \t ---> typeof(sheet.cell_value(%s, %s)) = %s and "
              "typeof(parameter_dict[%s]) = %s" %
              (k, v, i, v, type(sheet.cell_value(i, v)), k, type(parameter_dict[k])))
        cell_value = str(sheet.cell_value(i, v)).lower().strip()

        # handling a float value
        if ".0" in cell_value:
            cell_value = cell_value.replace(".0", "")

        # handling for FALSE and TRUE cases value
        if str(parameter_dict[k].lower().strip()) in ["true", "false"]:
            if cell_value == "1":
                cell_value = "true"
            elif cell_value == "0":
                cell_value = "false"

        # deciding whether condition is for a value or for it not being blank/not blank

        if parameter_dict[k].lower().strip() == "blank":
            required_value = ""
        elif parameter_dict[k].lower().strip() == "not_blank":
            required_value = "not_blank_rajn_is_telling"
        else:
            required_value = str(parameter_dict[k].lower().strip())

        if required_value != "not_blank_rajn_is_telling":
            if cell_value != required_value:
                print("sheet.cell_value(%s, %s) = %s whereas parameter_dict[%s] = %s \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                      "\n\n" %
                      (i, v, sheet.cell_value(i, int(v)), k, parameter_dict[k]))
                return False
        else:
            if cell_value == "":
                return False

    return True
