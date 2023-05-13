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

# remove those useless variables
data_SH01.drop(['category','description','description_values','type_'],axis=1,inplace=True)
data_SH01 = data_SH01.rename(columns={'aggregate_nominal_value”.':'aggregate_nominal_value'})

# add 0 to those 6 or 7-character long registration number for shares data
companies_new = []
for i in shares['Companies House Number'].values:
    if len(i) == 8:
        companies_new.append(i)
    elif len(i) == 7:
        i = '0' + i
        companies_new.append(i)
    elif len(i) == 6:
        i = '00' + i
        companies_new.append(i)
shares['Companies House Number'] = companies_new

shares.drop(['first_name','last_name', 'number_of_shares', 'percent_total'],axis=1,inplace=True)
shares = shares.drop_duplicates(inplace=False)    #eliminate duplicate data rows
shares = shares.dropna()

shares_com = shares[['Companies House Number','Company name']]
shares_com = shares_com.drop_duplicates(inplace=False)    #eliminate duplicate data rows
# shares data has 4026 unique firms

data_SH01 = data_SH01.rename(columns = {'company_number':'Companies House Number'})
data_SH01 = pd.merge(data_SH01, shares_com, on=['Companies House Number'], how='inner') 
data_SH01.to_csv('./data_crawl/match_SH01.csv')
# data_SH01 data has 3790 unique firms
# 24467 total observations

data_SH01_com = data_SH01[['Companies House Number']]
data_SH01_com = data_SH01_com.drop_duplicates(inplace=False)    #eliminate duplicate data rows
shares = pd.merge(shares, data_SH01_com, on=['Companies House Number'], how='inner') 
shares.to_csv('./data_crawl/match_shares.csv')
# now the shares data also has the same 3790 as those in data_SH01 
# 14185 total observations
# we can compare if the number of filings for these two datasets are the same 

# we also extract those deals information for these 3790 firms
data_SH01_com = data_SH01[['Companies House Number','Company name']]
data_SH01_com = data_SH01_com.drop_duplicates(inplace=False)    #eliminate duplicate data rows
deals = pd.merge(deals, data_SH01_com, on=['Company name'], how='inner') 
deals.to_csv('./data_crawl/match_deals.csv')
# there are only 3470 firms in deals data (smaller than 3790)
# 7203 total observations

'''4.1 match the shares and SH01 data'''
companies = list(shares['Companies House Number'].unique())

shares_count = []
data_SH01_count = []
for com in companies:
    aa = shares[shares['Companies House Number'] == com]
    shares_count_i = len(aa)
    bb = data_SH01[data_SH01['Companies House Number'] == com]
    data_SH01_count_i = len(bb)
    shares_count.append(shares_count_i)
    data_SH01_count.append(data_SH01_count_i)

filings_number = pd.DataFrame()
filings_number['Companies House Number'] =  companies
filings_number['shares_Org'] = shares_count
filings_number['data_SH01'] = data_SH01_count

filings_number['match'] = ''
for i in range(len(filings_number)):
    if filings_number['shares_Org'][i] == filings_number['data_SH01'][i]:
        filings_number['match'][i] = 'True'
    else:
        filings_number['match'][i] = 'False'
# 496 firms are Ture, 3294 firms are False
# Although the number of filings are matched in 496 firms, the filings dates cannot be further matched. 


'''4.2 match the deals and SH01 data'''
# It is difficult to match the deals and SH01 data since the dates are totally different 
# Therefore, we only match those firms that have only one filing date
data_SH01_one = pd.DataFrame()
for com in data_SH01['Company name'].unique():
    aa = data_SH01[data_SH01['Company name'] == com]
    if len(aa) == 1:
        data_SH01_one = data_SH01_one.append(aa)
    else:
        pass
# 566 firms only have one filing data which can also be considered as one deal data
 
# obtain the corresponding deals_one
deals_one = pd.DataFrame()
for com in data_SH01_one['Company name'].unique():
    aa = deals[deals['Company name'] == com]
    if len(aa) == 1:
        deals_one = deals_one.append(aa)
    else:
        pass

data_SH01_one_new = pd.DataFrame()
for com in deals_one['Company name'].unique():
    aa = data_SH01_one[data_SH01_one['Company name'] == com]
    data_SH01_one_new = data_SH01_one_new.append(aa)
    
data_SH01_one_new.reset_index(inplace=True)
data_SH01_one_new.drop(['index'],axis=1,inplace=True)

# process the aggregate_nominal_value
for i in range(len(data_SH01_one_new)):
    data_SH01_one_new['aggregate_nominal_value'][i] = data_SH01_one_new['aggregate_nominal_value'][i].replace(',','')
data_SH01_one_new['aggregate_nominal_value'] = data_SH01_one_new['aggregate_nominal_value'].astype('float')

# transform the EUR and USD currency
for i in range(len(data_SH01_one_new)):
    if data_SH01_one_new['currency'][i] == 'GBP':
        pass
    elif data_SH01_one_new['currency'][i] == 'EUR':
        data_SH01_one_new['aggregate_nominal_value'][i] = data_SH01_one_new['aggregate_nominal_value'][i] * 0.87
    elif data_SH01_one_new['currency'][i] == 'USD':
        data_SH01_one_new['aggregate_nominal_value'][i] = data_SH01_one_new['aggregate_nominal_value'][i] * 0.79
data_SH01_one_new.drop(['currency'],axis=1,inplace=True)

match = pd.merge(deals_one, data_SH01_one_new, on=['Company name'], how='inner') # remaining 3639 companies for deals
match.to_csv('./data_crawl/match_deals_SH01_one.csv')
# 450 firms

import seaborn as sns
import matplotlib.ticker as ticker

sns.set_theme(style='darkgrid')  # 图形主题
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 指定默認字體
plt.rcParams['axes.unicode_minus'] = False
plt.figure(dpi=600) # 设置分辨率
ax = sns.distplot(match['Investment amount'],hist=False,kde=True,color='limegreen')
ax = sns.distplot(match['aggregate_nominal_value'],hist=False, kde=True,color='salmon')
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
# Get the two lines from the axes to generate shading
l1 = ax.lines[0]
l2 = ax.lines[1]
# Get the xy data from the lines so that we can shade
x1 = l1.get_xydata()[:,0]
y1 = l1.get_xydata()[:,1]
x2 = l2.get_xydata()[:,0]
y2 = l2.get_xydata()[:,1]
ax.fill_between(x1,y1, color="limegreen", alpha=0.3,label = 'Beauhurst deals')
ax.fill_between(x2,y2, color="salmon", alpha=0.3, label = 'SH01')
# ax.set_xlim(0.0,1.5) # 限制x的值为[0,20]
# ax.set_ylim(0,4) # 限制y的值为[0,1]
plt.ylabel('Density', fontsize = 15,labelpad=8)
plt.xlabel('Investment Amount', fontsize = 15,labelpad=6)
plt.tick_params(labelsize=13.5)
plt.legend()
# plt.show()

# change the date format
match['Deal date'] = pd.to_datetime(match['Deal date'])
match['action_date'] = pd.to_datetime(match['action_date'])
match['filing_date'] = pd.to_datetime(match['filing_date'])

further_match = pd.DataFrame()
for i in range(len(match)):
    if match['Deal date'][i] == match['action_date'][i]:
        aa = match.iloc[i:i+1]
        further_match = further_match.append(aa)
    else:
        pass

