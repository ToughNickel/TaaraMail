# Taara Automated Mail Sending Solution

## Statement
[VMware Taara Initiative](https://www.vmware.com/taara/) is a program, where VMware will upskill 15,000 women in India over the next two years and uplift their careers for growth and impact, by providing free technical education and certification courses on ** digital business transformation ** technologies.
In order to update the participants about their account activation status, their signing up and their level of completion of VCP - DBT Certification. An excel spreadsheet is being maintained with several flags for indicating the level pf their participation, and thus the kind of mail they should receive for the update.

## Solution 
So this is a Django project which implements [Outlook Mail API](https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/mail-rest-operations#GetMessages) for sending the mass mails with filters defined. 
Tools used for this:
* Django
* Microsoft Graph API 
* xlrd (Python Excel operation module)
