import xlrd
from TaaraMail.settings import MEDIA_ROOT


def getParameters(filename):
    location = MEDIA_ROOT + filename
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)

    number_of_rows = sheet.nrows
    number_of_cols = sheet.ncols

    parameters = []

    decisive_index = 0

    if "column".lower().strip() in str(sheet.cell_value(decisive_index, 1)).lower().strip() or "Taara".lower().strip() in str(sheet.cell_value(decisive_index, 0)).lower().strip():
        decisive_index = decisive_index + 1

    for i in range(0, number_of_cols):
        parameters.append(sheet.cell_value(decisive_index, i))

    return parameters
