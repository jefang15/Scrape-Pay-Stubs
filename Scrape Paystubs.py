""" Scraping Text from PDF (Paystubs) """

import glob
import pdfplumber
import pandas as pd
from tabulate import tabulate



" Scrape PayStubs "


import pdfplumber
import pandas as pd

" Import PDF "

# Single file as a test
test_pdf = pdfplumber.open(r'Projects/Scrape-Paystubs/FERC - Earnings & Leave Statements/normal.pdf')
len(test_pdf.pages)


" Extract text from PDF "

# Single page
test_pdf_text = test_pdf.pages[0].extract_text().replace('\n', '<end>')
print(test_pdf_text)

# all pages, as string, hopefully
string = ''
for i in range(0, len(test_pdf.pages)):
    string += test_pdf.pages[i].extract_text().replace('\n', '<end>')


" Extraction method for single item "

# Set up keyword that describes the data to extract
keyword = 'Pay Period Ending : '
print(keyword)

# Return index position of pdf that contains keyword
value_index = string.find(keyword)
print(value_index)  # keyword starts at index no. 129

# Find starting index of desired value following the keyword
start = string.find(keyword) + len(keyword) + 1
print(start)  # value associated with keyword starts at index no. 150

# Search string for desired value based on its index
string[(value_index+len(keyword)):string.find('<end>', string.find(keyword))]
# The find function in the second index position looks for <end> starting at the point in the string that begins with
# the keyword.



" Shorter version "

headings = [
    'Pay Period End Date',
    'Net Pay'
    ]

# Blank list to store extracted data "
out = []

# Pay period End Date
pp_end = string[(string.find('Pay Period Ending : ')+len('Pay Period Ending : ')):(string.find('<end>', string.find(
    'Pay Period Ending : ')))]
out.append(pp_end)

# Net pay
net_pay = string[(string.find('Net Pay $ : ')+len('Net Pay $ : ')):(string.find('<end>', string.find(
    'Net Pay $ : ')))]
out.append(net_pay)
print(out)

# Pay period
print(string[(string.find('Pay Period # : ')+len('Pay Period # : ')):(string.find('<end>', string.find(
    'Pay Period # : ')))])

# Pay date
print(string[(string.find('Pay Date : ')+len('Pay Date : ')):(string.find('<end>', string.find(
    'Pay Date : ')))])

# Pay plan
print(string[(string.find('Pay Plan : ')+len('Pay Plan : ')):(string.find('<end>', string.find(
    'Pay Plan : ')))])

# Pay Grade :
print(string[(string.find('Pay Grade : ')+len('Pay Grade : ')):(string.find('<end>', string.find(
    'Pay Grade : ')))])

# Pay Step :
# Annual Salary $ :
# Hourly Rate $ :
# YTD Wages:
# Gross Pay YTD:
# Total Deductions YTD:
# Net Pay Current:
# Maximum Carry Over:
# Use Or Lose Balance:
# Annual Leave Begin Balance Current:
# Annual Leave Begin Balance Leave Year:
# Annual Leave Earned Current:
# Annual Leave Earned YTD:
# Annual Leave Advanced:
# Annual Leave Ending Balance:

# Sick Leave Begin Balance Current:
# Sick Leave Begin Balance Leave Year:
# Sick Leave Earned Current:
# Sick Leave Earned YTD:
# Sick Leave Used Current:
# Sick Leave Used YTD:
# Sick Leave Advanced:
# Sick Leave Ending Balance:
# Time Off Award Begin Balance Current:
# Time Off Award Begin Balance Leave Year:
# Time Off Award Advanced:
# Time Off Award Ending Balance:


" Items with different format "

# Home Address
print(string[(string.find('Home Address')+len('Home Address')+len('<end>')):(string.find('Pay Check', string.find(
    'Home Address')))-len('<end>')])

# Federal Taxes Adjusted - adjusted
print(string[(string.find('Federal Taxes Adjusted')+len('Federal Taxes Adjusted')):(string.find('Adjusted', string.find(
    'Federal Taxes Adjusted')))])

# Federal Taxes Adjusted - current
federal_taxes_adjusted = string.find('Federal Taxes Adjusted')  # index of variable desired
print(federal_taxes_adjusted)  # 1906

federal_taxes_adjusted_substring = string[federal_taxes_adjusted:]
print(federal_taxes_adjusted_substring)  # new substring starting at variable desired

print(federal_taxes_adjusted_substring[(federal_taxes_adjusted_substring.find('Misc | ')+len('Misc | '
                                                                                                    '')):(
    federal_taxes_adjusted_substring.find(' Current', federal_taxes_adjusted_substring.find(
    'Misc | ')))])

# Federal Taxes Adjusted - YTD
federal_taxes_adjusted_substring

print(federal_taxes_adjusted_substring[(federal_taxes_adjusted_substring.find('Current PPD | ')+len('Current PPD | '
                                                                                                    '')):(
    federal_taxes_adjusted_substring.find(' YTD', federal_taxes_adjusted_substring.find(
    'Current PPD | ')))])

" The following follow the same format as Federal Taxes "
# State Tax 1 ( DC )
# Health Benefits - Pretax Adjusted
# Dental/Vision Adjusted
# TSP Tax Deferred Adjusted
# Retirement - FERS/FRAE Adjusted
# OASDI Tax Adjusted
# Medicare Tax Adjusted
# FEGLI - Regular Adjusted

" Follows a different format "

# Service Comp Date
print(string[(string.find('Service Comp Date')+len('Service Comp Date')):(string.find(':', string.find(
    'Service Comp Date')))])
# Agency
# Cumulative Retirement Agency
# Duty Station
# Pay Begin Date
# Financial Institution
# TSP Tax Deferred Amt/%


" Follows a different format "

benefits_paid_by_government_substring = string[string.find('Benefits Paid by Government'):]

# FEGLI - current
print(benefits_paid_by_government_substring[(benefits_paid_by_government_substring.find('FEGLI')+len('FEGLI')):(benefits_paid_by_government_substring.find(' Current', benefits_paid_by_government_substring.find('FEGLI')))])
# FEGLI - YTD
print(benefits_paid_by_government_substring[(benefits_paid_by_government_substring.find('Current PPD | ')+len(
    'Current PPD | ')):(benefits_paid_by_government_substring.find(' YTD', benefits_paid_by_government_substring.find(
    'Current PPD | ')))])

# Medicare
# OASDI
# TSP Basic
# TSP Matching
# FERS/FRAE


" Infrequent items "
# 'Time Off Award Begin Balance Current: ',
# 'Time Off Award Begin Balance Leave Year: '
# 'Time Off Award Advanced: '
# 'Time Off Award Ending Balance: '
# 'State Tax 1 ( VA )'
# 'State Tax 1 ( DC )'
# 'State Tax 2 ( DC )'



" Read Me "

" Extract information from each PDF "

# loop through each individually (run either this or the next section, not both)

# pp_ending = string[(string.find('Pay Period Ending : ') + len('Pay Period Ending : ')):(string.find('<end>', string.find(
#     'Pay Period Ending : ')))]
#
# net_pay = string[(string.find('Net Pay $ : ') + len('Net Pay $ : ')):(string.find('<end>', string.find(
#     'Net Pay $ : ')))]
#
# inner_list_single = [pp_ending, net_pay]
# print(inner_list_single)
# out_single.append(inner_list_single)





"------------------------------------------ New Code for Multiple PDFs ------------------------------------------"


" Call PDFs in Folder "

paystubs_folder = (glob.glob('Projects/Scrape-Paystubs/FERC - Earnings & Leave Statements/*.pdf'))


" Extract information from all PDFs "

out_multi = []

# Loop through each page of each PDF
for file in paystubs_folder:
    with pdfplumber.open(file) as pdf:
        string = ''  # Empty string to store text from each page within a single PDF
        for i in range(0, len(pdf.pages)):
            string += pdf.pages[i].extract_text().replace('\n', '<end>')

        value = []

        # loop through keywords
        keywords = [
            'Pay Period Ending : ',
            'Net Pay $ : ',
            'Pay Period # : ',
            'Pay Date : ',
            'Pay Plan : ',
            'Pay Grade : ',
            'Pay Step : ',
            'Pay Step : ',
            'Annual Salary $ : ',
            'Hourly Rate $ : ',
            'YTD Wages: ',
            'Gross Pay YTD: ',
            'Total Deductions YTD: ',
            'Net Pay Current: ',
            'Maximum Carry Over: ',
            'Use Or Lose Balance: ',
            'Annual Leave Begin Balance Current: ',
            'Annual Leave Begin Balance Leave Year: ',
            'Annual Leave Earned Current: ',
            'Annual Leave Earned YTD: ',
            'Annual Leave Advanced: ',
            'Annual Leave Ending Balance: ',
            'Sick Leave Begin Balance Current: ',
            'Sick Leave Begin Balance Leave Year: ',
            'Sick Leave Earned Current: ',
            'Sick Leave Earned YTD: ',
            'Sick Leave Used Current: ',
            'Sick Leave Used YTD: ',
            'Sick Leave Advanced: ',
            'Sick Leave Ending Balance: ',
            'Time Off Award Begin Balance Current: ',
            'Time Off Award Begin Balance Leave Year: ',
            'Time Off Award Advanced: ',
            'Time Off Award Ending Balance: '
            ]

        for i in keywords:
            if i in string:
                value.append(string[(string.find(i) + len(i)):(string.find('<end>', string.find(i)))])
            else:
                value.append(0)

        # Home Address
        value.append(string[(string.find('Home Address') + len('Home Address') + len('<end>')):(string.find('Pay Check',
                                                                                                              string.find('Home Address'))) - len('<end>')])

        " Deductions "

        keywords2 = [
            'Federal Taxes',
            'State Tax 1 ( DC )',
            'State Tax 1 ( VA )',
            'State Tax 2 ( DC )',
            'Health Benefits - Pretax',
            'Dental/Vision',
            'TSP Tax Deferred',
            'Retirement - FERS/FRAE',
            'OASDI Tax',
            'Medicare Tax',
            'FEGLI - Regular'
            ]

        for i in keywords2:
            if i in string:
                # Federal Taxes Adjusted - Adjusted
                value.append(string[(string.find(i) + len(i)):(string.find('Adjusted', string.find(i)))])
            else:
                value.append(0)

            if i in string:
                element_substring = string[string.find(i):]
                # Federal Taxes Adjusted - Current
                value.append(element_substring[(element_substring.find('Misc | ') + len('Misc | ')):(element_substring.find(
                    'Current', element_substring.find('Misc | ')))])
            else:
                value.append(0)

            if i in string:
                # Federal Taxes Adjusted - YTD
                value.append(element_substring[(element_substring.find('Current PPD | ') + len('Current PPD | ')):(
                    element_substring.find(' YTD', element_substring.find('Current PPD | ')))])
            else:
                value.append(0)

        " Basic Info "

        keywords3 = [
            'Service Comp Date',
            'Agency',
            'Cumulative Retirement Agency',
            'Duty Station',
            'Pay Begin Date',
            'Financial Institution',
            'TSP Tax Deferred Amt/%'
            ]

        for i in keywords3:
            value.append(string[(string.find(i) + len(i)):(string.find(':', string.find(i)))])

        " Benefits "

        keywords4 = [
            'FEGLI',
            'Medicare',
            'OASDI',
            'TSP Basic',
            'TSP Matching',
            'FERS/FRAE'
            ]

        benefits_substring = string[string.find('Benefits Paid by Government'):]

        for i in keywords4:
            # Current
            value.append(benefits_substring[(benefits_substring.find(i) + len(i)):(benefits_substring.find(' Current',
                                                                                                          benefits_substring.find(i)))])

            # YTD
            element4_ytd = benefits_substring[(benefits_substring.find('Current PPD | ') + len('Current PPD | ')):(
                benefits_substring.find(' YTD', benefits_substring.find('Current PPD | ')))]
            value.append(element4_ytd)

        " Append all scraped values from inner list to outer list "
        out_multi.append(value)



print(out_multi)


" Create DataFrame "

headings = [
    'Pay Period Ending',
    'Net Pay',
    'Pay Period',
    'Pay Date',
    'Pay Plan',
    'Pay Grade',
    'Pay Step',
    'Pay Step',
    'Annual Salary',
    'Hourly Rate',
    'YTD Wages',
    'Gross Pay YTD',
    'Total Deductions YTD',
    'Net Pay Current',
    'Maximum Carry Over',
    'Use Or Lose Balance',
    'Annual Leave Begin Balance Current',
    'Annual Leave Begin Balance Leave Year',
    'Annual Leave Earned Current',
    'Annual Leave Earned YTD',
    'Annual Leave Advanced',
    'Annual Leave Ending Balance',
    'Sick Leave Begin Balance Current',
    'Sick Leave Begin Balance Leave Year',
    'Sick Leave Earned Current',
    'Sick Leave Earned YTD',
    'Sick Leave Used Current',
    'Sick Leave Used YTD',
    'Sick Leave Advanced',
    'Sick Leave Ending Balance',
    'Time Off Award Begin Balance Current',
    'Time Off Award Begin Balance Leave Year',
    'Time Off Award Advanced',
    'Time Off Award Ending Balance',
    'Home Address',
    'Federal Taxes Adjusted',
    'Federal Taxes Current',
    'Federal Taxes YTD',
    'State Tax 1 ( DC ) Adjusted',
    'State Tax 1 ( DC ) Current',
    'State Tax 1 ( DC ) YTD',
    'State Tax 1 ( VA ) Adjusted',
    'State Tax 1 ( VA ) Current',
    'State Tax 1 ( VA ) YTD',
    'State Tax 2 ( DC ) Adjusted',
    'State Tax 2 ( DC ) Current',
    'State Tax 2 ( DC ) YTD',
    'Health Benefits - Adjusted',
    'Health Benefits - Current',
    'Health Benefits - YTD',
    'Dental/Vision Adjusted',
    'Dental/Vision Current',
    'Dental/Vision YTD',
    'TSP Tax Deferred Adjusted',
    'TSP Tax Deferred Current',
    'TSP Tax Deferred YTD',
    'Retirement - FERS/FRAE Adjusted',
    'Retirement - FERS/FRAE Current',
    'Retirement - FERS/FRAE YTD',
    'OASDI Tax Adjusted',
    'OASDI Tax Current',
    'OASDI Tax YTD',
    'Medicare Tax Adjusted',
    'Medicare Tax Current',
    'Medicare Tax YTD',
    'FEGLI - Regular Adjusted',
    'FEGLI - Regular Current',
    'FEGLI - Regular YTD',
    'Service Comp Date',
    'Agency',
    'Cumulative Retirement Agency',
    'Duty Station',
    'Pay Begin Date',
    'Financial Institution',
    'TSP Tax Deferred Amt/%',
    'FEGLI Current',
    'FEGLI YTD',
    'Medicare Current',
    'Medicare YTD',
    'OASDI Current',
    'OASDI YTD',
    'TSP Basic Current',
    'TSP Basic YTD',
    'TSP Matching Current',
    'TSP Matching YTD',
    'FERS/FRAE Current',
    'FERS/FRAE YTD'
    ]

df = pd.DataFrame(out_multi, columns=headings)
print(df)







"------------------------------------------ Old Code Below ------------------------------------------"




# TODO: Redo code that scrapes earnings to pull values based on section heading.

# Create columns for dataframe
df_columns = ["Agency", "Pay_Period_Ending", "Net_Pay", "Pay_Period", "Pay_Date", "Plan", "Grade", "Step",
              "Annual_Salary", "Hourly_Rate", "Gross_Pay", "Total_Deductions", "Federal_Taxes", "State_Tax_DC",
              "State_Tax_VA", "Health_Benefits", "Dental_Vision", "TSP", "Retirement_FERS", "OASDI_Tax",
              "Medicare_Tax", "FEGLI_Regular", "Gov_FEGLI", "Gov_FEHB", "Gov_Medicare", "Gov_OASDI", "Gov_TSP_Basic",
              "Gov_TSP_Matching", "Gov_FERS", "Annual_Leave", "Annual_Leave_Earned"]
# "Sick_Leave", "Sick_Leave_Earned", "Time_Off_Award"
# TODO: Sick leave and time off award variables are messed up, probably from spot fixes in VA DC


" ############################################ ELS - No Health Insurance ############################################# "
# January - February 2019
# DC
# No health insurance

" Single PDF "

# Import single PDF
no_health_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - No Health "
                                       "Insurance/els-02_02_2019 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
no_health_single_text = no_health_single_pdf.pages[0].extract_text()
# Convert string to list
no_health_single_list = list(no_health_single_text.split())
# Dataframe from list
no_health_single_df = pd.DataFrame(no_health_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
no_health_folder = (glob.glob("Projects/Scrape-Paystubs/FERC - Earnings & Leave Statements/*.pdf"))

# Create blank list to store extracted PDF text
no_health_ext = []

# Loop through each PDF in folder
for file in no_health_folder:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[166].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[174].replace(",", ""), errors='coerce')
        State_Tax_VA = 0
        Health_Benefits = 0
        Dental_Vision = 0
        TSP = pd.to_numeric(pdf_text_words[179].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[185].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[190].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[195].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[200].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[213].replace(",", ""), errors='coerce')
        Gov_FEHB = 0
        Gov_Medicare = pd.to_numeric(pdf_text_words[216].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[219].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[223].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[227].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[230].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[255])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[257])
        Sick_Leave = pd.to_numeric(pdf_text_words[262])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[264])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    no_health_ext.append(innerlist)

# Create Dataframe from list
no_health_df = pd.DataFrame(no_health_ext, columns=df_columns)

" ################################################### ELS - Health ################################################### "
# March 2019
# DC
# Health insurance

" Single PDF "

# Import single PDF
health_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - Health "
                                    "Insurance/els-03_02_2019 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
health_single_text = health_single_pdf.pages[0].extract_text()
# Convert string to list
health_single_list = list(health_single_text.split())
# Dataframe from list
health_single_df = pd.DataFrame(health_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
health_folder = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - Health Insurance/*.pdf"))

# Create blank list to store extracted PDF text
health_ext = []

# Loop through each PDF in folder
for file in health_folder:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[166].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[174].replace(",", ""), errors='coerce')
        State_Tax_VA = 0
        Health_Benefits = pd.to_numeric(pdf_text_words[181].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[184].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[189].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[195].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[200].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[205].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[210].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[223].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[226].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[229].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[232].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[236].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[240].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[243].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[268])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[270])
        Sick_Leave = pd.to_numeric(pdf_text_words[275])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[277])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    health_ext.append(innerlist)

# Create Dataframe from list
health_df = pd.DataFrame(health_ext, columns=df_columns)

" ################################################ ELS - VA DC (2019) ################################################ "
# March 2019
# VA and DC state income tax
# With health insurance

" Single PDF "

# Import single PDF
va_dc_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - VA "
                                   "DC/els-03_16_2019 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
va_dc_single_text = va_dc_single_pdf.pages[0].extract_text()
# Convert string to list
va_dc_single_list = list(va_dc_single_text.split())
# Dataframe from list
va_dc_single_df = pd.DataFrame(va_dc_single_list, columns=['Field'])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
va_dc_folder = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - VA DC/*.pdf"))

# Create blank list to store extracted PDF text
va_dc_ext = []

# Loop through each PDF in folder
for file in va_dc_folder:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[171].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[187].replace(",", ""), errors='coerce')
        State_Tax_VA = pd.to_numeric(pdf_text_words[179].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[194].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[197].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[202].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[208].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[213].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[218].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[223].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[236].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[239].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[245].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[249].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[253].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[256].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[281])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[283])
        Sick_Leave = pd.to_numeric(pdf_text_words[288].replace(",", ""), errors='coerce')
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[290])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    va_dc_ext.append(innerlist)

# Create Dataframe from list
va_dc_df = pd.DataFrame(va_dc_ext, columns=df_columns)

# Spot fixes
# va_dc_df.loc[1, 'Sick_Leave'] = 76
# va_dc_df.loc[2, 'Sick_Leave'] = 68
# va_dc_df.loc[3, 'Sick_Leave'] = 56
# va_dc_df.loc[4, 'Sick_Leave'] = 92
# va_dc_df.loc[6, 'Sick_Leave'] = 64
# va_dc_df.loc[7, 'Sick_Leave'] = 96
# va_dc_df.loc[8, 'Sick_Leave'] = 72
# va_dc_df.loc[11, 'Sick_Leave'] = 100
# va_dc_df.loc[13, 'Sick_Leave'] = 104
# va_dc_df.loc[14, 'Sick_Leave'] = 86
# va_dc_df.loc[15, 'Sick_Leave'] = 60
# va_dc_df.loc[17, 'Sick_Leave'] = 108
# va_dc_df.loc[18, 'Sick_Leave'] = 82
#
# va_dc_df.loc[1, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[2, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[3, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[4, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[6, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[7, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[8, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[11, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[13, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[14, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[15, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[17, 'Sick_Leave_Earned'] = 4
# va_dc_df.loc[18, 'Sick_Leave_Earned'] = 4


" ############################################# ELS - Adjustment (2019) ############################################## "
# April 2019
# VA and DC state income tax
# With health insurance
# Some adjustment

" Single PDF "

# Import single PDF
va_dc_adj_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - "
                                       "Adjustment/els-04_13_2019 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
va_dc_adj_single_text = va_dc_adj_single_pdf.pages[0].extract_text()
# Convert string to list
va_dc_adj_single_list = list(va_dc_adj_single_text.split())
# Dataframe from list
va_dc_adj_single_df = pd.DataFrame(va_dc_adj_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
va_dc_adj_folder = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - Adjustment/*.pdf"))

# Create blank list to store extracted PDF text
va_dc_adj_ext = []

# Loop through each PDF in folder
for file in va_dc_adj_folder:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[177].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[193].replace(",", ""), errors='coerce')
        State_Tax_VA = pd.to_numeric(pdf_text_words[185].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[200].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[203].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[209].replace(",", ""), errors='coerce') + pd.to_numeric(
            pdf_text_words[208].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[216].replace(",", ""), errors='coerce') + pd.to_numeric(
            pdf_text_words[215].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[222].replace(",", ""), errors='coerce') + pd.to_numeric(
            pdf_text_words[221].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[228].replace(",", ""), errors='coerce') + pd.to_numeric(
            pdf_text_words[227].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[234].replace(",", ""), errors='coerce') + pd.to_numeric(
            pdf_text_words[233].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[247].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[250].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[253].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[256].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[260].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[264].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[267].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[292])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[294])
        Sick_Leave = pd.to_numeric(pdf_text_words[299])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[301])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    va_dc_adj_ext.append(innerlist)

# Create Dataframe from list
va_dc_adj_df = pd.DataFrame(va_dc_adj_ext, columns=df_columns)

" ############################################ ELS - VA DC Award (2019) ############################################## "
# August 2019
# VA and DC state income tax
# With health insurance
# Award

" Single PDF "

# Import single PDF
va_dc_award_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - VA DC "
                                         "Award/els-08_31_2019 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
va_dc_award_single_text = va_dc_award_single_pdf.pages[0].extract_text()
# Convert string to list
va_dc_award_single_list = list(va_dc_award_single_text.split())
# Dataframe from list
va_dc_award_single_df = pd.DataFrame(va_dc_award_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
va_dc_award_folder = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2019 - VA DC Award/*.pdf"))

# Create blank list to store extracted PDF text
va_dc_award_ext = []

# Loop through each PDF in folder
for file in va_dc_award_folder:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[174].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[190].replace(",", ""), errors='coerce')
        State_Tax_VA = pd.to_numeric(pdf_text_words[182].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[197].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[200].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[205].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[211].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[216].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[221].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[226].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[239].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[245].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[248].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[252].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[256].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[259].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[284])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[286])
        Sick_Leave = pd.to_numeric(pdf_text_words[292])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[294])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    va_dc_award_ext.append(innerlist)

# Create Dataframe from list
va_dc_award_df = pd.DataFrame(va_dc_award_ext, columns=df_columns)

" ################################################# ELS - VA (2020) ################################################## "
# January-February 2020
# Virginia

" Single PDF "

# Import single PDF
va_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - VA/els-02_29_2020 - "
                                "Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
va_single_text = va_single_pdf.pages[0].extract_text()
# Convert string to list
va_single_list = list(va_single_text.split())
# Dataframe from list
va_single_df = pd.DataFrame(va_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
va_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - VA/*.pdf"))

# Create blank list to store extracted PDF text
va_data = []

# Loop through each PDF in folder
for file in va_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[165].replace(",", ""), errors='coerce')
        State_Tax_DC = 0
        State_Tax_VA = pd.to_numeric(pdf_text_words[173].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[180].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[183].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[188].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[194].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[199].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[204].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[209].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[222].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[225].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[228].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[231].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[235].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[239].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[267])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[269])
        Sick_Leave = pd.to_numeric(pdf_text_words[274].replace(",", ""), errors='coerce')
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[276])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    va_data.append(innerlist)

# Create Dataframe from list
va_df = pd.DataFrame(va_data, columns=df_columns)

# Spot fixes
# va_df.loc[3, 'Sick_Leave'] = 112
# va_df.loc[3, 'Sick_Leave_Earned'] = 4

" ############################################### ELS - DC VA (2020) ################################################# "
# March 2020
# Virginia and DC

" Single PDF "

# Import single PDF
dc_va_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC "
                                   "VA/els-03_14_2020 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
dc_va_single_text = dc_va_single_pdf.pages[0].extract_text()
# Convert string to list
dc_va_single_list = list(dc_va_single_text.split())
# Dataframe from list
dc_va_single_df = pd.DataFrame(dc_va_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
dc_va_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC VA/*.pdf"))

# Create blank list to store extracted PDF text
dc_va_data = []

# Loop through each PDF in folder
for file in dc_va_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[172].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[180].replace(",", ""), errors='coerce')
        State_Tax_VA = pd.to_numeric(pdf_text_words[188].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[195].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[198].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[203].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[209].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[214].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[219].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[224].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[237].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[240].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[243].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[246].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[250].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[254].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[257].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[282])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[284])
        Sick_Leave = pd.to_numeric(pdf_text_words[289].replace(",", ""), errors='coerce')
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[291])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    dc_va_data.append(innerlist)

# Create Dataframe from list
dc_va_df = pd.DataFrame(dc_va_data, columns=df_columns)

" ############################################ ELS - DC VA Award (2020) ############################################## "
# September 2020
# DC and VA state income tax
# With health insurance
# Award

" Single PDF "

# Import single PDF
dc_va_award_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC VA "
                                         "Award/els-09_12_2020 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
dc_va_award_single_text = dc_va_award_single_pdf.pages[0].extract_text()
# Convert string to list
dc_va_award_single_list = list(dc_va_award_single_text.split())
# Dataframe from list
dc_va_award_single_df = pd.DataFrame(dc_va_award_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
dc_va_award_folder = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC VA Award/*.pdf"))

# Create blank list to store extracted PDF text
dc_va_award_ext = []

# Loop through each PDF in folder
for file in dc_va_award_folder:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[113].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[122].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[175].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[183].replace(",", ""), errors='coerce')
        State_Tax_VA = pd.to_numeric(pdf_text_words[191].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[198].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[201].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[206].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[212].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[217].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[222].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[227].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[240].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[243].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[246].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[249].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[253].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[257].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[260].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[285])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[287])
        Sick_Leave = pd.to_numeric(pdf_text_words[294])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[296])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    dc_va_award_ext.append(innerlist)

# Create Dataframe from list
dc_va_award_df = pd.DataFrame(dc_va_award_ext, columns=df_columns)

" ############################################## ELS - DC VA TSP (2020) ############################################## "
# March 2020
# Virginia and DC
# Switch from TSP contribution of 10% to $750

" Single PDF "

# Import single PDF
dc_va_tsp_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC VA "
                                       "TSP/els-10_24_2020 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
dc_va_tsp_single_text = dc_va_tsp_single_pdf.pages[0].extract_text()
# Convert string to list
dc_va_tsp_single_list = list(dc_va_tsp_single_text.split())
# Dataframe from list
dc_va_tsp_single_df = pd.DataFrame(dc_va_tsp_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
dc_va_tsp_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC VA TSP/*.pdf"))

# Create blank list to store extracted PDF text
dc_va_tsp_data = []

# Loop through each PDF in folder
for file in dc_va_tsp_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[112].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[121].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[171].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[179].replace(",", ""), errors='coerce')
        State_Tax_VA = pd.to_numeric(pdf_text_words[187].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[194].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[197].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[202].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[208].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[213].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[218].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[223].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[236].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[239].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[245].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[249].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[253].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[256].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[281])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[283])
        Sick_Leave = pd.to_numeric(pdf_text_words[289])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[291])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    dc_va_tsp_data.append(innerlist)

# Create Dataframe from list
dc_va_tsp_df = pd.DataFrame(dc_va_tsp_data, columns=df_columns)

" ############################################# ELS - DC VA Leave (2020) ############################################# "
# March 2020
# Virginia and DC
# Used annual/sick leave

" Single PDF "

# Import single PDF
dc_va_leave_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC VA "
                                         "Leave/els-12_05_2020 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
dc_va_leave_single_text = dc_va_leave_single_pdf.pages[0].extract_text()
# Convert string to list
dc_va_leave_single_list = list(dc_va_leave_single_text.split())
# Dataframe from list
dc_va_leave_single_df = pd.DataFrame(dc_va_leave_single_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
dc_va_leave_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/2020 - DC VA Leave/*.pdf"))

# Create blank list to store extracted PDF text
dc_va_leave_data = []

# Loop through each PDF in folder
for file in dc_va_leave_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[112].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[121].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[171].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[179].replace(",", ""), errors='coerce')
        State_Tax_VA = pd.to_numeric(pdf_text_words[187].replace(",", ""), errors='coerce')
        Health_Benefits = pd.to_numeric(pdf_text_words[194].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[197].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[202].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[208].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[213].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[218].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[223].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[236].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[239].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[245].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[249].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[253].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[256].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[281])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[283])
        Sick_Leave = pd.to_numeric(pdf_text_words[290])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[292])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    dc_va_leave_data.append(innerlist)

# Create Dataframe from list
dc_va_leave_df = pd.DataFrame(dc_va_leave_data, columns=df_columns)

" ############################################### ELS - Default Leave ################################################ "
# 2021
# DC
# Leave

" Single PDF "

# Import single PDF
default_leave_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/Default Leave/"
                                           "els-01_02_2021 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
default_leave_single_pdf_text = default_leave_single_pdf.pages[0].extract_text()
# Convert string to list
default_leave_single_pdf_list = list(default_leave_single_pdf_text.split())
# Dataframe from list; Use to determine item number
default_leave_single_pdf_df = pd.DataFrame(default_leave_single_pdf_list, columns=["Field"])

" Read Multiple PDFs "

# Call folders of PDFs
default_leave_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/Default Leave/*.pdf"))

# Create blank list to store extracted PDF text
default_leave_data = []

# Loop through each PDF in folder
for file in default_leave_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[112].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[121].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[165].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[173].replace(",", ""), errors='coerce')
        State_Tax_VA = 0
        Health_Benefits = pd.to_numeric(pdf_text_words[180].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[183].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[188].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[194].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[199].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[204].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[209].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[222].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[225].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[228].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[231].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[235].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[239].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[267])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[269])
        Sick_Leave = pd.to_numeric(pdf_text_words[276])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[278])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    default_leave_data.append(innerlist)

# Create Dataframe from list
default_leave_df = pd.DataFrame(default_leave_data, columns=df_columns)

" ################################################## ELS - Default ################################################### "
# 2021
# DC

" Single PDF "

# Import single PDF
default_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/Default/"
                                     "els-01_16_2021 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
default_single_pdf_text = default_single_pdf.pages[0].extract_text()
# Convert string to list
default_single_pdf_list = list(default_single_pdf_text.split())
# Dataframe from list
default_single_pdf_df = pd.DataFrame(default_single_pdf_list, columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
default_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/Default/*.pdf"))

# Create blank list to store extracted PDF text
default_data = []

# Loop through each PDF in folder
for file in default_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[112].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[121].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[165].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[173].replace(",", ""), errors='coerce')
        State_Tax_VA = 0
        Health_Benefits = pd.to_numeric(pdf_text_words[180].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[183].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[188].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[194].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[199].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[204].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[209].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[222].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[225].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[228].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[231].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[235].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[239].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[267])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[269])
        Sick_Leave = pd.to_numeric(pdf_text_words[274])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[276])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    default_data.append(innerlist)

# Create Dataframe from list
default_df = pd.DataFrame(default_data, columns=df_columns)

" ############################################### ELS - Default Award ################################################ "
# 2021
# DC
# Annual award

" Single PDF "

# Import single PDF
default_award_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/Default "
                                           "Award/els-07_31_2021 - Federal Energy Regulatory Commission.pdf")
# Extract text frpm PDF
default_award_single_pdf_text = default_award_single_pdf.pages[0].extract_text()
# Convert string to list
default_award_single_pdf_list = list(default_award_single_pdf_text.split())
# Dataframe from list; Use to determine item number
default_award_single_pdf_df = pd.DataFrame(default_award_single_pdf_list, columns=["Field"])

" Read Multiple PDFs "

# Call folders of PDFs
default_award_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/Default Award/*.pdf"))

# Create blank list to store extracted PDF text
default_award_data = []

# Loop through each PDF in folder
for file in default_award_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[112].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[121].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[168].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[176].replace(",", ""), errors='coerce')
        State_Tax_VA = 0
        Health_Benefits = pd.to_numeric(pdf_text_words[183].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[186].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[191].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[197].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[202].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[207].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[212].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[225].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[228].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[231].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[234].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[238].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[242].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[245].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[270])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[272])
        Sick_Leave = pd.to_numeric(pdf_text_words[279])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[281])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    default_award_data.append(innerlist)

# Create Dataframe from list
default_award_df = pd.DataFrame(default_award_data, columns=df_columns)

" ############################################ ELS - Default OASDI Award ############################################# "
# 2021
# DC
# Award
# OASDI deferred tax

" Single PDF "

# Import single PDF
default_oasdi_award_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/Default "
                                            "OASDI Award/els-08_14_2021 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
default_oasdi_award_single_pdf_text = default_oasdi_award_single_pdf.pages[0].extract_text()
# Convert string to list
default_oasdi_award_single_pdf_list = list(default_oasdi_award_single_pdf_text.split())
# Dataframe from list
default_oasdi_award_single_pdf_df = pd.DataFrame(default_oasdi_award_single_pdf_list,
                                                 columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
default_oasdi_award_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/Default OASDI Award"
                                       "/*.pdf"))

# Create blank list to store extracted PDF text
default_oasdi_award_data = []

# Loop through each PDF in folder
for file in default_oasdi_award_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[112].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[121].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[168].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[176].replace(",", ""), errors='coerce')
        State_Tax_VA = 0
        Health_Benefits = pd.to_numeric(pdf_text_words[183].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[186].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[191].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[197].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[202].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[213].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[218].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[231].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[234].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[237].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[240].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[244].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[248].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[251].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[276])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[278])
        Sick_Leave = pd.to_numeric(pdf_text_words[284])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[286])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    default_oasdi_award_data.append(innerlist)

# Create Dataframe from list
default_oasdi_award_df = pd.DataFrame(default_oasdi_award_data, columns=df_columns)

" ############################################### ELS - Default OASDI ################################################ "
# 2021
# DC
# OASDI deferred tax

" Single PDF "

# Import single PDF
default_oasdi_single_pdf = pdfplumber.open("/Users/jeff/Documents/Python Projects/Earnings Statements/Default "
                                           "OASDI/els-08_28_2021 - Federal Energy Regulatory Commission.pdf")
# Extract text from PDF
default_oasdi_single_pdf_text = default_oasdi_single_pdf.pages[0].extract_text()
# Convert string to list
default_oasdi_single_pdf_list = list(default_oasdi_single_pdf_text.split())
# Dataframe from list
default_oasdi_single_pdf_df = pd.DataFrame(default_oasdi_single_pdf_list,
                                           columns=["Field"])  # Use to determine item number

" Read Multiple PDFs "

# Call folders of PDFs
default_oasdi_files = (glob.glob("/Users/jeff/Documents/Python Projects/Earnings Statements/Default OASDI/*.pdf"))

# Create blank list to store extracted PDF text
default_oasdi_data = []

# Loop through each PDF in folder
for file in default_oasdi_files:
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]

        # Extract text as string
        pdf_text = page.extract_text()
        pdf_text_words = pdf_text.split()
        print(pdf_text_words)

        # Extract specific data
        Agency = "Federal Energy Regulatory Commission"
        Pay_Period_Ending = pd.to_datetime(pdf_text_words[10])
        Net_Pay = pd.to_numeric(pdf_text_words[12].replace(",", ""), errors='coerce')
        Pay_Period = pd.to_numeric(pdf_text_words[22])
        Pay_Date = pd.to_datetime(pdf_text_words[23])
        Plan = pdf_text_words[33]
        Grade = pd.to_numeric(pdf_text_words[34])
        Step = pd.to_numeric(pdf_text_words[35])
        Annual_Salary = pd.to_numeric(pdf_text_words[37].replace(",", ""), errors='coerce')
        Hourly_Rate = pd.to_numeric(pdf_text_words[39].replace(",", ""), errors='coerce')
        Gross_Pay = pd.to_numeric(pdf_text_words[112].replace(",", ""), errors='coerce')
        Total_Deductions = pd.to_numeric(pdf_text_words[121].replace(",", ""), errors='coerce')
        Federal_Taxes = pd.to_numeric(pdf_text_words[165].replace(",", ""), errors='coerce')
        State_Tax_DC = pd.to_numeric(pdf_text_words[173].replace(",", ""), errors='coerce')
        State_Tax_VA = 0
        Health_Benefits = pd.to_numeric(pdf_text_words[180].replace(",", ""), errors='coerce')
        Dental_Vision = pd.to_numeric(pdf_text_words[183].replace(",", ""), errors='coerce')
        TSP = pd.to_numeric(pdf_text_words[188].replace(",", ""), errors='coerce')
        Retirement_FERS = pd.to_numeric(pdf_text_words[194].replace(",", ""), errors='coerce')
        OASDI_Tax = pd.to_numeric(pdf_text_words[199].replace(",", ""), errors='coerce') + pd.to_numeric(
            pdf_text_words[204].replace(",", ""), errors='coerce')
        Medicare_Tax = pd.to_numeric(pdf_text_words[210].replace(",", ""), errors='coerce')
        FEGLI_Regular = pd.to_numeric(pdf_text_words[215].replace(",", ""), errors='coerce')
        Gov_FEGLI = pd.to_numeric(pdf_text_words[229].replace(",", ""), errors='coerce')
        Gov_FEHB = pd.to_numeric(pdf_text_words[231].replace(",", ""), errors='coerce')
        Gov_Medicare = pd.to_numeric(pdf_text_words[234].replace(",", ""), errors='coerce')
        Gov_OASDI = pd.to_numeric(pdf_text_words[237].replace(",", ""), errors='coerce')
        Gov_TSP_Basic = pd.to_numeric(pdf_text_words[241].replace(",", ""), errors='coerce')
        Gov_TSP_Matching = pd.to_numeric(pdf_text_words[245].replace(",", ""), errors='coerce')
        Gov_FERS = pd.to_numeric(pdf_text_words[248].replace(",", ""), errors='coerce')
        Annual_Leave = pd.to_numeric(pdf_text_words[273])
        Annual_Leave_Earned = pd.to_numeric(pdf_text_words[275])
        Sick_Leave = pd.to_numeric(pdf_text_words[245])
        Sick_Leave_Earned = pd.to_numeric(pdf_text_words[283])
        Time_Off_Award = 0

    # Assign each section of strings for a single pds to a list
    innerlist = [Agency, Pay_Period_Ending, Net_Pay, Pay_Period, Pay_Date, Plan, Grade, Step, Annual_Salary,
                 Hourly_Rate, Gross_Pay, Total_Deductions, Federal_Taxes, State_Tax_DC, State_Tax_VA, Health_Benefits,
                 Dental_Vision, TSP, Retirement_FERS, OASDI_Tax, Medicare_Tax, FEGLI_Regular, Gov_FEGLI, Gov_FEHB,
                 Gov_Medicare, Gov_OASDI, Gov_TSP_Basic, Gov_TSP_Matching, Gov_FERS, Annual_Leave,
                 Annual_Leave_Earned]
    # Sick_Leave, Sick_Leave_Earned, Time_Off_Award

    # Append each list to the outer list
    default_oasdi_data.append(innerlist)

# Create Dataframe from list
default_oasdi_df = pd.DataFrame(default_oasdi_data, columns=df_columns)

" ################################################ Concatenate ELS ################################################### "

els_merge = pd.concat([no_health_df, health_df, va_dc_df, va_dc_adj_df, va_dc_award_df, va_df, dc_va_df, dc_va_award_df,
                       dc_va_tsp_df, dc_va_leave_df, default_leave_df, default_df, default_award_df,
                       default_oasdi_award_df, default_oasdi_df], ignore_index=True)

# Sort by Pay Period
els_merge = els_merge.sort_values(by='Pay_Period_Ending').reset_index(drop=True)

# Print
print(tabulate(els_merge, headers='keys', tablefmt='plain'))

# Export
# els_merge.to_csv("ELS Master.csv", index=False)

" Analysis "

# Extract year
els_merge['Transaction Date DT'] = pd.to_datetime(els_merge['Pay_Period_Ending'])
els_merge["Year"] = els_merge["Transaction Date DT"].dt.year

# Sum by category and year
els_cat_annual = els_merge.groupby(['Year'])['Annual_Salary', 'Gross_Pay', 'Net_Pay', 'Total_Deductions',
                                             'Federal_Taxes', 'State_Tax_DC', 'State_Tax_VA', 'Health_Benefits',
                                             'Dental_Vision', 'TSP', 'Retirement_FERS', 'OASDI_Tax', 'Medicare_Tax',
                                             'FEGLI_Regular'].sum().reset_index()

# Transpose
els_cat_annual_long = pd.melt(els_cat_annual,
                              id_vars=['Year'],  # These variable are not pivoted; can use a list of variables here
                              value_vars=['Annual_Salary', 'Gross_Pay', 'Net_Pay', 'Total_Deductions', 'Federal_Taxes',
                                          'State_Tax_DC',
                                          'State_Tax_VA', 'Health_Benefits', 'Dental_Vision', 'TSP', 'Retirement_FERS',
                                          'OASDI_Tax',
                                          'Medicare_Tax', 'FEGLI_Regular'],  # These variables are pivoted
                              value_name='Amount'  # Rename
                              )

" Reassign Categories "

# Rename field name
els_cat_annual_long.rename(columns={'variable': 'Item'}, inplace=True)

els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Annual_Salary', 'Category'] = 'Salary'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Gross_Pay', 'Category'] = 'Gross Pay'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Net_Pay', 'Category'] = 'Net Pay'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Federal_Taxes', 'Category'] = 'Taxes'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'State_Tax_DC', 'Category'] = 'Taxes'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'State_Tax_VA', 'Category'] = 'Taxes'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Health_Benefits', 'Category'] = 'Health Insurance'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Dental_Vision', 'Category'] = 'Health Insurance'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'TSP', 'Category'] = 'Retirement'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Retirement_FERS', 'Category'] = 'Retirement'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'OASDI_Tax', 'Category'] = 'Taxes'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Medicare_Tax', 'Category'] = 'Taxes'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'FEGLI_Regular', 'Category'] = 'Retirement'
els_cat_annual_long.loc[els_cat_annual_long['Item'] == 'Total_Deductions', 'Category'] = 'Total Deductions'

print(tabulate(els_cat_annual_long, headers='keys', tablefmt='plain'))

" #################################################### Expenses ###################################################### "
# TODO: add AMEX charges.

# From Chase statements

" Import CSV "

# 2020
freedom_unlimited_2020 = pd.read_csv("/Users/jeff/Documents/Python/Python Projects/Expenses/Chase4715_Activity_2020.CSV")

freedom_2020 = pd.read_csv("/Users/jeff/Documents/Python/Python Projects/Expenses/Chase4715_Activity_2020.CSV")

" Concat Credit Card Statements "
expenses_concat = pd.concat([freedom_unlimited_2020, freedom_2020], ignore_index=True)

" Extract year "
expenses_concat['Transaction Date'] = pd.to_datetime(expenses_concat['Transaction Date'])
expenses_concat['Post Date'] = pd.to_datetime(expenses_concat['Post Date'])
expenses_concat["Year"] = expenses_concat["Transaction Date"].dt.year

" Rearrange "
expenses_concat = expenses_concat[['Transaction Date', 'Year', 'Post Date', 'Description', 'Category', 'Type', 'Amount', 'Memo']]
expenses_concat.dtypes
expenses_concat.head()

# Export
# expenses_concat.to_csv("Expenses Master.csv", index=False)

" Positive / Negative "

# Show unique type of transactions 
pd.DataFrame(expenses_concat["Type"].unique())

# Positive values for Sales and Adjustments
expenses_concat['Amount'] = expenses_concat['Amount'].abs()
# Negative values for Returns
expenses_concat.loc[expenses_concat.Type == 'Return', 'Amount'] = expenses_concat['Amount'] * -1

" Categories "

# Filter by categories
pd.DataFrame(expenses_concat["Category"].unique())

# View entries in each category to validate names for consistency
food_drink = expenses_concat.loc[(expenses_concat['Category'] == 'Food & Drink')]
food_drink = food_drink.sort_values(by='Transaction Date')
print(tabulate(food_drink, headers='keys', tablefmt='plain'))

health = expenses_concat.loc[(expenses_concat['Category'] == 'Health & Wellness')]
health = health.sort_values(by='Description')
print(tabulate(health, headers='keys', tablefmt='plain'))

home = expenses_concat.loc[(expenses_concat['Category'] == 'Home')]
home = home.sort_values(by='Description')
print(tabulate(home, headers='keys', tablefmt='plain'))

shopping = expenses_concat.loc[(expenses_concat['Category'] == 'Shopping')]
shopping = shopping.sort_values(by='Description')
print(tabulate(shopping, headers='keys', tablefmt='plain'))

groceries = expenses_concat.loc[(expenses_concat['Category'] == 'Groceries')]
groceries = groceries.sort_values(by='Description')
print(tabulate(groceries, headers='keys', tablefmt='plain'))

personal = expenses_concat.loc[(expenses_concat['Category'] == 'Personal')]
personal = personal.sort_values(by='Description')
print(tabulate(personal, headers='keys', tablefmt='plain'))

gas = expenses_concat.loc[(expenses_concat['Category'] == 'Gas')]
gas = gas.sort_values(by='Description')
print(tabulate(gas, headers='keys', tablefmt='plain'))

travel = expenses_concat.loc[(expenses_concat['Category'] == 'Travel')]
travel = travel.sort_values(by='Description')
print(tabulate(travel, headers='keys', tablefmt='plain'))

utilities = expenses_concat.loc[(expenses_concat['Category'] == 'Bills & Utilities')]
utilities = utilities.sort_values(by='Description')
print(tabulate(utilities, headers='keys', tablefmt='plain'))

donations = expenses_concat.loc[(expenses_concat['Category'] == 'Gifts & Donations')]
donations = donations.sort_values(by='Description')
print(tabulate(donations, headers='keys', tablefmt='plain'))

education = expenses_concat.loc[(expenses_concat['Category'] == 'Education')]
education = education.sort_values(by='Description')
print(tabulate(education, headers='keys', tablefmt='plain'))

entertainment = expenses_concat.loc[(expenses_concat['Category'] == 'Entertainment')]
entertainment = entertainment.sort_values(by='Description')
print(tabulate(entertainment, headers='keys', tablefmt='plain'))

# Re-categorize business names

# Shopping
expenses_concat.loc[expenses_concat.Description == "WWW COSTCO COM", 'Category'] = "Groceries"

# Home
expenses_concat.loc[expenses_concat.Description == "FRAGERS", 'Category'] = "Shopping"
expenses_concat.loc[expenses_concat.Description == "GINKGO GARDENS", 'Category'] = "Shopping"
expenses_concat.loc[expenses_concat.Description == "MERRIFIELD GC", 'Category'] = "Shopping"

# Personal
expenses_concat.loc[expenses_concat.Description == "WHITE HOUSE HSTRCL ASSOC", 'Category'] = "Shopping"

# Utilities
expenses_concat.loc[expenses_concat.Description == "Amazon Prime*MF4YL2E90", 'Category'] = "Shopping"
expenses_concat.loc[expenses_concat.Description == "IDENTOGO-IDEMIA TSA PRECH", 'Category'] = "Travel"
expenses_concat.loc[expenses_concat.Description == "WA VEHICLE LICENSING", 'Category'] = "Travel"

# Education
expenses_concat.loc[expenses_concat.Description == "THE NC ARBORETUM", 'Category'] = "Entertainment"

# Entertainment
expenses_concat.loc[expenses_concat.Description == "NIELSON WINES", 'Category'] = "Food & Drink"

" Add rent from 2020 "
new_row_rent_2020_a = {'Transaction Date': '01/01/2020', 'Post Date': '', 'Description': '1800 Oak', 'Category': 'Rent',
                       'Type': 'Sale', 'Amount': 1246.50, 'Memo': '', 'Transaction Date DT': '2020-01-01 00:00:00',
                       'Year': 2020, 'Month': 1}
new_row_rent_2020_b = {'Transaction Date': '02/01/2020', 'Post Date': '', 'Description': '1800 Oak', 'Category': 'Rent',
                       'Type': 'Sale', 'Amount': 773.69, 'Memo': '', 'Transaction Date DT': '2020-02-01 00:00:00',
                       'Year': 2020, 'Month': 2}
expenses_concat = expenses_concat.append(new_row_rent_2020_a, ignore_index=True)
expenses_concat = expenses_concat.append(new_row_rent_2020_b, ignore_index=True)

# Print
print(tabulate(expenses_concat, headers='keys', tablefmt='plain'))

" Analysis "

# Drop Payment transactions
expenses_master = expenses_concat.loc[(expenses_concat['Type'] == 'Adjustment') | (expenses_concat['Type'] == 'Sale')
                                      | (expenses_concat['Type'] == 'Return')]

" Sum by category and year "
cat_annual = expenses_master.groupby(['Year', 'Category'])['Amount'].sum().reset_index()
print(tabulate(cat_annual, headers='keys', tablefmt='plain'))

" Assign Categories "

# Rename field name
cat_annual.rename(columns={'Category': 'Item'}, inplace=True)
cat_annual['Category'] = 'Expenses'

" ########################################### Concatenate ELS and Expenses ########################################### "

# Concatenate
els_master = pd.concat([els_cat_annual_long, cat_annual], ignore_index=True)

# Sort
els_master = els_master.sort_values(by=['Year', 'Category', 'Item'])

# Rearrange columns
els_master = els_master[['Year', 'Category', 'Item', 'Amount']]

# Print
print(tabulate(els_master, headers='keys', tablefmt='plain'))

# Export
# els_master.to_csv("Expenses Summary.csv", index=False)
# TODO: Create redacted version for GitHub?


" #################################################### Analysis ###################################################### "

# Sum by year
els_sum = els_master.groupby(['Year', 'Category'])['Amount'].sum().reset_index()
print(tabulate(els_sum, headers='keys', tablefmt='plain'))
# Gross pay and total deduction values are correct. Net Pay for some reason is incorrect.




# Source
# https://stackoverflow.com/questions/63093234/how-to-open-multiple-files-in-pdfplumber
