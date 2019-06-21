import xlrd
from .outlookservice import send_my_message
from datetime import datetime as dt, timedelta
from TaaraMail.settings import MEDIA_ROOT, LOGO_BASE64, METHOD_1_BASE64, METHOD_2_BASE64

graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'


def filtred_selected_mail_sender(access_token, filename, vlz_report):
    location = MEDIA_ROOT + filename
    location_vlz_report = MEDIA_ROOT + vlz_report
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)

    wb_vlz_report = xlrd.open_workbook(location_vlz_report)
    sheet_vlz_report = wb_vlz_report.sheet_by_index(0)

    # the constants

    email_column = 1
    first_name_column = 2
    mylearn_column = 12

    # the constants for VLZ report

    award_column = 0
    email_column_vlz_report = 1
    joined_date_column = 2

    for i in range(0, sheet_vlz_report.ncols):
        if sheet_vlz_report.cell_value(0, i).lower() == "Award".lower():
            award_column = i
        elif sheet_vlz_report.cell_value(0, i).lower() == "Joined Date".lower():
            joined_date_column = i
        elif sheet_vlz_report.cell_value(0, i).lower() == "Email".lower():
            email_column_vlz_report = i

    level_up_subject = "<Pending Completion>Level 1 Course - VCA - Digital Business Transformation(VCA-DBT)"
    webinar_sign_up_subject = "<Coming Up> VMinclusion Taara - Briefing & QA Webinar - Sign Up Now!"
    activation_subject = "<Please Read> VMinclusion Taara > Activate Your Account & Kick Start Your Learning - TODAY!"

    level_up_body = "<html>" \
                    "<body>" \
                    "<a href=\"https://www.vmware.com/taara/ rel=\"_alt\">" \
                    "<img src=\"cid:logo_support\">" \
                    "</a>" \
                    "<br><br>" \
                    "Dear Candidate," \
                    "<br><br>Thank you for your interest in <strong>VMinclusion Taara</strong> Program! We see that you have enrolled in the Level 1 Course “<strong>VCA - Digital Business Transformation(VCA-DBT)</strong>”." \
                    "We also see that you have registered more than 30 days ago and this is still pending completion." \
                    "<br><br>We are sending a <strong>gentle reminder</strong> – for you to proceed to complete the course and then move forward to attempt the <strong>VCA-DBT Exam at the earliest.</strong>" \
                    "<br><br>We hope you make the most of this opportunity!" \
                    "<br><br>Regards," \
                    "<br>Team VMinclusion Taara" \
                    "<br><br><br><u>Disclaimer</u>: " \
                    "<strong>By commencing with the program, you are confirming that you are eligible to apply. Please note the eligibility criteria before proceeding:</strong>" \
                    "<ul>" \
                    "<li>This Program is open only for <u>women, who are citizens of India</u>, who currently reside within the territorial jurisdiction of India, should be a minimum of 18 years and have prior work experience in the field of Information Technology (IT) and the <u>applicant should not currently and for the minimum of last 6 months be in active employment with any company</u> (whether in India or abroad)." \
                    "<li>VMware will in its sole discretion shortlist and accept a total of 15,000 applications for participation for the Program (\"Participants\"), on first come first serve basis. Furthermore, VMware reserves the right to accept or reject applications at its sole discretion." \
                    "<li>All other persons are ineligible to enter the Program." \
                    "</ul>" \
                    "</p>" \
                    "</body>" \
                    "</html>"

    activation_body = "<html>" \
                      "<body>" \
                      "<a href = \"https://www.vmware.com/taara/\" rel=\"_alt\">" \
                      "<img src=\"cid:logo_support\">" \
                      "</a>" \
                      "<p>Hello!" \
                      "<br><br>" \
                      "Thank you for your interest in <strong>VMinclusion Taara</strong> Program!" \
                      "<br><br>We are sending a gentle reminder as we see that you have created your profile, " \
                      "but we also " \
                      "see that you have not activated your account." \
                      "<br><br>Please activate your account and kick-start your learning journey as soon as possible!" \
                      "<br><br>" \
                      "<strong>How do you do that? Enter your email ID in the Sign Up Box -> Click on Sign Up -> " \
                      "Complete your profile information -> Set the security questions -> Set password -> Activate " \
                      "your account</strong>" \
                      "<br><br>" \
                      "<img src=\"cid:method_1_support\">" \
                      "<br><br>For more information regarding the program, certification, badges, etc, please go to " \
                      "<a href = \"https://www.vmware.com/taara/faq\" rel =\"_alt\">https://www.vmware.com/taara/faq</a>." \
                      "<br><br>" \
                      "Still have more questions around the program? <strong>Register in advance for this webinar by visiting our website : </strong>" \
                      "<a href=\"https://www.vmware.com/taara/\" rel=\"_alt\">https://www.vmware.com/taara/</a>" \
                      "<br><br><img src=\"cid:method_2_support\">" \
                      "<br><br>" \
                      "<strong>After registering, you will receive a confirmation email containing information on how you can join the webinar.</strong>" \
                      "<br><br><strong>We hope you make the most of this opportunity!</strong><br><br>" \
                      "Regards,<br><br>" \
                      "Team VMinclusion Taara" \
                      "<br><br><br><u>Disclaimer</u>: " \
                      "<strong>By commencing with the program, you are confirming that you are eligible to apply. Please note the eligibility criteria before proceeding:</strong>" \
                      "<ul>" \
                      "<li>This Program is open only for <u>women, who are citizens of India</u>, who currently reside within the territorial jurisdiction of India, should be a minimum of 18 years and have prior work experience in the field of Information Technology (IT) and the <u>applicant should not currently and for the minimum of last 6 months be in active employment with any company</u> (whether in India or abroad)." \
                      "<li>VMware will in its sole discretion shortlist and accept a total of 15,000 applications for participation for the Program (\"Participants\"), on first come first serve basis. Furthermore, VMware reserves the right to accept or reject applications at its sole discretion." \
                      "<li>All other persons are ineligible to enter the Program." \
                      "</ul>" \
                      "</p>" \
                      "</body>" \
                      "</html>"

    webinar_sign_up_body = "<html>" \
                           "<body>" \
                           "<a href = \"https://www.vmware.com/taara/\" rel=\"_alt\">" \
                           "<img src=\"cid:logo_support\">" \
                           "</a>" \
                           "<p><br><br>You are invited to a Zoom webinar!" \
                           "<br><br><strong>When: Mar 7, 2019 11:00 AM India" \
                           "<br><br>Register in advance for this webinar by visiting our website: " \
                           "<a href=\"https://www.vmware.com/taara/\" rel= \"_alt\">https://www.vmware.com/taara/</a></strong>" \
                           "<br><br>" \
                           "<img src=\"cid:method_2_support\">" \
                           "<br><br><strong>After registering, you will receive a confirmation email containing information on how you can join the webinar</strong><br><br>" \
                           "For more information regarding the program : " \
                           "<a href = \"https://www.vmware.com/taara/faq\" rel=\"_alt\">https://www.vmware.com/taara/faq</a>." \
                           "<br><br>Regards,<br>" \
                           "Team VMinclusion Taara" \
                           "<br><br><br><u>Disclaimer</u>: " \
                           "<strong>By commencing with the program, you are confirming that you are eligible to apply. Please note the eligibility criteria before proceeding:</strong>" \
                           "<ul>" \
                           "<li>This Program is open only for <u>women, who are citizens of India</u>, who currently reside within the territorial jurisdiction of India, should be a minimum of 18 years and have prior work experience in the field of Information Technology (IT) and the <u>applicant should not currently and for the minimum of last 6 months be in active employment with any company</u> (whether in India or abroad)." \
                           "<li>VMware will in its sole discretion shortlist and accept a total of 15,000 applications for participation for the Program (\"Participants\"), on first come first serve basis. Furthermore, VMware reserves the right to accept or reject applications at its sole discretion." \
                           "<li>All other persons are ineligible to enter the Program." \
                           "</ul>" \
                           "</p>" \
                           "</body>" \
                           "</html>"

    ######################

    number_of_entries = sheet.nrows
    number_of_entries_vlz_report = sheet_vlz_report.nrows

    for i in range(2, number_of_entries):
        TO = sheet.cell_value(i, email_column)

        # Webinar General Sign Up

        payload = {
            "message": {
                "subject": webinar_sign_up_subject,
                "body": {
                    "contentType": "html",
                    "content": webinar_sign_up_body
                },
                "from": {
                    "emailAddress": {
                        "name": "Taara VMInclusion",
                        "address": "taara_vminclusion@vmware.com"
                    }
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": TO
                        }
                    }
                ],
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
            "saveToSentItems": "true"
        }

        send_my_message(access_token=access_token, payload=payload)
        # -------------------------

        # Activate your account mail

        if sheet.cell_value(i, first_name_column) != "" and sheet.cell_value(i, mylearn_column) == 0:
            payload = {
                "message": {
                    "subject": activation_subject,
                    "body": {
                        "contentType": "html",
                        "content": activation_body
                    },
                    "from": {
                        "emailAddress": {
                            "name": "Taara VMInclusion",
                            "address": "taara_vminclusion@vmware.com"
                        }
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": TO
                            }
                        }
                    ],
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
                "saveToSentItems": "true"
            }

            send_my_message(access_token=access_token, payload=payload)
        # -------------------------

    for i in range(1, number_of_entries_vlz_report):
        joined_date = sheet_vlz_report.cell_value(i, joined_date_column)
        joined_date_refined = joined_date.split(" ")
        joined_date_refined[0] = joined_date_refined[0].replace("/", "-")

        current_date = dt.utcnow() - timedelta(hours=8)  # PST
        current_date_refined = str(current_date.month) + "-" + str(current_date.day) + "-" + str(current_date.year)

        a = dt.strptime(joined_date_refined[0], "%m-%d-%Y")
        b = dt.strptime(current_date_refined, "%m-%d-%Y")

        # Level Up for the program mail
        if sheet_vlz_report.cell_value(i, award_column) == 0 and (b-a).days >= 30:
            payload = {
                "message": {
                    "subject": level_up_subject,
                    "body": {
                        "contentType": "html",
                        "content": level_up_body
                    },
                    "from": {
                        "emailAddress": {
                            "name": "Taara VMInclusion",
                            "address": "taara_vminclusion@vmware.com"
                        }
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": sheet_vlz_report.cell_value(i, email_column_vlz_report)
                            }
                        }
                    ],
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
                "saveToSentItems": "true"
            }

            send_my_message(access_token=access_token, payload=payload)
        # -------------------------
