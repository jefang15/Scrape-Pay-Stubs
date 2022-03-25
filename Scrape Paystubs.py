""" Scraping Text from Pay Stubs """

import glob
import pdfplumber
import pandas as pd
from tabulate import tabulate


" Create function that scrapes information from pay stubs and accounts for occasional differences between PDFs "


def scrape_pay_stubs(folder):
    out = []  # Empty list to store information from all PDFs
    for file in folder:
        with pdfplumber.open(file) as one_pdf:
            string = ''
            for i in range(0, len(one_pdf.pages)):
                string += one_pdf.pages[i].extract_text().replace('\n', '<end>')  # Write each page of single PDF to empty string
                # Keeps <end> as indicator for end of each line of string

            inner = []

            " General Information and Leave "

            # TODO: Add annual leave used current throughout
            # TODO: Add 'Time Off Award Earned Current: ' throughout
            keywords = [
                'Pay Period Ending : ',
                'Net Pay $ : ',
                'Pay Period # : ',
                'Pay Date : ',
                'Pay Plan : ',
                'Pay Grade : ',
                'Pay Step : ',
                'Annual Salary $ : ',
                'Hourly Rate $ : ',
                'YTD Wages: ',
                'Gross Pay YTD: ',
                'Total Deductions YTD: ',
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
                if i in string:  # If statement because certain keywords do not appear in each PDF
                    inner.append(string[(string.find(i) + len(i)):(string.find('<end>', string.find(i)))])
                else:
                    inner.append('')
            # string.find(i) - returns index position of the first appearance of the keyword
            # len(i) - returns length of keyword string; to get to the index number at the end of the entire keyword
            # string.find('<end>', string.find(i)) - returns index when <end> appears, starting at the keyword index
            # string[(string.find(i) + len(i)):(string.find('<end>', string.find(i)))] - returns desired value based on index

            # Other Award
            if 'Other Award' in string:
                other_award_substring = string[string.find('Other Award'):]
                inner.append(other_award_substring[
                             other_award_substring.find('Adj Hours | ') + len('Adj Hours | '):other_award_substring.find(
                                 ' Current PPD')])
            else:
                inner.append(0)

            # Home Address
            inner.append(string[(string.find('Home Address') + len('Home Address') + len('<end>')):(string.find('Pay Check',
                                                                                                                string.find(
                                                                                                                    'Home Address'))) - len(
                '<end>')])

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
                deductions_substring = string[string.find(i):]
                if i in string:
                    # Federal Taxes Adjusted
                    inner.append(string[(string.find(i) + len(i)):(string.find('Adjusted', string.find(i)))])
                else:
                    inner.append(0)

                if i in string:
                    # Federal Taxes Current
                    inner.append(deductions_substring[(deductions_substring.find('Misc | ') + len('Misc | ')):(
                        deductions_substring.find('Current', deductions_substring.find('Misc | ')))])
                else:
                    inner.append(0)

                if i in string:
                    # Federal Taxes YTD
                    inner.append(deductions_substring[(deductions_substring.find('Current PPD | ') + len('Current PPD | ')):(
                        deductions_substring.find(' YTD', deductions_substring.find('Current PPD | ')))])
                else:
                    inner.append(0)

            " Basic Info "

            keywords3 = [
                'Service Comp Date',
                'Agency',
                'Cumulative Retirement Agency $',
                'Duty Station',
                'Pay Begin Date',
                'Financial Institution',
                'TSP Tax Deferred Amt/%'
                ]

            for i in keywords3:
                inner.append(string[(string.find(i) + len(i)):(string.find(':', string.find(i)))])

            " Benefits "

            benefits_substring = string[string.find('Benefits Paid by Government'):]

            keywords4 = [
                'FEGLI',
                'Medicare',
                'OASDI',
                'TSP Basic',
                'TSP Matching',
                'FERS/FRAE'
                ]

            for i in keywords4:
                # Benefits Current
                inner.append(benefits_substring[
                             (benefits_substring.find(i) + len(i)):(
                                 benefits_substring.find(' Current', benefits_substring.find(i)))])

                # Benefits YTD
                inner.append(benefits_substring[(benefits_substring.find('Current PPD | ') + len('Current PPD | ')):(
                    benefits_substring.find(' YTD', benefits_substring.find('Current PPD | ')))])

            " Append all scraped values from inner list to outer list "
            out.append(inner)
    return out


" Open Folder with All Pay Stubs "
pay_stubs_folder = (glob.glob('Projects/Scrape-Paystubs/FERC - Earnings & Leave Statements/*.pdf'))

" Apply Function to Folder "
scraped_data = scrape_pay_stubs(pay_stubs_folder)

" Create DataFrame "
headings = [
    'Pay Period Ending',
    'Net Pay',
    'Pay Period',
    'Pay Date',
    'Pay Plan',
    'Pay Grade',
    'Pay Step',
    'Annual Salary',
    'Hourly Rate',
    'YTD Wages',
    'Gross Pay YTD',
    'Total Deductions YTD',
    'Maximum Carry Over',
    'Use Or Lose Balance',
    'Annual Leave Begin Balance',
    'Annual Leave Begin Balance Leave Year',
    'Annual Leave Earned',
    'Annual Leave Earned YTD',
    'Annual Leave Advanced',
    'Annual Leave Total',
    'Sick Leave Begin Balance',
    'Sick Leave Begin Balance Leave Year',
    'Sick Leave Earned',
    'Sick Leave Total',
    'Sick Leave Used',
    'Sick Leave Used YTD',
    'Sick Leave Advanced',
    'Sick Leave Ending Balance',
    'Time Off Award Begin Balance',
    'Time Off Award Begin Balance Leave Year',
    'Time Off Award Advanced',
    'Time Off Award Ending Balance',
    'Other Award',
    'Home Address',
    'Federal Taxes Adjusted',
    'Federal Taxes',
    'Federal Taxes YTD',
    'State Tax 1 ( DC ) Adjusted',
    'State Tax 1 ( DC )',
    'State Tax 1 ( DC ) YTD',
    'State Tax 1 ( VA ) Adjusted',
    'State Tax 1 ( VA )',
    'State Tax 1 ( VA ) YTD',
    'State Tax 2 ( DC ) Adjusted',
    'State Tax 2 ( DC )',
    'State Tax 2 ( DC ) YTD',
    'Health Benefits Adjusted',
    'Health Benefits',
    'Health Benefits YTD',
    'Dental/Vision Adjusted',
    'Dental/Vision',
    'Dental/Vision YTD',
    'TSP Tax Deferred Adjusted',
    'TSP Tax Deferred',
    'TSP Tax Deferred YTD',
    'Retirement - FERS/FRAE Adjusted',
    'Retirement - FERS/FRAE',
    'Retirement - FERS/FRAE YTD',
    'OASDI Tax Adjusted',
    'OASDI Tax',
    'OASDI Tax YTD',
    'Medicare Tax Adjusted',
    'Medicare Tax',
    'Medicare Tax YTD',
    'FEGLI - Regular Adjusted',
    'FEGLI - Regular',
    'FEGLI - Regular YTD',
    'Service Comp Date',
    'Agency',
    'Cumulative Retirement Agency',
    'Duty Station',
    'Pay Begin Date',
    'Financial Institution',
    'TSP Tax Deferred Amt',
    'FEGLI',
    'FEGLI YTD',
    'Medicare',
    'Medicare YTD',
    'OASDI',
    'OASDI YTD',
    'TSP Basic',
    'TSP Basic YTD',
    'TSP Matching',
    'TSP Matching YTD',
    'FERS/FRAE',
    'FERS/FRAE YTD'
    ]

df_scraped = pd.DataFrame(scraped_data, columns=headings)

" Clean Data "

# Convert Data Types
df_clean = df_scraped.copy()
print(df_clean.dtypes)

var_to_datetime = [
    'Pay Period Ending', 'Pay Date', 'Service Comp Date', 'Pay Begin Date'
    ]
df_clean[var_to_datetime] = df_clean[var_to_datetime].apply(pd.to_datetime)

var_to_int = [
    'Pay Period', 'Pay Grade', 'Pay Step', 'Maximum Carry Over', 'Use Or Lose Balance', 'Annual Leave Begin Balance',
    'Annual Leave Begin Balance Leave Year', 'Annual Leave Earned', 'Annual Leave Earned YTD', 'Annual Leave Advanced',
    'Annual Leave Total', 'Sick Leave Begin Balance', 'Sick Leave Begin Balance Leave Year', 'Sick Leave Earned',
    'Sick Leave Total', 'Sick Leave Used', 'Sick Leave Used YTD', 'Sick Leave Advanced', 'Sick Leave Ending Balance',
    'Time Off Award Begin Balance', 'Time Off Award Begin Balance Leave Year', 'Time Off Award Advanced',
    'Time Off Award Ending Balance'
    ]
df_clean[var_to_int] = df_clean[var_to_int].apply(pd.to_numeric).fillna(0).astype(int)

var_to_float = [
    'Net Pay', 'Annual Salary', 'Hourly Rate', 'YTD Wages', 'Gross Pay YTD', 'Total Deductions YTD', 'Federal Taxes Adjusted',
    'Other Award', 'Federal Taxes', 'Federal Taxes YTD', 'State Tax 1 ( DC ) Adjusted', 'State Tax 1 ( DC )',
    'State Tax 1 ( DC ) YTD', 'State Tax 1 ( VA ) Adjusted', 'State Tax 1 ( VA )', 'State Tax 1 ( VA ) YTD',
    'State Tax 2 ( DC ) Adjusted', 'State Tax 2 ( DC )', 'State Tax 2 ( DC ) YTD', 'Health Benefits Adjusted',
    'Health Benefits', 'Health Benefits YTD', 'Dental/Vision Adjusted', 'Dental/Vision', 'Dental/Vision YTD',
    'TSP Tax Deferred Adjusted', 'TSP Tax Deferred', 'TSP Tax Deferred YTD', 'Retirement - FERS/FRAE Adjusted',
    'Retirement - FERS/FRAE', 'Retirement - FERS/FRAE YTD', 'OASDI Tax Adjusted', 'OASDI Tax', 'OASDI Tax YTD',
    'Medicare Tax Adjusted', 'Medicare Tax', 'Medicare Tax YTD', 'FEGLI - Regular Adjusted', 'FEGLI - Regular',
    'FEGLI - Regular YTD', 'Cumulative Retirement Agency', 'FEGLI', 'FEGLI YTD', 'Medicare', 'Medicare YTD', 'OASDI',
    'OASDI YTD', 'TSP Basic', 'TSP Basic YTD', 'TSP Matching', 'TSP Matching YTD', 'FERS/FRAE', 'FERS/FRAE YTD'
    ]
df_clean[var_to_float] = df_clean[var_to_float].replace(',', '', regex=True).apply(pd.to_numeric, errors='coerce').fillna(0)

# Clean up
df_clean['TSP Tax Deferred Amt'] = df_clean['TSP Tax Deferred Amt'].replace(' ', '', regex=True)
df_clean['Home Address'] = df_clean['Home Address'].replace('<end>', '', regex=True)

# Sort
df_sort = df_clean.sort_values(by=['Pay Date']).copy().reset_index(drop=True)

# Rearrange columns
df_sort.columns

df_rearrange = df_sort[[
    'Agency',
    'Duty Station',
    'Service Comp Date',

    'Pay Period',
    'Pay Date',
    'Pay Begin Date',
    'Pay Period Ending',

    'Pay Plan',
    'Pay Grade',
    'Pay Step',
    'Annual Salary',
    'Net Pay',
    'Hourly Rate',
    'YTD Wages',
    'Gross Pay YTD',
    'Total Deductions YTD',
    'Financial Institution',
    'Home Address',

    'Maximum Carry Over',
    'Use Or Lose Balance',
    'Annual Leave Begin Balance',
    'Annual Leave Begin Balance Leave Year',
    'Annual Leave Earned',
    'Annual Leave Earned YTD',
    'Annual Leave Advanced',
    'Annual Leave Total',
    'Sick Leave Begin Balance',
    'Sick Leave Begin Balance Leave Year',
    'Sick Leave Earned',
    'Sick Leave Total',
    'Sick Leave Used',
    'Sick Leave Used YTD',
    'Sick Leave Advanced',
    'Sick Leave Ending Balance',
    'Time Off Award Begin Balance',
    'Time Off Award Begin Balance Leave Year',
    'Time Off Award Advanced',
    'Time Off Award Ending Balance',
    'Other Award',
    'Federal Taxes Adjusted',
    'Federal Taxes',
    'Federal Taxes YTD',
    'State Tax 1 ( DC ) Adjusted',
    'State Tax 1 ( DC )',
    'State Tax 1 ( DC ) YTD',
    'State Tax 1 ( VA ) Adjusted',
    'State Tax 1 ( VA )',
    'State Tax 1 ( VA ) YTD',
    'State Tax 2 ( DC ) Adjusted',
    'State Tax 2 ( DC )',
    'State Tax 2 ( DC ) YTD',
    'Health Benefits Adjusted',
    'Health Benefits',
    'Health Benefits YTD',
    'Dental/Vision Adjusted',
    'Dental/Vision',
    'Dental/Vision YTD',
    'TSP Tax Deferred Adjusted',
    'TSP Tax Deferred',
    'TSP Tax Deferred YTD',
    'Retirement - FERS/FRAE Adjusted',
    'Retirement - FERS/FRAE',
    'Retirement - FERS/FRAE YTD',
    'OASDI Tax Adjusted',
    'OASDI Tax',
    'OASDI Tax YTD',
    'Medicare Tax Adjusted',
    'Medicare Tax',
    'Medicare Tax YTD',
    'FEGLI - Regular Adjusted',
    'FEGLI - Regular',
    'FEGLI - Regular YTD',
    'Cumulative Retirement Agency',
    'TSP Tax Deferred Amt',
    'FEGLI',
    'FEGLI YTD',
    'Medicare',
    'Medicare YTD',
    'OASDI',
    'OASDI YTD',
    'TSP Basic',
    'TSP Basic YTD',
    'TSP Matching',
    'TSP Matching YTD',
    'FERS/FRAE',
    'FERS/FRAE YTD'
    ]].copy()

# Subset
# TODO: Add annual leave used current here and throughout
df_subset = df_rearrange[[
    'Agency',
    'Duty Station',
    'Pay Period',
    'Pay Date',
    'Pay Begin Date',
    'Pay Period Ending',
    'Pay Plan',
    'Pay Grade',
    'Pay Step',
    'Annual Salary',
    'Net Pay',
    'Hourly Rate',
    'YTD Wages',
    'Gross Pay YTD',
    'Total Deductions YTD',
    'Financial Institution',
    'Home Address',
    'Annual Leave Earned',
    'Annual Leave Total',
    'Sick Leave Earned',
    'Sick Leave Total',
    'Sick Leave Used',
    'Time Off Award Ending Balance',
    'Other Award',
    'Federal Taxes Adjusted',
    'Federal Taxes',
    'State Tax 1 ( DC )',
    'State Tax 1 ( VA )',
    'State Tax 2 ( DC )',
    'Health Benefits',
    'Dental/Vision',
    'TSP Tax Deferred',
    'Retirement - FERS/FRAE',
    'OASDI Tax',
    'Medicare Tax',
    'FEGLI - Regular',
    'Cumulative Retirement Agency',
    'TSP Tax Deferred Amt',
    'FEGLI',
    'Medicare',
    'OASDI',
    'TSP Basic',
    'TSP Matching',
    'FERS/FRAE',
    ]].copy()

# Print
print(tabulate(df_subset, headers='keys', tablefmt='plain'))



"------------------------------------------ Old Code Below ------------------------------------------"

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
