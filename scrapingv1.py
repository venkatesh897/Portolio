
from bs4 import BeautifulSoup 
import requests 
import smtplib 
import time 
import datetime 
import csv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import csv 


header = ['Title', 'Price','stars','color','reviewCount','date']

with open('AmazonWebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

baseurl = 'https://www.amazon.in/s?k=phones&ref=nb_sb_noss'
def next_page(soup):
        try:
            if not soup.find('span', {'class': 's-pagination-strip'}).find('span',{'class':['s-pagination-next', 's-pagination-disabled ']}):
                pages = soup.find('span', {'class': 's-pagination-strip'}).find('a',{'class': 's-pagination-next'})['href']  
                url = 'https://www.amazon.in' + str(pages)
                return url
            else:
                return 0
        except:
            print("error")
   


def get_data(baseurl):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",}
    
    page = requests.get(baseurl, headers=headers)
    
    soup1 = BeautifulSoup(page.content, "html.parser")
    
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    

    for urlContainer in soup2.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
       
        productUrl = 'https://www.amazon.in' + str(urlContainer['href'])
        try:
            ProductData = requests.get(productUrl, headers=headers,verify=False)
        except:
            print("An exception occurred")

        
        
        try:
            soup3 = BeautifulSoup(ProductData.content, "html.parser")
        except:
            print("error")    
        try:
            soup4 = BeautifulSoup(soup3.prettify(), "html.parser")
        except:
            print("error")

        
        try:
            ProductTitle = soup4.find(id="productTitle").get_text().strip()
            productPrice = soup4.find('span', {'class': 'a-price-whole'}).get_text().strip()
            formattedProductPrice = productPrice.replace(".", "")

            reviewPoints = soup4.find('span', {'class': 'a-icon-alt'}).get_text().strip()
            today = datetime.date.today()
        except:
            print("error")
        try:
            color = soup4.find('span', {'class': 'selection'}).get_text().strip()
        except:
            print("error")

        try:
            reviewCount = soup4.find('span',{'data-hook':'total-review-count'}).get_text().strip()
        except:
            print("error")
        
   

        
        

        data = [ProductTitle,formattedProductPrice.strip(),reviewPoints[:4],color,reviewCount,today]

        with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    

        

        

    

    nextPageurl = next_page(soup2)

    

    if(nextPageurl != 0):
        get_data(nextPageurl)



    
        
        

get_data(baseurl)


