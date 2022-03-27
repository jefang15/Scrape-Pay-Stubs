""" Scrape Text from Pay Stubs """

import glob
import pdfplumber
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np


def scrape_pay_stubs(folder):
    """
    Indexing notes:
    string.find(i) - returns index position of the first appearance of the desired keyword
    len(i) - returns length of keyword string; to get to the index number at the end of the entire keyword
    string.find('<end>', string.find(i)) - returns index when <end> appears, starting at the keyword index instead of whole string
    string[(string.find(i) + len(i)):(string.find('<end>', string.find(i)))] - returns desired value based on index
    """
    out = []  # Empty list to store information from all PDFs
    for file in folder:
        with pdfplumber.open(file) as one_pdf:
            string = ''
            for i in range(0, len(one_pdf.pages)):
                string += one_pdf.pages[i].extract_text().replace('\n', '<end>')  # Write each page of single PDF to empty string
                # Keeps <end> as indicator for end of each line of string

            inner = []

            " General Information and Leave "
            keywords = [
                'Pay Period Ending : ', 'Net Pay $ : ', 'Pay Period # : ', 'Pay Date : ', 'Pay Plan : ', 'Pay Grade : ',
                'Pay Step : ', 'Annual Salary $ : ', 'Hourly Rate $ : ', 'YTD Wages: ', 'Gross Pay YTD: ',
                'Total Deductions YTD: ', 'Maximum Carry Over: ', 'Use Or Lose Balance: ', 'Annual Leave Begin Balance Current: ',
                'Annual Leave Begin Balance Leave Year: ', 'Annual Leave Earned Current: ', 'Annual Leave Earned YTD: ',
                'Annual Leave Used Current: ', 'Annual Leave Used YTD: ', 'Annual Leave Advanced: ',
                'Annual Leave Ending Balance: ', 'Sick Leave Begin Balance Current: ', 'Sick Leave Begin Balance Leave Year: ',
                'Sick Leave Earned Current: ', 'Sick Leave Earned YTD: ', 'Sick Leave Used Current: ', 'Sick Leave Used YTD: ',
                'Sick Leave Advanced: ', 'Sick Leave Ending Balance: ', 'Time Off Award Begin Balance Current: ',
                'Time Off Award Begin Balance Leave Year: ', 'Time Off Award Earned Current: ', 'Time Off Award Earned YTD: ',
                'Time Off Award Used Current: ', 'Time Off Award Used YTD: ', 'Time Off Award Advanced: ',
                'Time Off Award Ending Balance: '
                ]
            for i in keywords:
                if i in string:  # If statement because certain keywords do not appear in each PDF
                    inner.append(string[(string.find(i) + len(i)):(string.find('<end>', string.find(i)))])
                else:
                    inner.append('')

            " Other Award "
            if 'Other Award' in string:
                other_award_substring = string[string.find('Other Award'):]
                inner.append(other_award_substring[
                             other_award_substring.find('Adj Hours | ') + len('Adj Hours | '):other_award_substring.find(
                                 ' Current PPD')])
            else:
                inner.append(0)

            " Home Address "
            inner.append(string[(string.find('Home Address') + len('Home Address') + len('<end>')):
                                (string.find('Pay Check', string.find('Home Address'))) - len('<end>')])

            " Deductions "
            keywords2 = [
                'Federal Taxes', 'State Tax 1 ( DC )', 'State Tax 1 ( VA )', 'State Tax 2 ( DC )', 'Health Benefits - Pretax',
                'Dental/Vision', 'TSP Tax Deferred', 'Retirement - FERS/FRAE', 'OASDI Tax', 'Medicare Tax', 'FEGLI - Regular'
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
                'Service Comp Date', 'Agency', 'Cumulative Retirement Agency $', 'Duty Station', 'Pay Begin Date',
                'Financial Institution', 'TSP Tax Deferred Amt/%'
                ]
            for i in keywords3:
                inner.append(string[(string.find(i) + len(i)):(string.find(':', string.find(i)))])

            " Benefits "
            benefits_substring = string[string.find('Benefits Paid by Government'):]
            keywords4 = [
                'FEGLI', 'Medicare', 'OASDI', 'TSP Basic', 'TSP Matching', 'FERS/FRAE'
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


pay_stubs = glob.glob('Projects/Scrape-Paystubs/Pay Stubs - FERC/*.pdf')
scraped_pay_data = scrape_pay_stubs(pay_stubs)


" Create DataFrame "

headings = ['Pay Period Ending', 'Net Pay', 'Pay Period', 'Pay Date', 'Pay Plan', 'Pay Grade', 'Pay Step', 'Annual Salary',
            'Hourly Rate', 'YTD Wages', 'Gross Pay YTD', 'Total Deductions YTD', 'Maximum Carry Over', 'Use Or Lose Balance',
            'Annual Leave Begin Balance', 'Annual Leave Begin Balance Leave Year', 'Annual Leave', 'Annual Leave Earned YTD',
            'Annual Leave Used', 'Annual Leave Used YTD', 'Annual Leave Advanced', 'Annual Leave Total',
            'Sick Leave Begin Balance', 'Sick Leave Begin Balance Leave Year', 'Sick Leave', 'Sick Leave Earned YTD',
            'Sick Leave Used', 'Sick Leave Used YTD', 'Sick Leave Advanced', 'Sick Leave Total',
            'Time Off Award Begin Balance', 'Time Off Award Begin Balance Leave Year', 'Time Off Award',
            'Time Off Award Earned YTD', 'Time Off Award Used', 'Time Off Award Used YTD', 'Time Off Award Advanced',
            'Time Off Award Total', 'Other Award', 'Home Address', 'Federal Taxes Adjusted', 'Federal Taxes', 'Federal Taxes YTD',
            'State Tax 1 ( DC ) Adjusted', 'State Tax 1 ( DC )', 'State Tax 1 ( DC ) YTD', 'State Tax 1 ( VA ) Adjusted',
            'State Tax 1 ( VA )', 'State Tax 1 ( VA ) YTD', 'State Tax 2 ( DC ) Adjusted', 'State Tax 2 ( DC )',
            'State Tax 2 ( DC ) YTD', 'Health Benefits Adjusted', 'Health Benefits', 'Health Benefits YTD',
            'Dental/Vision Adjusted', 'Dental/Vision', 'Dental/Vision YTD', 'TSP Tax Deferred Adjusted', 'TSP Tax Deferred',
            'TSP Tax Deferred YTD', 'Retirement - FERS/FRAE Adjusted', 'Retirement - FERS/FRAE', 'Retirement - FERS/FRAE YTD',
            'OASDI Tax Adjusted', 'OASDI Tax', 'OASDI Tax YTD', 'Medicare Tax Adjusted', 'Medicare Tax', 'Medicare Tax YTD',
            'FEGLI - Regular Adjusted', 'FEGLI - Regular', 'FEGLI - Regular YTD', 'Service Comp Date', 'Agency',
            'Cumulative Retirement Agency', 'Duty Station', 'Pay Begin Date', 'Financial Institution', 'TSP Tax Deferred Amt',
            'FEGLI', 'FEGLI YTD', 'Medicare', 'Medicare YTD', 'OASDI', 'OASDI YTD', 'TSP Basic', 'TSP Basic YTD', 'TSP Matching',
            'TSP Matching YTD', 'FERS/FRAE', 'FERS/FRAE YTD'
            ]

df_scraped_pay = pd.DataFrame(scraped_pay_data, columns=headings)


def convert_datatypes(df):
    vars_to_datetime = [
        'Pay Period Ending', 'Pay Date', 'Service Comp Date', 'Pay Begin Date'
        ]
    df[vars_to_datetime] = df[vars_to_datetime].apply(pd.to_datetime)

    vars_to_int = [
        'Pay Period', 'Pay Grade', 'Pay Step', 'Maximum Carry Over', 'Use Or Lose Balance', 'Annual Leave Begin Balance',
        'Annual Leave Begin Balance Leave Year', 'Annual Leave', 'Annual Leave Earned YTD', 'Annual Leave Used',
        'Annual Leave Used YTD', 'Annual Leave Advanced', 'Annual Leave Total', 'Sick Leave Begin Balance',
        'Sick Leave Begin Balance Leave Year', 'Sick Leave', 'Sick Leave Earned YTD', 'Sick Leave Used', 'Sick Leave Used YTD',
        'Sick Leave Advanced', 'Sick Leave Total', 'Time Off Award Begin Balance', 'Time Off Award Begin Balance Leave Year',
        'Time Off Award', 'Time Off Award Earned YTD', 'Time Off Award Used', 'Time Off Award Used YTD',
        'Time Off Award Advanced',
        'Time Off Award Total'
        ]
    df[vars_to_int] = df[vars_to_int].apply(pd.to_numeric).fillna(0).astype(int)

    vars_to_float = [
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
    df[vars_to_float] = df[vars_to_float].replace(',', '', regex=True).apply(pd.to_numeric, errors='coerce').fillna(0)

    # Clean up remaining fields
    df['TSP Tax Deferred Amt'] = df['TSP Tax Deferred Amt'].replace(' ', '', regex=True)
    df['Home Address'] = df['Home Address'].replace('<end>', '', regex=True)

    return df


df_scraped_pay = convert_datatypes(df_scraped_pay)

df_scraped_pay['Year'] = df_scraped_pay['Pay Period Ending'].dt.year

paystubs_master = df_scraped_pay[[
    'Agency',
    'Duty Station',
    'Service Comp Date',
    'Pay Period',
    'Pay Date',
    'Pay Begin Date',
    'Pay Period Ending',
    'Year',
    'Pay Plan',
    'Pay Grade',
    'Pay Step',
    'Annual Salary',
    'Gross Pay YTD',
    'Net Pay',
    'Hourly Rate',
    'YTD Wages',
    'Total Deductions YTD',
    'Financial Institution',
    'Home Address',
    'Maximum Carry Over',
    'Use Or Lose Balance',
    'Annual Leave Begin Balance',
    'Annual Leave Begin Balance Leave Year',
    'Annual Leave',
    'Annual Leave Earned YTD',
    'Annual Leave Used',
    'Annual Leave Used YTD',
    'Annual Leave Advanced',
    'Annual Leave Total',
    'Sick Leave Begin Balance',
    'Sick Leave Begin Balance Leave Year',
    'Sick Leave',
    'Sick Leave Earned YTD',
    'Sick Leave Used',
    'Sick Leave Used YTD',
    'Sick Leave Advanced',
    'Sick Leave Total',
    'Time Off Award Begin Balance',
    'Time Off Award Begin Balance Leave Year',
    'Time Off Award',
    'Time Off Award Earned YTD',
    'Time Off Award Used',
    'Time Off Award Used YTD',
    'Time Off Award Advanced',
    'Time Off Award Total',
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
    ]]

paystubs_master = paystubs_master.sort_values(by=['Pay Date']).copy().reset_index(drop=True)

# paystubs_master.to_csv('Projects/Scrape-Paystubs/Output/Earnings and Leave Statements Master.csv', index=False)


" Summarize Pay and Deductions "

# Components of gross pay
gross_pay = paystubs_master[[
    'Pay Period Ending', 'Year', 'Net Pay', 'Federal Taxes', 'State Tax 1 ( DC )', 'State Tax 1 ( VA )', 'State Tax 2 ( DC )',
    'Health Benefits', 'Dental/Vision', 'TSP Tax Deferred', 'Retirement - FERS/FRAE', 'OASDI Tax', 'Medicare Tax',
    'FEGLI - Regular'
    ]].copy()

gross_pay_long = gross_pay.melt(
    id_vars=['Pay Period Ending', 'Year'],
    var_name='Description',
    value_name='Amount'
    )

gross_pay_long.loc[gross_pay_long['Description'] == 'Net Pay', 'Category'] = 'Net Pay'
gross_pay_long.loc[gross_pay_long['Description'] == 'Federal Taxes', 'Category'] = 'Taxes'
gross_pay_long.loc[gross_pay_long['Description'] == 'State Tax 1 ( DC )', 'Category'] = 'Taxes'
gross_pay_long.loc[gross_pay_long['Description'] == 'State Tax 1 ( VA )', 'Category'] = 'Taxes'
gross_pay_long.loc[gross_pay_long['Description'] == 'State Tax 2 ( DC )', 'Category'] = 'Taxes'
gross_pay_long.loc[gross_pay_long['Description'] == 'Health Benefits', 'Category'] = 'Health Insurance'
gross_pay_long.loc[gross_pay_long['Description'] == 'Dental/Vision', 'Category'] = 'Health Insurance'
gross_pay_long.loc[gross_pay_long['Description'] == 'TSP Tax Deferred', 'Category'] = 'Retirement'
gross_pay_long.loc[gross_pay_long['Description'] == 'Retirement - FERS/FRAE', 'Category'] = 'Retirement'
gross_pay_long.loc[gross_pay_long['Description'] == 'OASDI Tax', 'Category'] = 'Taxes'
gross_pay_long.loc[gross_pay_long['Description'] == 'Medicare Tax', 'Category'] = 'Taxes'
gross_pay_long.loc[gross_pay_long['Description'] == 'FEGLI - Regular', 'Category'] = 'Retirement'

pay_annual = gross_pay_long.groupby(['Year', 'Category'])['Amount'].sum().reset_index()


" Import Credit Card Statements "


def concat_chase_statements(folder):
    for statement in folder:
        concat_csv = pd.concat(pd.read_csv(statement) for statement in folder)
        return concat_csv


chase_statements = glob.glob('Projects/Scrape-Paystubs/Expenses - Chase/*')
chase_concat = concat_chase_statements(chase_statements).reset_index(drop=True)

# Show unique type of transactions 
pd.DataFrame(chase_concat["Type"].unique())
# Positive values for Sales and Adjustments
chase_concat['Amount'] = chase_concat['Amount'].abs()
# Negative values for Returns
chase_concat.loc[chase_concat.Type == 'Return', 'Amount'] = chase_concat['Amount'] * -1

# Drop (credit card) Payment transactions
chase_concat = chase_concat.loc[
    (chase_concat['Type'] == 'Adjustment') |
    (chase_concat['Type'] == 'Sale') |
    (chase_concat['Type'] == 'Return')].copy()

chase_concat.rename(columns={'Category': 'Category Description'}, inplace=True)
chase_concat.rename(columns={'Description': 'Merchant'}, inplace=True)
chase_concat['Category'] = 'Expenses'

chase_concat['Transaction Date'] = chase_concat['Transaction Date'].apply(pd.to_datetime)
chase_concat['Year'] = pd.to_datetime(chase_concat['Transaction Date']).dt.year

chase_master = chase_concat[['Transaction Date', 'Year', 'Category', 'Category Description', 'Merchant', 'Amount']].copy()
chase_master.dtypes



def concat_amex_statements(folder):
    for statement in folder:
        concat_xlsx = pd.concat(pd.read_excel(statement, skiprows=6) for statement in folder)
        return concat_xlsx


amex_statements = glob.glob('Projects/Scrape-Paystubs/Expenses - American Express/*')
amex_concat = concat_amex_statements(amex_statements)

amex_concat = amex_concat.loc[(amex_concat['Amount'] > 0)].copy().reset_index(drop=True)

amex_concat.rename(columns={'Date': 'Transaction Date'}, inplace=True)
amex_concat.rename(columns={'Description': 'Merchant'}, inplace=True)
amex_concat.rename(columns={'Category': 'Category Description'}, inplace=True)
amex_concat['Category'] = 'Expenses'

amex_concat['Year'] = pd.to_datetime(amex_concat['Transaction Date']).dt.year
amex_concat['Transaction Date'] = amex_concat['Transaction Date'].apply(pd.to_datetime)

amex_master = amex_concat[['Transaction Date', 'Year', 'Category', 'Category Description', 'Merchant', 'Amount']].copy()
amex_master.dtypes


" Concatenate Credit Card Charges "

charges_concat = pd.concat([chase_master, amex_master], ignore_index=True)

# Condense expense categories
pd.DataFrame(charges_concat['Category Description'].unique())

charges_concat.loc[charges_concat['Category Description'] == 'Business Services-Office Supplies', 'Category Description'] = 'Streaming'
charges_concat.loc[charges_concat['Category Description'] == 'Communications-Cable & Internet Comm', 'Category Description'] = 'Streaming'
charges_concat.loc[charges_concat['Category Description'] == 'Home', 'Category Description'] = 'Shopping'
charges_concat.loc[charges_concat['Category Description'] == 'Merchandise & Supplies-Groceries', 'Category Description'] = 'Groceries'
charges_concat.loc[charges_concat['Category Description'] == 'Merchandise & Supplies-Internet Purchase', 'Category Description'] = 'Shopping'
charges_concat.loc[charges_concat['Category Description'] == 'Personal', 'Category Description'] = 'Shopping'
charges_concat.loc[charges_concat['Category Description'] == 'Restaurant-Bar & Café', 'Category Description'] = 'Food & Drink'
charges_concat.loc[charges_concat['Category Description'] == 'Restaurant-Restaurant', 'Category Description'] = 'Food & Drink'
charges_concat.loc[charges_concat['Category Description'] == 'Transportation-Fuel', 'Category Description'] = 'Gas'
charges_concat.loc[charges_concat['Category Description'] == 'Transportation-Parking Charges', 'Category Description'] = 'Travel'
charges_concat.loc[charges_concat['Category Description'] == 'Transportation-Taxis & Coach', 'Category Description'] = 'Travel'

# Recategorize merchant categories
charges_concat.sort_values(by='Category Description').reset_index(drop=True)

charges_concat.loc[charges_concat['Merchant'].str.contains('SPOTIFY|Spotify'), 'Category Description'] = 'Streaming'
charges_concat.loc[charges_concat['Merchant'].str.contains(
    'WA VEHICLE LICENSING|IDENTOGO-IDEMIA TSA PRECH'), 'Category Description'] = 'Travel'
charges_concat.loc[charges_concat['Merchant'].str.contains('Amazon|PAYPAL'), 'Category Description'] = 'Shopping'
charges_concat.loc[charges_concat['Merchant'].str.contains('BRIG|Brig|NIELSON WINES'), 'Category Description'] = 'Food & Drink'
charges_concat.loc[charges_concat['Merchant'].str.contains(
    'ACADIA NATIONAL PARK|THE NC ARBORETUM'), 'Category Description'] = 'Entertainment'
charges_concat = charges_concat[~charges_concat['Category Description'].str.contains('Fees & Adjustments')]
charges_concat = charges_concat[charges_concat['Year'] > 2019]

charges_master = charges_concat.sort_values(by=['Year', 'Transaction Date', 'Category Description', 'Merchant']).copy()

# charges_master.to_csv('Projects/Scrape-Paystubs/Output/Expenses Master.csv', index=False)

# charges_master.loc[
#     (charges_master['Category Description'] == 'Streaming') | (charges_master['Category Description'] == 'Entertainment')].to_csv(
#     'Projects/Scrape-Paystubs/Output/Expenses Master - Sample.csv', index=False)


" Analyze Credit Card Charges "

# To concatenate with pay
charges_annual = charges_master.groupby(['Year', 'Category'])['Amount'].sum().reset_index()
# To plot
charges_description_annual = charges_master.groupby(['Year', 'Category Description'])['Amount'].sum().reset_index()

# Transform data long to wide by Year
charges_description_wide = charges_description_annual.pivot(
    index='Category Description',
    columns='Year',
    values='Amount'
    ).reset_index()


" Plot Annual Charges "


plt.style.use('seaborn-notebook')  # Set style
fig, ax = plt.subplots(figsize=(13, 8))  # Set figure

x_axis = np.arange(len(charges_description_wide['Category Description']))

# Plot
plt.bar(x_axis - 0.2, charges_description_wide.iloc[:, 1], width=0.4, label='2020')
plt.bar(x_axis + 0.2, charges_description_wide.iloc[:, 2], width=0.4, label='2021')

# Titles
plt.title('Annual Expenses by Category',
          fontweight='bold',
          fontsize=20)
plt.ylabel('Amount ($)',
           fontweight='bold',
           size=12)

plt.xticks(x_axis, charges_description_wide['Category Description'])
plt.tight_layout()
plt.legend()
plt.show()

# plt.savefig('Projects/Scrape-Paystubs/Output/Annual Expenses by Category.png')
# plt.savefig('Projects/Scrape-Paystubs/Output/Annual Expenses by Category.pdf')


" Concatenate Annual Pay and Charges "

# Concatenate
pay_charge_concat = pd.concat([pay_annual, charges_annual], ignore_index=True)
pay_charge_annual = pay_charge_concat[['Year', 'Category', 'Amount']].sort_values(by=['Year', 'Category'])


" Calculate Savings by Year "

# Transform data long to wide by Year
pay_charge_wide = pay_charge_annual.pivot(
    index='Year',
    columns='Category',
    values='Amount'
    ).reset_index().fillna(0)

gross_pay = paystubs_master.iloc[:, [7, 12]].loc[paystubs_master['Pay Period'] == 26]
pay_charge_wide = pay_charge_wide.merge(gross_pay, how='left', left_on=['Year'], right_on=['Year'])

pay_charge_wide['Savings'] = pay_charge_wide['Gross Pay YTD'] - pay_charge_wide['Taxes'] - pay_charge_wide['Retirement'] \
                             - pay_charge_wide['Health Insurance'] - pay_charge_wide['Expenses']

print(tabulate(pay_charge_wide, headers='keys', tablefmt='plain'))
