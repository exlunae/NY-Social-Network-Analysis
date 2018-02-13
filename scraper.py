from bs4 import BeautifulSoup
import requests 

#Loops through the specified page numbers for the analsis: pages for prior to December 1, 2014 
for i in range(6, 31):
    url = "http://www.newyorksocialdiary.com/party-pictures?page=%d" %i 
    #response = requests.get(url) 
    print(url)

#soup = BeautifulSoup(response.text)
#print(soup.prettify())