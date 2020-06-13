#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:00:48 2020

@author: sakshirathi
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def getBookURLs(pageURL):
    response = requests.get(pageURL)
    data = BeautifulSoup(response.text,'html.parser')
    
    books = data.find_all(class_='product_pod')
    
    base_url = 'http://books.toscrape.com/catalogue/'
    
    books_urls = []
    
    for i in books:
        books_urls.append(base_url + i.h3.a['href'])
        
    return books_urls

def saveBookDetails(url,AllBookDetails):
    
    bookURLs = getBookURLs(url)
    
    for bookLink in bookURLs:
        response = requests.get(bookLink)
        data = BeautifulSoup(response.text,'html.parser')
        
        title = data.find('h1').string
        
        price_string = data.find(class_='price_color').string
        
        price = float(re.search('[\d.]+',price_string).group())
    
        
        q = data.find(class_='instock availability')
        
        qty_string = q.contents[-1].strip()
        
        qty = int(re.search('\d+',qty_string).group())
        
        detail = [title,bookLink,price,qty]

        AllBookDetails.append(detail)
        
allPages = ['http://books.toscrape.com/catalogue/page-1.html',
            'http://books.toscrape.com/catalogue/page-2.html']

AllBookDetails = []

for page in allPages:
    saveBookDetails(page, AllBookDetails)
    
AllBookDetails_df = pd.DataFrame(AllBookDetails, columns = ['Title','Link','Price','Quantity in Stock'])

AllBookDetails_df.to_csv('booksnew.csv')

for i in range(len(AllBookDetails_df)):
    print(AllBookDetails_df['Title'][i],AllBookDetails_df['Link'][i],AllBookDetails_df['Price'][i],AllBookDetails_df['Quantity in Stock'][i])
    