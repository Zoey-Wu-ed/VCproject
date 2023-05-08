'''
1. data cleaning
'''
import warnings; warnings.simplefilter('ignore')    
import pandas as pd
import numpy as np
# import statsmodels.api as sm
# import scipy.stats as scs
# import tushare as ts
%matplotlib inline
# from scipy.stats import norm
from matplotlib import pyplot as plt
# from scipy.interpolate import PchipInterpolator
# from scipy.integrate import quad
# from scipy import stats
from tqdm import *

# import deals dataset
deals = pd.read_csv('.\investmentsUK\deals.csv')    #import data
deals = deals.drop(columns=['Beauhurst company URL','Beauhurst deal URL','Amount raised (converted to GBP)'])    #drop useless information
deals = deals.rename(columns={'Verified investment amount (converted to GBP)':'Investment amount'})    #rename column
deals = deals.dropna()    #clean missing data rows

# import shares.csv
shares = pd.read_csv('.\investmentsUK\shares.csv')    #import data
shares = shares.loc[:,['Companies House Number','Company name','filing_date', 'first_name', 'last_name', 'number_of_shares','percent_total']]    #select and retain useful information


'''
2. data crawl through Company House API
'''
import requests
import json
import sys
import time
import numpy as np
from tqdm import *

companies = list(shares['Companies House Number'].unique())

# check if there is 0 missing in company house number
length = []
for i in companies:
    length_i = len(i)
    length.append(length_i)
print(set(length)) # {6, 7, 8}

# add 0 to those 6 or 7-character long registration number
companies_new = []
for i in companies:
    if len(i) == 8:
        companies_new.append(i)
    elif len(i) == 7:
        i = '0' + i
        companies_new.append(i)
    elif len(i) == 6:
        i = '00' + i
        companies_new.append(i)
        
'''collect capital: SH01 data'''
SH01_data = pd.DataFrame()
api_key = "86eb0eb5-ccbe-41cc-861a-2bebd865e64c"      
url = "https://api.company-information.service.gov.uk/company/{}/filing-history?category=capital&items_per_page={}&start_index={}"
items_per_page = 100

for company_number in tqdm(companies_new): 
    start_index = 0
    response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
    json_search_result = response.text
    search_result = json.JSONDecoder().decode(json_search_result)
    total_count = search_result['total_count']
    
    if total_count < items_per_page: 
        SH01_i = pd.DataFrame()
        action_date = []
        category = []
        date = []
        description = []
        description_values = []
        type_ = []
        company_number_i = []
        for item in search_result['items']:
            if item['type'] == 'SH01':
                company_number_i.append(company_number)
                action_date.append(item['action_date'])
                category.append(item['category'])
                date.append(item['date'])
                description.append(item['description'])
                description_values.append(str(item['description_values']))
                type_.append(item['type'])
            else: 
                pass
        SH01_i['company_number'] = company_number_i
        SH01_i['action_date'] = action_date
        SH01_i['category'] = category
        SH01_i['date'] = date
        SH01_i['description'] = description
        SH01_i['description_values'] = description_values
        SH01_i['type_'] = type_
    
        SH01_data = SH01_data.append(SH01_i)
        time.sleep(10)
    else:
        calculator = int(np.ceil(total_count/items_per_page))
        for i in range(calculator):
            start_index = i * items_per_page
            response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
            json_search_result = response.text
            search_result = json.JSONDecoder().decode(json_search_result)
            
            SH01_i = pd.DataFrame()
            action_date = []
            category = []
            date = []
            description = []
            description_values = []
            type_ = []
            company_number_i = []
            for item in search_result['items']:
                if item['type'] == 'SH01':
                    company_number_i.append(company_number)
                    action_date.append(item['action_date'])
                    category.append(item['category'])
                    date.append(item['date'])
                    description.append(item['description'])
                    description_values.append(str(item['description_values']))
                    type_.append(item['type'])
                else: 
                    pass
            SH01_i['company_number'] = company_number_i
            SH01_i['action_date'] = action_date
            SH01_i['category'] = category
            SH01_i['date'] = date
            SH01_i['description'] = description
            SH01_i['description_values'] = description_values
            SH01_i['type_'] = type_
            
            SH01_data = SH01_data.append(SH01_i)
            time.sleep(10)

# if there is a break in the above loop then run these following codes
aa = []
for company in companies_new: 
    if company in SH01_data.company_number.unique()[:-1]:
        pass
    else:
        aa.append(company)

for company_number in tqdm(aa): 
    start_index = 0
    response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
    json_search_result = response.text
    search_result = json.JSONDecoder().decode(json_search_result)
    total_count = search_result['total_count']
    
    if total_count < items_per_page: 
        SH01_i = pd.DataFrame()
        action_date = []
        category = []
        date = []
        description = []
        description_values = []
        type_ = []
        company_number_i = []
        for item in search_result['items']:
            if item['type'] == 'SH01':
                company_number_i.append(company_number)
                action_date.append(item['action_date'])
                category.append(item['category'])
                date.append(item['date'])
                description.append(item['description'])
                description_values.append(str(item['description_values']))
                type_.append(item['type'])
            else: 
                pass
        SH01_i['company_number'] = company_number_i
        SH01_i['action_date'] = action_date
        SH01_i['category'] = category
        SH01_i['date'] = date
        SH01_i['description'] = description
        SH01_i['description_values'] = description_values
        SH01_i['type_'] = type_
    
        SH01_data = SH01_data.append(SH01_i)
        time.sleep(10)
    else:
        calculator = int(np.ceil(total_count/items_per_page))
        for i in range(calculator):
            start_index = i * items_per_page
            response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
            json_search_result = response.text
            search_result = json.JSONDecoder().decode(json_search_result)
            
            SH01_i = pd.DataFrame()
            action_date = []
            category = []
            date = []
            description = []
            description_values = []
            type_ = []
            company_number_i = []
            for item in search_result['items']:
                if item['type'] == 'SH01':
                    company_number_i.append(company_number)
                    action_date.append(item['action_date'])
                    category.append(item['category'])
                    date.append(item['date'])
                    description.append(item['description'])
                    description_values.append(str(item['description_values']))
                    type_.append(item['type'])
                else: 
                    pass
            SH01_i['company_number'] = company_number_i
            SH01_i['action_date'] = action_date
            SH01_i['category'] = category
            SH01_i['date'] = date
            SH01_i['description'] = description
            SH01_i['description_values'] = description_values
            SH01_i['type_'] = type_
            
            SH01_data = SH01_data.append(SH01_i)
            time.sleep(10)

SH01_data.to_csv('./data_crawl/org_SH01_data.csv')
# unique company: 3930

'''collect confirmation-statement: CS01 and AR01 data'''
CS01_AR01_data = pd.DataFrame()
api_key = "86eb0eb5-ccbe-41cc-861a-2bebd865e64c"      
url = "https://api.company-information.service.gov.uk/company/{}/filing-history?category=confirmation-statement&items_per_page={}&start_index={}"
items_per_page = 100

for company_number in tqdm(companies_new): # companies_new
    start_index = 0
    response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
    json_search_result = response.text
    search_result = json.JSONDecoder().decode(json_search_result)
    total_count = search_result['total_count']
    
    if total_count < items_per_page: 
        CS01_AR01_i = pd.DataFrame()
        action_date = []
        category = []
        date = []
        description = []
        description_values = []
        type_ = []
        company_number_i = []
        for item in search_result['items']:
            if item['type'] == 'CS01' or item['type'] == 'AR01':
                company_number_i.append(company_number)
                action_date.append(item['action_date'])
                category.append(item['category'])
                date.append(item['date'])
                description.append(item['description'])
                description_values.append(str(item['description_values']))
                type_.append(item['type'])
            else: 
                pass
        CS01_AR01_i['company_number'] = company_number_i
        CS01_AR01_i['action_date'] = action_date
        CS01_AR01_i['category'] = category
        CS01_AR01_i['date'] = date
        CS01_AR01_i['description'] = description
        CS01_AR01_i['description_values'] = description_values
        CS01_AR01_i['type_'] = type_
    
        CS01_AR01_data = CS01_AR01_data.append(CS01_AR01_i)
        time.sleep(10)
    else:
        calculator = int(np.ceil(total_count/items_per_page))
        for i in range(calculator):
            start_index = i * items_per_page
            response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
            json_search_result = response.text
            search_result = json.JSONDecoder().decode(json_search_result)
            
            CS01_AR01_i = pd.DataFrame()
            action_date = []
            category = []
            date = []
            description = []
            description_values = []
            type_ = []
            company_number_i = []
            for item in search_result['items']:
                if item['type'] == 'CS01' or item['type'] == 'AR01':
                    company_number_i.append(company_number)
                    action_date.append(item['action_date'])
                    category.append(item['category'])
                    date.append(item['date'])
                    description.append(item['description'])
                    description_values.append(str(item['description_values']))
                    type_.append(item['type'])
                else: 
                    pass
            CS01_AR01_i['company_number'] = company_number_i
            CS01_AR01_i['action_date'] = action_date
            CS01_AR01_i['category'] = category
            CS01_AR01_i['date'] = date
            CS01_AR01_i['description'] = description
            CS01_AR01_i['description_values'] = description_values
            CS01_AR01_i['type_'] = type_
            
            CS01_AR01_data = CS01_AR01_data.append(CS01_AR01_i)
            time.sleep(10)

# if there is a break in the above loop then run these following codes
aa = []
for company in companies_new: 
    if company in CS01_AR01_data.company_number.unique()[:-1]:
        pass
    else:
        aa.append(company)

for company_number in tqdm(aa): # companies_new
    start_index = 0
    response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
    json_search_result = response.text
    search_result = json.JSONDecoder().decode(json_search_result)
    total_count = search_result['total_count']
    
    if total_count < items_per_page: 
        CS01_AR01_i = pd.DataFrame()
        action_date = []
        category = []
        date = []
        description = []
        description_values = []
        type_ = []
        company_number_i = []
        for item in search_result['items']:
            if item['type'] == 'CS01' or item['type'] == 'AR01':
                company_number_i.append(company_number)
                action_date.append(item['action_date'])
                category.append(item['category'])
                date.append(item['date'])
                description.append(item['description'])
                description_values.append(str(item['description_values']))
                type_.append(item['type'])
            else: 
                pass
        CS01_AR01_i['company_number'] = company_number_i
        CS01_AR01_i['action_date'] = action_date
        CS01_AR01_i['category'] = category
        CS01_AR01_i['date'] = date
        CS01_AR01_i['description'] = description
        CS01_AR01_i['description_values'] = description_values
        CS01_AR01_i['type_'] = type_
    
        CS01_AR01_data = CS01_AR01_data.append(CS01_AR01_i)
        time.sleep(10)
    else:
        calculator = int(np.ceil(total_count/items_per_page))
        for i in range(calculator):
            start_index = i * items_per_page
            response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
            json_search_result = response.text
            search_result = json.JSONDecoder().decode(json_search_result)
            
            CS01_AR01_i = pd.DataFrame()
            action_date = []
            category = []
            date = []
            description = []
            description_values = []
            type_ = []
            company_number_i = []
            for item in search_result['items']:
                if item['type'] == 'CS01' or item['type'] == 'AR01':
                    company_number_i.append(company_number)
                    action_date.append(item['action_date'])
                    category.append(item['category'])
                    date.append(item['date'])
                    description.append(item['description'])
                    description_values.append(str(item['description_values']))
                    type_.append(item['type'])
                else: 
                    pass
            CS01_AR01_i['company_number'] = company_number_i
            CS01_AR01_i['action_date'] = action_date
            CS01_AR01_i['category'] = category
            CS01_AR01_i['date'] = date
            CS01_AR01_i['description'] = description
            CS01_AR01_i['description_values'] = description_values
            CS01_AR01_i['type_'] = type_
            
            CS01_AR01_data = CS01_AR01_data.append(CS01_AR01_i)
            time.sleep(10)

CS01_AR01_data.to_csv('./data_crawl/org_CS01_AR01_data.csv')


'''
3. data processing
'''
import pandas as pd
import re
CS01_AR01 = pd.read_csv('./data_crawl/org_CS01_AR01_data.csv')
CS01_AR01.drop(['Unnamed: 0'],axis=1,inplace=True)
SH01 = pd.read_csv('./data_crawl/org_SH01_data.csv')
SH01.drop(['Unnamed: 0'],axis=1,inplace=True)

# change the variable name
CS01_AR01 = CS01_AR01.rename(columns={'date':'filing_date'})    #rename column
SH01 = SH01.rename(columns={'date':'filing_date'})    #rename column

currency_lst = []
amount_lst = []
for i in range(len(SH01)):
    dic = eval(SH01['description_values'][i])
    if 'capital' in dic:
        capital = dic['capital'][0]
        currency = capital['currency']
        amount = capital['figure']
    else:
        pass
    currency_lst.append(currency)
    amount_lst.append(amount)
    
SH01['currency'] = currency_lst
SH01['aggregate_nominal_value”.'] = amount_lst

currency_lst = []
amount_lst = []
for i in range(len(CS01_AR01)):
    dic = eval(CS01_AR01['description_values'][i])
    if 'original_description' in dic:
        desc = dic['original_description']
        desc = re.sub('[0-9]{2}/[0-9]{2}/[0-9]{2}','',desc)
        if 'gbp' in desc:
            currency = 'GBP'
            amount = re.findall("\d+\.\d+|\d+",desc)[0]
        elif 'usd' in desc:
            currency = 'USD'
            amount = re.findall("\d+\.\d+|\d+",desc)[0]
        elif 'eur' in desc:
            currency = 'EUR'
            amount = re.findall("\d+\.\d+|\d+",desc)[0]
        else:
            currency = 'unknown'
            amount = re.findall("\d+\.\d+|\d+",desc)[0]
    else:
        currency = ''
        amount = ''
    currency_lst.append(currency)
    amount_lst.append(amount)

CS01_AR01['currency'] = currency_lst
CS01_AR01['aggregate_nominal_value”.'] = amount_lst
       
CS01_AR01.to_csv('./data_crawl/processed_CS01_AR01_data.csv')
SH01.to_csv('./data_crawl/processed_SH01_data.csv')


'''
4. comparison
'''
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tqdm import *

# import deals dataset
deals = pd.read_csv('.\investmentsUK\deals.csv')    #import data
deals = deals.drop(columns=['Beauhurst company URL','Beauhurst deal URL','Amount raised (converted to GBP)'])    #drop useless information
deals = deals.rename(columns={'Verified investment amount (converted to GBP)':'Investment amount'})    #rename column
deals = deals.dropna()    #clean missing data rows

# import shares.csv
shares = pd.read_csv('.\investmentsUK\shares.csv')    #import data
shares = shares.loc[:,['Companies House Number','Company name','filing_date', 'first_name', 'last_name', 'number_of_shares','percent_total']]    #select and retain useful information

# improt processed SH01 and CS01_AR01 data
data_CS01_AR01 = pd.read_csv('./data_crawl/processed_CS01_AR01_data.csv')
data_CS01_AR01.drop(['Unnamed: 0'],axis=1,inplace=True)
data_SH01 = pd.read_csv('./data_crawl/processed_SH01_data.csv')
data_SH01.drop(['Unnamed: 0'],axis=1,inplace=True)



