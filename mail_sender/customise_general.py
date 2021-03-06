import xlrd
from TaaraMail.settings import MEDIA_ROOT
from .conditionTester import conditionTester
from .outlookservice import send_my_message
from TaaraMail.settings import LOGO_BASE64, METHOD_1_BASE64, METHOD_2_BASE64
from .entryWiseValueInsertion import Entry_wise_value_conversion


def customise_general(access_token, filename, parameter_dict, subject, body, attachments):
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

    for i in range(0, number_of_cols):
        if sheet.cell_value(decisive_index, i).lower().strip() == "email".lower().strip():
            email_column = i
            print("\n\n\n\n ******************** EMAIL COLUMN FOUND AT *********************** \n\n", email_column,
                  "\n\n\n\n\n")
            break

    parameter_col_dict = {}

    for k in parameter_dict:
        for i in range(0, number_of_cols):
            if sheet.cell_value(decisive_index, i).lower() == k.lower():
                parameter_col_dict[k] = i
                break

    for i in range(decisive_index + 1, number_of_rows):
        if conditionTester(filename=filename, parameter_dict=parameter_dict, parameter_col_dict=parameter_col_dict,
                           i=i):
            TO = sheet.cell_value(i, email_column)

            # Adding the respective salutation
            # Entry Wise Value Conversion

            body_modified = Entry_wise_value_conversion(body=body, filename=filename, row_number=i)

            # --------------------------------
            payload = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "html",
                        "content": body_modified
                    },
                    "from": {
                        "emailAddress": {
                            "name": "Corporate View Team",
                            "address": "corp-view-team@vmware.com"
                        }
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": TO
                            }
                        }
                    ],
                    # "CcRecipients": [
                    #     {
                    #         "emailAddress": {
                    #             "name": "Taara VMInclusion",
                    #             "address": "taara_vminclusion@vmware.com"
                    #         }
                    #     }
                    # ],
                    "Attachments": [
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "Name": "logo.png",
                            "isInline": True,
                            "ContentId": "logo_support",
                            "ContentBytes": LOGO_BASE64
                        },
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "Name": "method.jpg",
                            "isInline": True,
                            "ContentId": "method_1_support",
                            "ContentBytes": METHOD_1_BASE64
                        },
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "Name": "method2.jpg",
                            "isInline": True,
                            "ContentId": "method_2_support",
                            "ContentBytes": METHOD_2_BASE64
                        }
                    ]
                },
                "saveToSentItems": "false"
            }

            if len(attachments) != 0:
                payload['message']['Attachments'].extend(attachments)

            send_my_message(access_token=access_token, payload=payload)
            print("Send Email --> {}".format(sheet.cell_value(i, email_column)))
