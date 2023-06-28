# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:12:36 2023

@author: wzxia
"""

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
        

'''
3. download PDFs for each company
'''
import os

# define the folder creation function
def mkdir(path):
    isExists = os.path.exists(path)
 
    if not isExists:
        os.makedirs(path) 
        print(path+'create the folder successfully')
        return True
    else:
        print(path+'the folder has existed')
        return False

# create folder
for com in companies_new:
    path = './data_PDFs/CompNum_' + com
    mkdir(path)

# download the PDFs from the CompanyHouse website
api_key = "86eb0eb5-ccbe-41cc-861a-2bebd865e64c"      
url = "https://api.company-information.service.gov.uk/company/{}/filing-history?category=capital&items_per_page={}&start_index={}"
items_per_page = 100
      
# for company_number in tqdm(companies_new): 
#     start_index = 0
#     response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
#     json_search_result = response.text
#     search_result = json.JSONDecoder().decode(json_search_result)
#     total_count = search_result['total_count']
    
#     if total_count < items_per_page: 
#         for idx in range(len(search_result['items'])):
#             if search_result['items'][idx]['type'] == 'SH01':
#                 if 'links' in search_result['items'][idx].keys():
#                     try: 
#                         link = search_result['items'][idx]['links']['document_metadata']
#                         metadata= requests.get(link, auth=(api_key, '')).json()        
#                         document_url = metadata['links']['document']
#                         response_new = requests.get(document_url, auth=(api_key,''), headers={'Accept': 'application/pdf'})
#                         aws_url = response_new.url
#                         response_new = requests.get(aws_url)
                        
#                         filename = company_number + "_" + str(idx+1) + '_' + search_result['items'][idx]['date']+".pdf"
#                         with open('./data_PDFs/CompNum_' + company_number + '/' + filename,'wb') as f:
#                             f.write(response_new.content)
#                         time.sleep(3)
#                     except:
#                         print(f'No PDF available for {filename}')   
#                         time.sleep(3)
#                 else:
#                         print(f'No PDF available for {filename} due to no links')
#     else:
#         calculator = int(np.ceil(total_count/items_per_page))
#         for i in range(calculator):
#             start_index = i * items_per_page
#             response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
#             json_search_result = response.text
#             search_result = json.JSONDecoder().decode(json_search_result)
            
#             for idx in range(len(search_result['items'])):
#                 if search_result['items'][idx]['type'] == 'SH01':
#                     if 'links' in search_result['items'][idx].keys():
#                         try: 
#                             link = search_result['items'][idx]['links']['document_metadata']
#                             metadata= requests.get(link, auth=(api_key, '')).json()        
#                             document_url = metadata['links']['document']
#                             response_new = requests.get(document_url, auth=(api_key,''), headers={'Accept': 'application/pdf'})
#                             aws_url = response_new.url
#                             response_new = requests.get(aws_url)
                            
#                             filename = company_number + "_" + str(idx+1) + '_' + search_result['items'][idx]['date']+".pdf"
#                             with open('./data_PDFs/CompNum_' + company_number + '/' + filename,'wb') as f:
#                                 f.write(response_new.content)
#                             time.sleep(3)
#                         except:
#                             print(f'No PDF available for {filename}')   
#                             time.sleep(3)
#                     else:
#                             print(f'No PDF available for {filename} due to no links')
            

# if there is a break in the above loop then run these following codes
for company_number in tqdm(companies_new): 
    path = './data_PDFs/CompNum_' + company_number
    files = os.listdir(path)
    num_txt = len(files)
    
    if num_txt == 0:
        start_index = 0
        response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
        json_search_result = response.text
        search_result = json.JSONDecoder().decode(json_search_result)
        total_count = search_result['total_count']
        
        if total_count < items_per_page: 
            for idx in range(len(search_result['items'])):
                if search_result['items'][idx]['type'] == 'SH01':
                    if 'links' in search_result['items'][idx].keys():
                        if 'document_metadata' in search_result['items'][idx]['links'].keys():
                            try: 
                                link = search_result['items'][idx]['links']['document_metadata']
                                metadata= requests.get(link, auth=(api_key, '')).json()        
                                document_url = metadata['links']['document']
                                response_new = requests.get(document_url, auth=(api_key,''), headers={'Accept': 'application/pdf'})
                                aws_url = response_new.url
                                response_new = requests.get(aws_url)
                                
                                filename = company_number + "_" + str(idx+1) + '_' + search_result['items'][idx]['date']+".pdf"
                                with open('./data_PDFs/CompNum_' + company_number + '/' + filename,'wb') as f:
                                    f.write(response_new.content)
                                time.sleep(3)
                            except:
                                print(f'No PDF available for {filename}')   
                                time.sleep(3)
                        else:
                            print(f'No document_metadata for {company_number}--{idx}')
                    else:
                        print(f'No PDF available for {filename} due to no links')

        else:
            calculator = int(np.ceil(total_count/items_per_page))
            for i in range(calculator):
                start_index = i * items_per_page
                response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
                json_search_result = response.text
                search_result = json.JSONDecoder().decode(json_search_result)
                
                for idx in range(len(search_result['items'])):
                    if search_result['items'][idx]['type'] == 'SH01':
                        if 'links' in search_result['items'][idx].keys():
                            if 'document_metadata' in search_result['items'][idx]['links'].keys():
                                try: 
                                    link = search_result['items'][idx]['links']['document_metadata']
                                    metadata= requests.get(link, auth=(api_key, '')).json()        
                                    document_url = metadata['links']['document']
                                    response_new = requests.get(document_url, auth=(api_key,''), headers={'Accept': 'application/pdf'})
                                    aws_url = response_new.url
                                    response_new = requests.get(aws_url)
                                    
                                    filename = company_number + "_" + str(idx+1) + '_' + search_result['items'][idx]['date']+".pdf"
                                    with open('./data_PDFs/CompNum_' + company_number + '/' + filename,'wb') as f:
                                        f.write(response_new.content)
                                    time.sleep(3)
                                except:
                                    print(f'No PDF available for {filename}')   
                                    time.sleep(3)
                            else:
                                print(f'No document_metadata for {company_number}--{idx}')
                        else:
                            print(f'No PDF available for {filename} due to no links')
    else:
        # finally check
        start_index = 0
        response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
        json_search_result = response.text
        search_result = json.JSONDecoder().decode(json_search_result)
        total_count = search_result['total_count']
        
        if total_count < items_per_page:
            SH01_num = 0
            dates = []
            links = []
            idxes = []
            for idx in range(len(search_result['items'])):
                if search_result['items'][idx]['type'] == 'SH01':
                    if 'links' in search_result['items'][idx].keys():
                        if 'document_metadata' in search_result['items'][idx]['links'].keys():
                            SH01_num = SH01_num + 1
                            dates.append(search_result['items'][idx]['date'])
                            links.append(search_result['items'][idx]['links']['document_metadata'])
                            idxes.append(idx+1)
                        else:
                            print(f'No document_metadata for {company_number}--{idx}')
                    else:
                        print(f'No link for {company_number}--{idx}')
            if num_txt == SH01_num:
                pass
            else:
                for idxx in range(len(dates)):
                    PDF_check = company_number + '_' + str(idxes[idxx]) + '_' + dates[idxx] + '.pdf'
                    if PDF_check in os.listdir(path):
                        pass
                    else:
                        if 'links' in search_result['items'][idx].keys():
                            if 'document_metadata' in search_result['items'][idx]['links'].keys():
                                try: 
                                    link = search_result['items'][idx]['links']['document_metadata']
                                    metadata= requests.get(link, auth=(api_key, '')).json()        
                                    document_url = metadata['links']['document']
                                    response_new = requests.get(document_url, auth=(api_key,''), headers={'Accept': 'application/pdf'})
                                    aws_url = response_new.url
                                    response_new = requests.get(aws_url)
                                    
                                    filename = company_number + "_" + str(idx+1) + '_' + search_result['items'][idx]['date']+".pdf"
                                    with open('./data_PDFs/CompNum_' + company_number + '/' + filename,'wb') as f:
                                        f.write(response_new.content)
                                    time.sleep(3)
                                except:
                                    print(f'No PDF available for {filename}')   
                                    time.sleep(3)
                            else:
                                print(f'No document_metadata for {company_number}--{idx}')
                        else:
                            print(f'No PDF available for {filename} due to no links')
                      
        else:
            calculator = int(np.ceil(total_count/items_per_page))  
            SH01_num = 0
            dates = []
            links = []
            idxes = []  
            for i in range(calculator):
                start_index = i * items_per_page
                response = requests.get(url.format(company_number,items_per_page,start_index),auth=(api_key,''))
                json_search_result = response.text
                search_result = json.JSONDecoder().decode(json_search_result)
        
                for idx in range(len(search_result['items'])):
                    if search_result['items'][idx]['type'] == 'SH01':
                        if 'links' in search_result['items'][idx].keys():
                            if 'document_metadata' in search_result['items'][idx]['links'].keys():
                                SH01_num = SH01_num + 1
                                dates.append(search_result['items'][idx]['date'])
                                links.append(search_result['items'][idx]['links']['document_metadata'])
                                idxes.append(idx+1)
                            else:
                                print(f'No document_metadata for {company_number}--{idx}')
                        else:
                            print(f'No link for {company_number}--{idx}')
            if num_txt == SH01_num:
                pass
            else:
                for idxx in range(len(dates)):
                    PDF_check = company_number + '_' + str(idxes[idxx]) + '_' + dates[idxx] + '.pdf'
                    if PDF_check in os.listdir(path):
                        pass
                    else:
                        if 'links' in search_result['items'][idx].keys():
                            if 'document_metadata' in search_result['items'][idx]['links'].keys():
                                try: 
                                    link = search_result['items'][idx]['links']['document_metadata']
                                    metadata= requests.get(link, auth=(api_key, '')).json()        
                                    document_url = metadata['links']['document']
                                    response_new = requests.get(document_url, auth=(api_key,''), headers={'Accept': 'application/pdf'})
                                    aws_url = response_new.url
                                    response_new = requests.get(aws_url)
                                    
                                    filename = company_number + "_" + str(idx+1) + '_' + search_result['items'][idx]['date']+".pdf"
                                    with open('./data_PDFs/CompNum_' + company_number + '/' + filename,'wb') as f:
                                        f.write(response_new.content)
                                    time.sleep(3)
                                except:
                                    print(f'No PDF available for {filename}')   
                                    time.sleep(3)
                            else:
                                print(f'No document_metadata for {company_number}--{idx}')
                        else:
                            print(f'No PDF available for {filename} due to no links')
            
# calculate the number of PDFs for each company
num_PDFs = []
years_PDFs = []
for company_number in tqdm(companies_new): 
    path = './data_PDFs/CompNum_' + company_number
    files = os.listdir(path)
    num_PDF = len(files)
    num_PDFs.append(num_PDF)
    for idx in range(num_PDF):
        files[idx] = files[idx][-14:-10]
    files.sort()
    years_PDFs.append(files)
        
df = pd.DataFrame()
df['CompanyID'] = companies_new
df['num_PDFs'] = num_PDFs
df['years_PDFs'] = years_PDFs

# check if there are specfic years included in our PDF years
# period [1995 - 2023]
# period [1997, 1998, 1999, 2000, 2002, 2003, 2005, 2008] are missing
for i in range(len(df)):
    if '1997' in df['years_PDFs'][i]:
        print('1997')
    if '1998' in df['years_PDFs'][i]:
        print('1998')
    if '1999' in df['years_PDFs'][i]:
        print('1999')
    if '2000' in df['years_PDFs'][i]:
        print('2000')
    if '2002' in df['years_PDFs'][i]:
        print('2002')
    if '2003' in df['years_PDFs'][i]:
        print('2003')
    if '2005' in df['years_PDFs'][i]:
        print('2005')
    if '2008' in df['years_PDFs'][i]:
        print('2008')
    
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib
sns.distplot(df['num_PDFs'],hist=True,kde=True,color='limegreen')
plt.show()
# plt.savefig('./num_PDFs.svg',bbox_inches='tight',dpi=600)

'''Notes'''
# 1. There are 6 categories of PDFs
#    For example: 1995, 1996, 2007, | 2009, | 2014
# 2. We can not define PDF category using years only
#    For the same year, there may be different PDFs' categories
# 3. We can manually scarpe data from the PDFs before 2009 (the amount of PDFs before 2009 is quite small) and only set different Python functions for other three main categories


'''
4. scrape data from PDFs
'''
# You may need to install pytesseract.  This is the ML tool that we use for optical character recognition.  If so uncomment line below
# pip install pytesseract
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# You may need to install cv2 via opencv. This is a library for general computer vision operations.  If so uncomment line below
# pip install opencv-python
import cv2
import os 

# define the folder creation function
def mkdir(path):
    isExists = os.path.exists(path)
 
    if not isExists:
        os.makedirs(path) 
        print(path+'create the folder successfully')
        return True
    else:
        print(path+'the folder has existed')
        return False

# create folder
for com in companies_new:
    path = './data_PDFs_images/CompNum_' + com
    mkdir(path)

poppler_location = 'C:/Program Files/poppler-0.68.0/bin'
# You Need to Install Poppler for Run The Following Loop
# It's fiddley to install using the usual methods (i.e. conda forge or pip)
# Best way is to extract the latest binary to C:/Program Files/
# Download the binary from here https://blog.alivate.com.au/poppler-windows/
# You then direct the function below to the poppler-0.68.0/bin file in that location
# I hardcode the location of this file in the poppler_location variable defined near the top of this code 

# pip install pdf2image
from pdf2image import convert_from_path

'''The first PDF category: italic words'''
# use the CompNum_04569647/04569647_14_2013-11-07.pdf as example
doc_path = './data_PDFs/CompNum_04569647/04569647_14_2013-11-07.pdf'
pages = convert_from_path(doc_path, 350, poppler_path = poppler_location)

# create image folder for this PDF
path = './data_PDFs_images/CompNum_04569647/04569647_14_2013-11-07'
mkdir(path)

# cut the PDF into different images and save them in this folder
i = 1
for page in pages:
    image_name = path + "/Page_" + str(i) + ".jpg"  
    page.save(image_name, "JPEG")
    i = i+1 

# The following function strips out the horizontal and vertical lines as these can improve the accuracy of the OCR
def remove_table_borders(image):
        result = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        contours = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        for c in contours:
            cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        contours = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        for c in contours:
            cv2.drawContours(result, [c], -1, (255, 255, 255), 5)
        return result

# The following code invokes the remove borders function and displays the new image without border    
image = cv2.imread(r'./data_PDFs_images/CompNum_04569647/04569647_14_2013-11-07/Page_1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image)
plt.show()
newimage = remove_table_borders(image)
plt.imshow(newimage)
plt.show()

# This function defines regions in the image
def mark_region(image_path):
    #image = cv2.imread(image_path)
    image = newimage
    # define threshold of regions to ignore
    THRESHOLD_REGION_IGNORE = 40
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)
    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        if w < THRESHOLD_REGION_IGNORE or h < THRESHOLD_REGION_IGNORE:
            continue
        image = cv2.rectangle(image, (x,y), (x+w, y+h), color=(255,0,255), thickness=3)
        line_items_coordinates.append([(x,y), (x+w, y+h)])
    return image, line_items_coordinates

image, line_items_coordinates = mark_region(image)
plt.figure(figsize=(20,20))
plt.imshow(image)
plt.show()

print(len(line_items_coordinates))

text_array = []
for i in reversed(range(len(line_items_coordinates))):
    left = line_items_coordinates[i][0][0]
    bottom = line_items_coordinates[i][0][1]
    right = line_items_coordinates[i][1][0]
    top = line_items_coordinates[i][1][1]
    crop = image[bottom:top, left:right]
    plt.imshow(crop)
    ret,thresh1 = cv2.threshold(crop,220,255,cv2.THRESH_BINARY)
    # 200 is the key parameter that need to be adjusted
    config = '--oem 3  --psm 6'
    text = str(pytesseract.image_to_string(thresh1, config='config'))
    print("This is region " +str(len(line_items_coordinates)-i))
    print(text)
    text_array.append(text)

index = [idx for idx, s in enumerate(text_array) if 'Class of share' in s]
index2 = [idx for idx, s in enumerate(text_array) if 'Amount paid' in s]
share_class = [text_array[i+1] for i in index]
number_alloted = [text_array[i+2] for i in index]
nominal_value_per_share = [text_array[i+3] for i in index]
amount_paid_per_share = [text_array[i+1] for i in index2]
amount_unpaid_per_share = [text_array[i+2] for i in index2]
# need to use 0.0 to replace '' for amount_unpaid_per_share

print('share_class is: ', share_class)
print('number_alloted is: ', number_alloted)
print('nominal_value_per_share is: ', nominal_value_per_share)
print('amount_paid_per_share is: ', amount_paid_per_share)
print('amount_unpaid_per_share is: ', amount_unpaid_per_share)


'''The second PDF category: Orthographic words'''
# use the CompNum_04569647/04569647_56_2014-09-02.pdf as example
doc_path = './data_PDFs/CompNum_04569647/04569647_56_2014-09-02.pdf'
pages = convert_from_path(doc_path, 350, poppler_path = poppler_location)

# create image folder for this PDF
path = './data_PDFs_images/CompNum_04569647/04569647_56_2014-09-02'
mkdir(path)

# cut the PDF into different images and save them in this folder
i = 1
for page in pages:
    image_name = path + "/Page_" + str(i) + ".jpg"  
    page.save(image_name, "JPEG")
    i = i+1 

# The following function strips out the horizontal and vertical lines as these can improve the accuracy of the OCR
def remove_table_borders(image):
        result = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        contours = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        for c in contours:
            cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        contours = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        for c in contours:
            cv2.drawContours(result, [c], -1, (255, 255, 255), 5)
        return result

# The following code invokes the remove borders function and displays the new image without border    
image = cv2.imread(r'./data_PDFs_images/CompNum_04569647/04569647_56_2014-09-02/Page_1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image)
plt.show()
newimage = remove_table_borders(image)
plt.imshow(newimage)
plt.show()

# This function defines regions in the image
def mark_region(image_path):
    #image = cv2.imread(image_path)
    image = newimage
    # define threshold of regions to ignore
    THRESHOLD_REGION_IGNORE = 40
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)
    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        if w < THRESHOLD_REGION_IGNORE or h < THRESHOLD_REGION_IGNORE:
            continue
        image = cv2.rectangle(image, (x,y), (x+w, y+h), color=(255,0,255), thickness=3)
        line_items_coordinates.append([(x,y), (x+w, y+h)])
    return image, line_items_coordinates

image, line_items_coordinates = mark_region(image)
plt.figure(figsize=(20,20))
plt.imshow(image)
plt.show()

print(len(line_items_coordinates))

text_array = []
for i in reversed(range(len(line_items_coordinates))):
    left = line_items_coordinates[i][0][0]
    bottom = line_items_coordinates[i][0][1]
    right = line_items_coordinates[i][1][0]
    top = line_items_coordinates[i][1][1]
    crop = image[bottom:top, left:right]
    plt.imshow(crop)
    ret,thresh1 = cv2.threshold(crop,220,255,cv2.THRESH_BINARY)
    # 200 is the key parameter that need to be adjusted
    config = '--oem 3  --psm 6'
    text = str(pytesseract.image_to_string(thresh1, config='config'))
    print("This is region " +str(len(line_items_coordinates)-i))
    print(text)
    text_array.append(text)

index = [idx for idx, s in enumerate(text_array) if 'Class of Shares' in s]
index2 = [idx for idx, s in enumerate(text_array) if 'Number allotted' in s]
share_class = [text_array[i+1] for i in index]
number_alloted = [text_array[i+1] for i in index2]
index3 = [idx for idx, s in enumerate(text_array) if 'Amount paid' in s]
nominal_value_per_share = [text_array[i-1] for i in index3]
amount_paid_per_share = [text_array[i+1] for i in index3]
index4 = [idx for idx, s in enumerate(text_array) if 'Amount unpaid' in s]
amount_unpaid_per_share = [text_array[i+1] for i in index4]
# need to use 0.0 to replace '' for amount_unpaid_per_share

print('share_class is: ', share_class)
print('number_alloted is: ', number_alloted)
print('nominal_value_per_share is: ', nominal_value_per_share)
print('amount_paid_per_share is: ', amount_paid_per_share)
print('amount_unpaid_per_share is: ', amount_unpaid_per_share)


'''The third PDF category: old forms'''


















