from bs4 import BeautifulSoup, NavigableString
import xlrd
from TaaraMail.settings import MEDIA_ROOT


def Entry_wise_value_conversion(body, filename, row_number):
    print("\n\n\n\n\nEntered the def\n\n\n\n")
    location = MEDIA_ROOT + filename
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)

    number_of_rows = sheet.nrows
    number_of_cols = sheet.ncols

    email_column = -1

    decisive_index = 0

    if "column".lower().strip() in str(sheet.cell_value(decisive_index, 1)).lower().strip() or \
            "Taara".lower().strip() in str(sheet.cell_value(decisive_index, 0)).lower().strip() or \
            str(sheet.cell_value(decisive_index, 1)).lower().strip() == "":
        decisive_index = decisive_index + 1

    parameter_name_column_number = {}

    for i in range(0, number_of_cols):
        parameter_name_column_number[sheet.cell_value(decisive_index, i)] = i

    value_to_be_inserted = sheet.cell_value(row_number, 0)

    body_to_be_returned = body
    soup = BeautifulSoup(body_to_be_returned, 'html.parser')

    for item in soup.find_all('p'):
        strOp = item.getText()
        column_name = "#"
        if "{{" in strOp:
            print("\n\n\n\tFound swiggles \n")
            strList = strOp.split("{{")
            print("\t", str(int(len(strList) - 1)), " <-- these many\n\n\n\n")
            for i in range(1, len(strList)):
                strTemp = strList[i]
                column_name = strTemp.split("}}")[0]
                column_name = column_name.strip()
                print("\t\t\t", column_name, " <--- column name\n\n\n")
                # finding the column_number
                print("\n\n\t\t\t column name's type : ", type(column_name))
                print("\n\n\n\n")
                print(" the index of the column by the name: ", column_name, "is : -> ", parameter_name_column_number[column_name])
                column_number = parameter_name_column_number[column_name]
                print("\t\t\t column number is : ", column_number, "\n\n\n")
                value_to_be_inserted = sheet.cell_value(row_number, column_number)
                print("\n\t\t\t value to be inserted : ", value_to_be_inserted, "\n\n")
                _str_be_replaced = "{{ %s }}" % column_name
                print("\n\n\n\n\n\t\t\tvalue that is going to be replaced : -> ", _str_be_replaced, " \n\n\n")
                strOp = strOp.replace(_str_be_replaced, value_to_be_inserted)
                print("value of strOp : ", strOp, "\n\n\n\n\n")
                item.replace_with(strOp)
        else:
            print("\n\n\n\n\n\t\t\t\tDon't have a custom salutation\n\n\n\n\n")
    return soup.prettify()
